from contextlib import contextmanager
import asyncio
import time

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
)


@contextmanager
def timer():
    t1 = t2 = time.perf_counter()
    yield lambda: t2 - t1
    t2 = time.perf_counter()


@async_to_sync()
async def test_memory_cache():
    cache = MemoryCache()
    async with CDragonClient(
        default_params={"patch": "latest", "locale": "default"},
        middlewares=[
            cache_middleware(cache, [
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_champion", 10),
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_items", 200),
                (lambda inv: inv.invoker.__name__ == "get_lol_v1_summoner_spells", float("inf")),
            ]),
            json_response_middleware(),
            http_error_middleware(),
        ]
    ) as client:
        (await client.get_lol_v1_items())[0]["_CACHED"] = 1
        assert (await client.get_lol_v1_items())[0].get("_CACHED", 0) == 1

        (await client.get_lol_v1_summoner_spells())[0]["_CACHED"] = 1
        assert (await client.get_lol_v1_summoner_spells())[0].get("_CACHED", 0) == 1
        await asyncio.sleep(2)
        assert (await client.get_lol_v1_summoner_spells())[0].get("_CACHED", 0) == 1 # still cached

        (await client.get_lol_v1_champion(id=777))["_CACHED"] = 1
        assert (await client.get_lol_v1_champion(id=777)).get("_CACHED", 0) == 1
        await asyncio.sleep(10)
        assert (await client.get_lol_v1_champion(id=777)).get("_CACHED", 0) == 0 # cache expired


@async_to_sync()
async def test_disk_cache():
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
            json_response_middleware(),
            http_error_middleware(),
        ]
    ) as client:
        (await client.get_lol_v1_items())[0]["_CACHED"] = 1
        assert (await client.get_lol_v1_items())[0].get("_CACHED", 0) == 1

        (await client.get_lol_v1_summoner_spells())[0]["_CACHED"] = 1
        assert (await client.get_lol_v1_summoner_spells())[0].get("_CACHED", 0) == 1
        await asyncio.sleep(2)
        assert (await client.get_lol_v1_summoner_spells())[0].get("_CACHED", 0) == 1 # still cached

        (await client.get_lol_v1_champion(id=777))["_CACHED"] = 1
        assert (await client.get_lol_v1_champion(id=777)).get("_CACHED", 0) == 1
        await asyncio.sleep(10)
        assert (await client.get_lol_v1_champion(id=777)).get("_CACHED", 0) == 0 # cache expired
