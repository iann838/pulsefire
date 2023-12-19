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
        with timer() as get_t:
            await client.get_lol_v1_items()
        assert get_t() > 0.02
        with timer() as get_t:
            await client.get_lol_v1_items()
        assert get_t() < 0.002
        with timer() as get_t:
            await client.get_lol_v1_summoner_spells()
        assert get_t() > 0.02
        with timer() as get_t:
            await client.get_lol_v1_summoner_spells()
        assert get_t() < 0.002
        with timer() as get_t:
            await client.get_lol_v1_summoner_spells()
        assert get_t() < 0.002
        with timer() as get_t:
            await client.get_lol_v1_champion(id=777)
        assert get_t() > 0.02
        with timer() as get_t:
            await client.get_lol_v1_champion(id=777)
        assert get_t() < 0.002
        await asyncio.sleep(10)
        with timer() as get_t:
            await client.get_lol_v1_champion(id=777)
        assert get_t() > 0.02


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
        with timer() as get_t:
            await client.get_lol_v1_items()
        assert get_t() > 0.02
        with timer() as get_t:
            await client.get_lol_v1_items()
        assert get_t() < 0.015
        with timer() as get_t:
            await client.get_lol_v1_summoner_spells()
        assert get_t() > 0.02
        with timer() as get_t:
            await client.get_lol_v1_summoner_spells()
        assert get_t() < 0.002
        with timer() as get_t:
            await client.get_lol_v1_summoner_spells()
        assert get_t() < 0.002
        with timer() as get_t:
            await client.get_lol_v1_champion(id=777)
        assert get_t() > 0.02

        with timer() as get_t:
            await client.get_lol_v1_champion(id=777)
        assert get_t() < 0.002
        await asyncio.sleep(10)
        with timer() as get_t:
            await client.get_lol_v1_champion(id=777)
        assert get_t() > 0.02
