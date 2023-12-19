"""Base module for pulsefire.

This module contains the base classes for implementing pulsefire.
"""

from base64 import b64encode
from typing import Any, Literal
from types import MethodType
import os
import urllib.parse

import aiohttp


type HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class Invocation:
    """Container used for building and peforming HTTP request."""

    uid: str
    """Invocation UID (unique per instance)."""
    method: HttpMethod
    """HTTP method."""
    urlformat: str
    """URL format (bracket based)."""
    params: dict[str, Any]
    """Invocation parameters (includes queries and headers)."""
    session: aiohttp.ClientSession | None
    """Client session used for request. Cannot perform HTTP request if is None."""
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
        if self.session is None:
            raise RuntimeError("session is None, cannot perform HTTP request")
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
