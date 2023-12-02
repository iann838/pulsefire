"""Module for pulsefire middlewares.

This module contains middlewares used by pulsefire clients, middlewares provides
flexible ways to manipulate and run operations on invocations and responses.
"""

from typing import Any, Callable
import asyncio
import collections
import json
import logging
import time

import aiohttp

from .base import RateLimiter, Invocation, MiddlewareCallable


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
            last_response: aiohttp.ClientResponse = None
            for attempt in range(max_retries + 1):
                if attempt:
                    await asyncio.sleep(2 ** attempt)
                response: aiohttp.ClientResponse = await next(invocation)
                last_response = response
                if 300 > response.status >= 200:
                    return response
                if not (response.status == 429 or response.status >= 500):
                    response.raise_for_status()
            else:
                last_response.raise_for_status()

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


def ttl_cache_middleware(ttl: float, cond: Callable[[Invocation], bool] = lambda _: True):
    """TTL cache middleware.

    Recommended to be placed before response deserialization middlewares.
    This cache lives in-memory, be aware of memory footprint when caching large responses.

    Example:
    ```python
    # Cache all for 1 hour.
    ttl_cache_middleware(3600, lambda _: True)
    # Cache if invoker function name ... for 1 hour.
    ttl_cache_middleware(3600, lambda inv: inv.invoker.__name__ ...)
    # Cache if invocation url ... for 1 hour.
    ttl_cache_middleware(3600, lambda inv: inv.url ...)
    # Cache if invocation params ... for 1 hour.
    ttl_cache_middleware(3600, lambda inv: inv.params ...)

    # Using multiple or complex conditions
    def sample_cache_cond(inv: Invocation) -> bool: ...
    ttl_cache_middleware(3600, sample_cache_cond)
    ```

    Parameters:
        ttl: Time in seconds objects should remain cached.
        cond: Run cache logic if `cond(invocation)` is true.
    """

    cache: dict[tuple[str, str], tuple[Any, float]] = {}
    last_expired = time.time()

    def cache_expire():
        for cache_key, (_, expire) in list(cache.items()):
            if time.time() > expire:
                cache.pop(cache_key, None)

    def constructor(next: MiddlewareCallable):

        async def middleware(invocation: Invocation):
            nonlocal last_expired
            if not cond(invocation):
                return await next(invocation)
            cache_key = (invocation.method, invocation.url)
            try:
                response, expire = cache[cache_key]
                if time.time() > expire:
                    cache.pop(cache_key, None)
                    raise KeyError(cache_key)
            except KeyError:
                response = await next(invocation)
                cache[cache_key] = [response, time.time() + ttl]
            if time.time() - last_expired > 60:
                last_expired = time.time()
                cache_expire()
            return response

        return middleware

    return constructor


def rate_limiter_middleware(rate_limiter: RateLimiter):
    """Rate limiter middleware.

    Should be positioned as late as possible in the client middlewares list.

    Example:
    ```python
    rate_limiter_middleware(RiotAPIRateLimiter())
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
