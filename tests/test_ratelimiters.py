import asyncio
import os
import subprocess
import time

import aiohttp

from pulsefire.clients import RiotAPIClient
from pulsefire.functools import async_to_sync
from pulsefire.middlewares import (
    json_response_middleware,
    http_error_middleware,
    rate_limiter_middleware
)
from pulsefire.ratelimiters import RiotAPIRateLimiter
from pulsefire.taskgroups import TaskGroup


@async_to_sync()
async def test_riot_api_rate_limiter_local():
    async with RiotAPIClient(
        default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]},
        middlewares=[
            json_response_middleware(),
            http_error_middleware(),
            rate_limiter_middleware(RiotAPIRateLimiter()),
        ]
    ) as client:
        start_time = time.time()
        async with TaskGroup(asyncio.Semaphore(100)) as tg:
            for _ in range(70):
                await tg.create_task(client.get_lol_champion_v3_rotation(region="na1"))
        assert 20 <= time.time() - start_time < 25


@async_to_sync()
async def test_riot_api_rate_limiter_proxy():
    popen = subprocess.Popen(
        'python -c "' +
        'from pulsefire.ratelimiters import RiotAPIRateLimiter;' +
        'RiotAPIRateLimiter().serve()' +
        '"'
    )

    async with RiotAPIClient(
        default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]},
        middlewares=[
            json_response_middleware(),
            http_error_middleware(),
            rate_limiter_middleware(RiotAPIRateLimiter(proxy="http://127.0.0.1:12227")),
        ]
    ) as client:
        start_time = time.time()
        async with TaskGroup(asyncio.Semaphore(100)) as tg:
            for _ in range(70):
                await tg.create_task(client.get_lol_champion_v3_rotation(region="na1"))
        assert 20 <= time.time() - start_time < 25

    popen.kill()


@async_to_sync()
async def test_riot_api_rate_limiter_proxy_secret():
    popen = subprocess.Popen(
        'python -c "' +
        'from pulsefire.ratelimiters import RiotAPIRateLimiter;' +
        'RiotAPIRateLimiter().serve(secret=\'sAmPLesECReT\')' +
        '"'
    )
    await asyncio.sleep(1)

    async with RiotAPIClient(
        default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]},
        middlewares=[
            json_response_middleware(),
            http_error_middleware(),
            rate_limiter_middleware(RiotAPIRateLimiter(
                proxy="http://127.0.0.1:12227",
                proxy_secret="WRONGsECReT"
            )),
        ]
    ) as client:
        try:
            await client.get_lol_champion_v3_rotation(region="na1")
            assert False, "Expected exception"
        except aiohttp.ClientResponseError as e:
            assert e.status == 401

    async with RiotAPIClient(
        default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]},
        middlewares=[
            json_response_middleware(),
            http_error_middleware(),
            rate_limiter_middleware(RiotAPIRateLimiter(
                proxy="http://127.0.0.1:12227",
                proxy_secret="sAmPLesECReT"
            )),
        ]
    ) as client:
        start_time = time.time()
        async with TaskGroup(asyncio.Semaphore(100)) as tg:
            for _ in range(70):
                await tg.create_task(client.get_lol_champion_v3_rotation(region="na1"))
        assert 20 <= time.time() - start_time < 25

    popen.kill()
