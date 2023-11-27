import os

from pulsefire.clients import RiotAPIClient
from pulsefire.functools import async_to_sync


client = RiotAPIClient(
    default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]},
)

@async_to_sync()
async def test_base_raw():
    summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
    assert summoner["name"] == "Not a Whale"
    assert summoner["summonerLevel"] > 200


@async_to_sync()
async def test_base_enter():
    async with client:
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        assert summoner["name"] == "Not a Whale"
        assert summoner["summonerLevel"] > 200


@async_to_sync()
@client
async def test_base_decorator_enter():
    summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
    assert summoner["name"] == "Not a Whale"
    assert summoner["summonerLevel"] > 200
