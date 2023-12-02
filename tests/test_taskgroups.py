import asyncio
import os

from pulsefire.clients import RiotAPIClient
from pulsefire.functools import async_to_sync
from pulsefire.schemas import RiotAPISchema
from pulsefire.taskgroups import TaskGroup


@async_to_sync()
async def test_taskgroup():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
        plat_league = await client.get_lol_league_v4_entries_by_division(region="na1", queue="RANKED_SOLO_5x5", tier="PLATINUM", division="IV")
        summoner = await client.get_lol_summoner_v4_by_id(region="na1", id=plat_league[0]["summonerId"])
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        async with TaskGroup() as tg:
            for match_id in match_ids[:20]:
                await tg.create_task(client.get_lol_match_v5_match(region="americas", id=match_id))
        matches: list[RiotAPISchema.LolMatchV5Match] = tg.results()

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids


@async_to_sync()
async def test_taskgroup_semaphore():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
        plat_league = await client.get_lol_league_v4_entries_by_division(region="na1", queue="RANKED_SOLO_5x5", tier="PLATINUM", division="IV")
        summoner = await client.get_lol_summoner_v4_by_id(region="na1", id=plat_league[0]["summonerId"])
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        async with TaskGroup(asyncio.Semaphore(100)) as tg:
            for match_id in match_ids[:20]:
                await tg.create_task(client.get_lol_match_v5_match(region="americas", id=match_id))
        matches: list[RiotAPISchema.LolMatchV5Match] = tg.results()

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids
