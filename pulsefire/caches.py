"""Module for pulsefire caches.

This module contains cache implementations for pulsefire.
"""

from typing import Any, Callable
import abc
import math
import time
import pickle

from .functools import sync_to_async
from .invocation import Invocation


type CacheRule = tuple[Callable[[Invocation], bool], float]


class BaseCache(abc.ABC):
    """Base cache class.

    Inherit from this class to implement a cache.
    """

    @abc.abstractmethod
    async def get[T](self, key: str) -> T:
        """Get a value from cache."""

    @abc.abstractmethod
    async def set(self, key: str, value: Any, ttl: float) -> None:
        """Set a value to cache."""

    @abc.abstractmethod
    async def clear(self) -> None:
        """Clear all values in cache."""


class MemoryCache(BaseCache):
    """Memory Cache.

    This cache lives in-memory, be aware of memory footprint when caching large responses.

    Example:
    ```python
    MemoryCache()
    ```
    """

    cache: dict[str, tuple[Any, float]]

    def __init__(self) -> None:
        self.cache = {}
        self.last_expired = time.time()

    async def get[T](self, key: str) -> T:
        value, expire = self.cache[key]
        if time.time() > expire:
            self.cache.pop(key, None)
            raise KeyError(key)
        return value

    async def set(self, key: str, value: Any, ttl: float) -> None:
        if ttl <= 0:
            return
        self.cache[key] = [value, time.time() + ttl]
        if time.time() - self.last_expired > 60:
            self.last_expired = time.time()
            for old_key, (_, expire) in self.cache.items():
                if time.time() > expire:
                    self.cache.pop(old_key, None)

    async def clear(self) -> None:
        self.cache.clear()


class DiskCache(BaseCache):
    """Disk Cache.

    Requires `diskcache` installed. This cache lives on disk, meaning cheaper storage but slower access.

    Example:
    ```python
    DiskCache() # Cache on tmp
    DiskCache("folder") # Cache on folder/
    ```

    Parameters:
        directory: Cache directory, uses tmp if None.
        shards: Number of shards to distribute writes.
        serializer: Serializer package supporting `loads` and `dumps`.
    """

    def __init__(self, directory: str | None = None, shards: int = 8, serializer=pickle) -> None:
        import diskcache
        self.directory = directory
        self.serializer = serializer
        self.cache = diskcache.FanoutCache(directory, shards)

    @sync_to_async()
    def get[T](self, key: str) -> T:
        value = self.cache.get(key)
        if value is None:
            raise KeyError(key)
        return self.serializer.loads(value)

    @sync_to_async()
    def set(self, key: str, value: Any, ttl: float) -> None:
        if ttl <= 0:
            return
        if math.isinf(ttl):
            ttl = None
        self.cache.set(key, self.serializer.dumps(value), ttl)

    @sync_to_async()
    def clear(self) -> None:
        self.cache.clear()
