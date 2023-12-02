import asyncio
import os

from pulsefire.clients import RiotAPIClient
from pulsefire.functools import async_to_sync
from pulsefire.schemas import RiotAPISchema


@async_to_sync()
async def test_concurrent_request_alt2():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        tasks: list[asyncio.Task] = []
        async with asyncio.TaskGroup() as tg:
            for match_id in match_ids[:20]:
                tasks.append(tg.create_task(client.get_lol_match_v5_match(region="americas", id=match_id)))
        matches: list[RiotAPISchema.LolMatchV5Match] = [task.result() for task in tasks]

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids


@async_to_sync()
async def test_concurrent_request_alt3():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        matches: list[RiotAPISchema.LolMatchV5Match] = await asyncio.gather(*[
            client.get_lol_match_v5_match(region="americas", id=match_id)
            for match_id in match_ids[:20]
        ])

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids
