import os

from pulsefire.clients import RiotAPIClient
from pulsefire.functools import async_to_sync


@async_to_sync()
async def test_base_enter():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
        account = await client.get_account_v1_by_riot_id(region="americas", game_name="200", tag_line="16384")
        summoner = await client.get_lol_summoner_v4_by_puuid(region="na1", puuid=account["puuid"])
        assert account["gameName"] == "200"
        assert summoner["summonerLevel"] > 200
