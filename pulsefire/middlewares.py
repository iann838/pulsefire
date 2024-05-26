"""Module for pulsefire middlewares.

This module contains middlewares used by pulsefire clients, middlewares provides
flexible ways to manipulate and run operations on invocations and responses.
"""

from typing import Any, Awaitable, Callable
import asyncio
import collections
import json
import logging
import time

import aiohttp

from .caches import BaseCache
from .invocation import Invocation
from .ratelimiters import BaseRateLimiter


type MiddlewareCallable = Callable[["Invocation"], Awaitable[Any]]
type Middleware = Callable[[MiddlewareCallable], MiddlewareCallable]


LOGGER = logging.getLogger("pulsefire.middlewares")


def http_error_middleware(max_retries: int = 3):
    """HTTP error middleware.

    Should be positioned as late as possible and before rate limiter middlewares
    (if any) in the client middlewares list.

    Responses are handled differently based on their HTTP status:

    | Status | Measures                              |
    | ------ | ------------------------------------- |
    | 2XX    | Return response.                      |
    | 3XX    | Raise `aiohttp.ClientResponseError`.  |
    | 4XX    | Raise `aiohttp.ClientResponseError`.  |
    | 429    | Exponential retries (2^n).            |
    | 5XX    | Exponential retries (2^n).            |
    | Conn   | Exponential retries (2^n).            |

    Example:
    ```python
    http_error_middleware(3)
    ```

    Parameters:
        max_retries: Number of retries to perform before giving up.

    Raises:
        aiohttp.ClientResponseError: When retries have exhausted.
    """

    def constructor(next: MiddlewareCallable):

        async def middleware(invocation: Invocation):
            last_response: aiohttp.ClientResponse | None = None
            last_connexc: aiohttp.ClientConnectionError | asyncio.TimeoutError = asyncio.TimeoutError()
            for attempt in range(max_retries + 1):
                if attempt:
                    await asyncio.sleep(2 ** attempt)
                try:
                    response: aiohttp.ClientResponse = await next(invocation)
                except (asyncio.TimeoutError, aiohttp.ClientConnectionError) as connexc:
                    last_connexc = connexc
                    continue
                last_response = response
                if 300 > response.status >= 200:
                    return response
                if not (response.status == 429 or response.status >= 500):
                    response.raise_for_status()
            else:
                if last_response:
                    last_response.raise_for_status()
                raise last_connexc

        return middleware

    return constructor


def json_response_middleware(loads: Callable[[str | bytes | bytearray], Any] = json.loads):
    """JSON response middleware.

    Attempts to deserialize JSON responses regardless of content type,
    if an exception is raised during deserialization, bytes are returned instead.

    Example:
    ```python
    # Use orjson loads for 3~10x faster deserialization
    import orjson
    json_response_middleware(orjson.loads)
    ```

    Parameters:
        loads: JSON decoder to be used on deserialization.
    """

    def constructor(next: MiddlewareCallable):

        async def middleware(invocation: Invocation):
            response: aiohttp.ClientResponse = await next(invocation)
            try:
                return await response.json(encoding="utf-8", content_type=None, loads=loads)
            except Exception:
                return await response.read()

        return middleware

    return constructor


def cache_middleware(cache: BaseCache, rules: list[tuple[Callable[[Invocation], bool], float]]):
    """Cache middleware.

    Recommended to be placed before response deserialization middlewares.

    Example:
    ```python
    cache = MemoryCache()
    cache_middleware(cache, [
        (lambda inv: inv.invoker.__name__ == "get_lol_v1_champion", 3600),
        (lambda inv: inv.invoker.__name__ ..., float("inf")), # cache indefinitely.
        (lambda inv: inv.url ..., 3600),
        (lambda inv: inv.params ..., 3600),
    ])
    ```

    Parameters:
        cache: Cache instance.
        rules: Cache rules, defined by a list of (condition, ttl).
    """

    rules.append((lambda _: True, 0)) # Add default

    def constructor(next: MiddlewareCallable):

        async def middleware(invocation: Invocation):
            key = f"{invocation.method} {invocation.url}"
            for cond, ttl in rules:
                if not cond(invocation):
                    continue
                try:
                    value = await cache.get(key)
                except KeyError:
                    value = await next(invocation)
                    await cache.set(key, value, ttl)
                return value
            raise RuntimeError("rules out of range")

        return middleware

    return constructor


def rate_limiter_middleware(rate_limiter: BaseRateLimiter):
    """Rate limiter middleware.

    Should be positioned as late as possible in the client middlewares list.

    Example:
    ```python
    rate_limiter = RiotAPIRateLimiter()
    rate_limiter_middleware(rate_limiter)
    ```

    Parameters:
        rate_limiter: Rate limiter instance.
    """

    track_429s = collections.deque(maxlen=12)

    def constructor(next: MiddlewareCallable):

        async def middleware(invocation: Invocation):
            while True:
                wait_for = await rate_limiter.acquire(invocation)
                if wait_for <= 0:
                    break
                await asyncio.sleep(wait_for)

            response: aiohttp.ClientResponse = await next(invocation)

            if response.status == 429:
                response_time = time.time()
                track_429s.append(response_time)
                if sum(response_time - prev_time < 10 for prev_time in track_429s) >= 10:
                    LOGGER.warning(f"rate_limiter_middleware: detected elevated amount of http 429 responses")
                    track_429s.clear()

            if wait_for == -1:
                await rate_limiter.synchronize(invocation, response.headers)

            return response

        return middleware

    return constructor
