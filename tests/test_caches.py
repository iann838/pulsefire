import asyncio

from pulsefire.caches import (
    MemoryCache,
    DiskCache
)
from pulsefire.clients import CDragonClient
from pulsefire.functools import async_to_sync
from pulsefire.middlewares import (
    cache_middleware,
    http_error_middleware,
    json_response_middleware,
    MiddlewareCallable,
    Invocation
)


def detect_cache_expire_middleware(prev_urls: set[str]):
    def constructor(next: MiddlewareCallable):
        async def middleware(invocation: Invocation):
            assert invocation.url not in prev_urls
            try:
                return await next(invocation)
            finally:
                prev_urls.add(invocation.url)
        return middleware
    return constructor


@async_to_sync()
async def test_memory_cache():
    prev_urls = set()
    cache = MemoryCache()
    async with CDragonClient(
        default_params={"patch": "latest", "locale": "default"},
        middlewares=[
            cache_middleware(cache, [
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_champion", 10),
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_items", 200),
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_summoner_spells", float("inf")),
            ]),
            detect_cache_expire_middleware(prev_urls),
            json_response_middleware(),
            http_error_middleware(),
        ]
    ) as client:
        await client.get_lol_v1_items()
        await client.get_lol_v1_items()

        await client.get_lol_v1_summoner_spells()
        await client.get_lol_v1_summoner_spells()
        await asyncio.sleep(2)
        await client.get_lol_v1_summoner_spells() # still cached

        await client.get_lol_v1_champion(id=777)
        await client.get_lol_v1_champion(id=777)
        await asyncio.sleep(10)
        try:
            await client.get_lol_v1_champion(id=777) # cache expired
            assert False, "Expected exception"
        except AssertionError:
            assert True


@async_to_sync()
async def test_disk_cache():
    prev_urls = set()
    cache = DiskCache("tests/__pycache__/diskcache")
    await cache.clear()
    async with CDragonClient(
        default_params={"patch": "latest", "locale": "default"},
        middlewares=[
            cache_middleware(cache, [
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_champion", 10),
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_items", 200),
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_summoner_spells", float("inf")),
            ]),
            detect_cache_expire_middleware(prev_urls),
            json_response_middleware(),
            http_error_middleware(),
        ]
    ) as client:
        await client.get_lol_v1_items()
        await client.get_lol_v1_items()

        await client.get_lol_v1_summoner_spells()
        await client.get_lol_v1_summoner_spells()
        await asyncio.sleep(2)
        await client.get_lol_v1_summoner_spells() # still cached

        await client.get_lol_v1_champion(id=777)
        await client.get_lol_v1_champion(id=777)
        await asyncio.sleep(10)
        try:
            await client.get_lol_v1_champion(id=777) # cache expired
            assert False, "Expected exception"
        except AssertionError:
            assert True
