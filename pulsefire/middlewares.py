"""Module for pulsefire middlewares.

This module contains middlewares used by pulsefire clients, middlewares provides
flexible ways to manipulate and run operations on invocations and responses.
"""

from typing import Any, Callable
import asyncio
import collections
import json
import logging
import math
import time

import aiohttp

from .base import Invocation, MiddlewareCallable


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

    Response history can be accessed on `.history` after catching `aiohttp.ClientResponseError`.

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
            response_history: list[aiohttp.ClientResponse] = []
            for attempt in range(max_retries + 1):
                if attempt:
                    await asyncio.sleep(2 ** attempt)
                response: aiohttp.ClientResponse = await next(invocation)
                response_history.append(response)
                if 300 > response.status >= 200:
                    return response
                if not (response.status == 429 or response.status >= 500):
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response_history,
                        status=response.status,
                        message=await response.text(),
                        headers=response.headers,
                    )
            else:
                raise aiohttp.ClientResponseError(
                    response_history[-1].request_info,
                    response_history,
                    status=response_history[-1].status,
                    message=await response.text(),
                    headers=response_history[-1].headers,
                )

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


def riot_api_rate_limiter_middleware(weight: float = 1):
    """Riot API rate limiter middleware.

    Should be positioned as late as possible in the client middlewares list.
    This rate limiter lives in-memory; therefore, its entries are not shareable across hardwares.

    **Multiple middlewares does not share the same entries**, to shared entries between
    multiple clients, create this middleware separately and pass as variable to
    the middlewares list.

    Example:
    ```python
    riot_api_rate_limiter_middleware(1) # Use full rate limits
    riot_api_rate_limiter_middleware(0.5) # Use half of the rate limits
    ```

    Parameters:
        weight: Rate limiter will use capacity up to `limit*weight`
    """

    entries: dict[tuple[str, int, *tuple[str]], tuple[int, int, float, float, bool]] = \
        collections.defaultdict(lambda: (0, 0, 0, 0, False))
    last_429s = collections.deque(maxlen=10)

    def constructor(next: MiddlewareCallable):

        async def middleware(invocation: Invocation):
            while True:
                max_sleep = 0
                pinging_targets = []
                requesting_targets = []
                request_time = time.time()
                for target in [
                    ("app", 0, invocation.params.get("region", ""), invocation.method),
                    ("app", 1, invocation.params.get("region", ""), invocation.method),
                    ("method", 0, invocation.params.get("region", ""), invocation.method, invocation.url),
                    ("method", 1, invocation.params.get("region", ""), invocation.method, invocation.url)
                ]:
                    count, limit, expire, latency, pinging = entries[target]
                    if pinging:
                        max_sleep = max(max_sleep, 0.1)
                    elif request_time > expire:
                        pinging_targets.append(target)
                    elif request_time > expire - latency * 1.1 + 0.01 or count >= math.floor(limit * weight):
                        max_sleep = max(max_sleep, expire - request_time)
                    else:
                        requesting_targets.append(target)
                if max_sleep <= 0:
                    for pinging_target in pinging_targets:
                        entries[pinging_target] = (0, 0, 0, 0, True)
                    for requesting_target in requesting_targets:
                        count, *values = entries[requesting_target]
                        entries[requesting_target] = (count + 1, *values)
                    break
                await asyncio.sleep(max_sleep)

            response: aiohttp.ClientResponse = await next(invocation)
            response_time = time.time()

            if response.status == 429:
                last_429s.append(response_time)
                if sum(response_time - prev_time < 10 for prev_time in last_429s) >= 10:
                    logging.warn(f"riot_api_rate_limiter_middleware: detected elevated amount of http 429 responses")
                    last_429s.clear()

            try:
                header_limits = {
                    "app": [[int(v) for v in t.split(':')] for t in response.headers["X-App-Rate-Limit"].split(',')],
                    "method": [[int(v) for v in t.split(':')] for t in response.headers["X-Method-Rate-Limit"].split(',')],
                }
                header_counts = {
                    "app": [[int(v) for v in t.split(':')] for t in response.headers["X-App-Rate-Limit-Count"].split(',')],
                    "method": [[int(v) for v in t.split(':')] for t in response.headers["X-Method-Rate-Limit-Count"].split(',')],
                }
                for scope, idx, *subscopes in pinging_targets:
                    if idx >= len(header_limits[scope]):
                        entries[(scope, idx, *subscopes)] = (0, 10**10, response_time + 3600, 0, False)
                        continue
                    entries[(scope, idx, *subscopes)] = (
                        header_counts[scope][idx][0],
                        header_limits[scope][idx][0],
                        header_limits[scope][idx][1] + response_time,
                        response_time - request_time,
                        False
                    )
            except KeyError:
                for pinging_target in pinging_targets:
                    entries[pinging_target] = (0, 0, 0, 0, False)
            return response

        return middleware

    return constructor
