"""Base module for pulsefire.

This module contains the base classes for implementing pulsefire.
"""

from base64 import b64encode
from typing import Any, Awaitable, Callable, Literal
from types import MethodType
import abc
import asyncio
import contextlib
import functools
import inspect
import itertools
import os
import sys
import urllib.parse

import aiohttp


type HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
type MiddlewareCallable = Callable[["Invocation"], Awaitable[Any]]
type Middleware = Callable[[MiddlewareCallable], MiddlewareCallable]


class Client(abc.ABC):
    """Base client class.

    Inherit from this class to implement a client.
    """

    base_url: str
    """Base URL, can be extended by `invoke`."""
    default_headers: dict[str, str]
    """Default params (ignores `...`), can be overwritten by `invoke`."""
    default_params: dict[str, Any]
    """Default header params, can be overwritten by `invoke`."""
    default_queries: dict[str, str]
    """Default query params, can be overwritten by `invoke`."""
    middlewares: list[Middleware]
    """Pre and post processors during `invoke`."""
    session: aiohttp.ClientSession | None = None
    """Context manager client session."""

    def __init__(
        self,
        *,
        base_url: str,
        default_params: dict[str, Any] = {},
        default_headers: dict[str, str] = {},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [],
    ) -> None:
        self.base_url = base_url
        self.default_headers = default_headers
        self.default_params = default_params
        self.default_queries = default_queries
        self.middlewares = middlewares
        async def run_invocation(invocation: "Invocation"):
            return await invocation()
        self.middleware_begin = run_invocation
        for middleware in middlewares[::-1]:
            self.middleware_begin = middleware(self.middleware_begin)
            if not inspect.iscoroutinefunction(self.middleware_begin):
                raise TypeError(f"{self.middleware_begin} is not a coroutine function")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={id(self)}>"

    def __call__[**P, R](self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Context manager decorator, see `__aenter__`."""
        if not inspect.iscoroutinefunction(func):
            raise TypeError(f"{func} is not a coroutine function")
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with self:
                return await func(*args, **kwargs)
        return wrapper

    async def __aenter__(self):
        """Context manager, in-context invocations will reuse a single `aiohttp.ClientSession`
        improving performance and memory footprint.

        Raises:
            RuntimeError: When entering an already entered client.
        """
        if self.session:
            raise RuntimeError(f"{self!r} has been already entered")
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *_) -> None:
        transports = 0
        transports_closed = asyncio.Event()

        def connection_lost(exc, orig_lost):
            nonlocal transports
            try:
                orig_lost(exc)
            finally:
                transports -= 1
                if transports == 0:
                    transports_closed.set()

        def eof_received(orig_eof_received):
            try:
                orig_eof_received()
            except AttributeError:
                pass

        for conn in self.session.connector._conns.values():
            for handler, _ in conn:
                proto: asyncio.Protocol = getattr(handler.transport, "_ssl_protocol", None)
                if proto is None:
                    continue
                transports += 1
                orig_lost = proto.connection_lost
                orig_eof_received = proto.eof_received
                proto.connection_lost = functools.partial(
                    connection_lost, orig_lost=orig_lost
                )
                proto.eof_received = functools.partial(
                    eof_received, orig_eof_received=orig_eof_received
                )
        if transports == 0:
            transports_closed.set()

        await self.session.close()
        await transports_closed.wait()
        self.session = None

    async def invoke(self, method: HttpMethod, path_or_url: str):
        """Build an Invocation and send through the middlewares.

        Params are automatically grabbed from the outer frame (ignores `...`).
        The invoker client method is automatically grabbed from the outer frame
        and passed to the instantiation of Invocation.
        """
        async with contextlib.nullcontext() if self.session else aiohttp.ClientSession() as session:
            session = session or self.session
            params = {}
            for key, value in itertools.chain(self.default_params.items(), sys._getframe(1).f_locals.items()):
                if key != "self" and value != ...:
                    params[key] = value
            params["queries"] = {**self.default_queries, **params.get("queries", {})}
            params["headers"] = {**self.default_headers, **params.get("headers", {})}
            invoker: MethodType | None = getattr(self, sys._getframe(1).f_code.co_name, None)
            invocation = Invocation(method, self.base_url + path_or_url, params, session, invoker=invoker)
            return await self.middleware_begin(invocation)


class Invocation:
    """Objects containing data used for building and peforming HTTP request."""

    uid: str
    """Invocation UID (unique per instance)."""
    method: HttpMethod
    """HTTP method."""
    urlformat: str
    """URL format (bracket based)."""
    params: dict[str, Any]
    """Invocation parameters (includes queries and headers)."""
    session: aiohttp.ClientSession | None
    """Client session used for request. Cannot perform HTTP request if set to None."""
    invoker: MethodType | None
    """Bound method if invoked by client method, None otherwise."""

    def __init__(
        self,
        method: HttpMethod,
        urlformat: str,
        params: dict[str, Any],
        session: aiohttp.ClientSession | None = None,
        *,
        invoker: MethodType | None = None,
        uid: str | None = None,
    ) -> None:
        self.uid = uid or b64encode(os.urandom(12)).decode("utf-8")
        self.method = method
        self.urlformat = urlformat
        self.params = params
        self.session = session
        self.invoker = invoker

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} uid={self.uid} method={self.method} url={self.url}>"

    async def __call__(self) -> aiohttp.ClientResponse:
        """Build and perform HTTP request."""
        return await self.session.request(
            self.method,
            self.url,
            headers=self.params.get("headers", {}),
            json=self.params.get("json", None),
            data=self.params.get("data", None),
        )

    @property
    def url(self) -> str:
        """Build URL (includes query parameters).

        Raises:
            KeyError: When a path parameter is missing.
        """
        url = self.urlformat.format(**self.params)
        if queries := self.params.get("queries", {}):
            url += '?' + urllib.parse.urlencode(queries)
        return url


class RateLimiter(abc.ABC):
    """Base rate limiter class.
    
    Inherit this class to implement a rate limiter.
    """

    @abc.abstractmethod
    async def acquire(self, invocation: Invocation) -> float:
        """Acquire a wait_for value in seconds.

        | wait_for | action required  |
        | :------: | ---------------- |
        | -1       | Proceed then synchronize. |
        | 0        | Proceed then skip synchronize. |
        | >0       | Wait for value in seconds then acquire again. |
        """

    @abc.abstractmethod
    async def synchronize(self, invocation: Invocation, headers: dict[str, str]) -> None:
        """Synchronize rate limiting headers to index."""
