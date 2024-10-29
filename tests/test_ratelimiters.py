import asyncio
import os
import subprocess

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


RATELIMITER_PROXY_SCRIPT = (
    "from pulsefire.ratelimiters import RiotAPIRateLimiter;"
    "RiotAPIRateLimiter().serve()"
)

RATELIMITER_PROXY_SECRET_SCRIPT = (
    "from pulsefire.ratelimiters import RiotAPIRateLimiter;"
    "RiotAPIRateLimiter().serve(secret='sAmPLesECReT')"
)

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
        async with TaskGroup(asyncio.Semaphore(100)) as tg:
            for _ in range(70):
                await tg.create_task(client.get_lol_champion_v3_rotation(region="na1"))
        assert tg.results()


@async_to_sync()
async def test_riot_api_rate_limiter_proxy():
    popen = subprocess.Popen(f'python -c "{RATELIMITER_PROXY_SCRIPT}"', shell=os.name == "posix")
    try:
        await asyncio.sleep(1)

        async with RiotAPIClient(
            default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]},
            middlewares=[
                json_response_middleware(),
                http_error_middleware(),
                rate_limiter_middleware(RiotAPIRateLimiter(proxy="http://127.0.0.1:12227")),
            ]
        ) as client:
            await client.get_lol_champion_v3_rotation(region="na1")
            async with TaskGroup(asyncio.Semaphore(100)) as tg:
                for _ in range(2):
                    await tg.create_task(client.get_lol_champion_v3_rotation(region="na1"))
            assert tg.results()
    finally:
        popen.terminate()
        if os.name == "posix":
            subprocess.run("kill -9 $(sudo lsof -t -i:12227)", shell=True)


@async_to_sync()
async def test_riot_api_rate_limiter_proxy_secret():
    popen = subprocess.Popen(f'python -c "{RATELIMITER_PROXY_SECRET_SCRIPT}"', shell=os.name == "posix")
    try:
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
            async with TaskGroup(asyncio.Semaphore(100)) as tg:
                for _ in range(70):
                    await tg.create_task(client.get_lol_champion_v3_rotation(region="na1"))
            assert tg.results()

    finally:
        popen.terminate()
        if os.name == "posix":
            subprocess.run("kill -9 $(sudo lsof -t -i:12227)", shell=True)
