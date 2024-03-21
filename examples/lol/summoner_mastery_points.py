import asyncio
import os
import sys

from pulsefire.clients import CDragonClient, RiotAPIClient

REGION = "na1"
RIOT_API_KEY = os.environ["RIOT_API_KEY"]


async def summoner_mastery_points(summoner_name: str) -> list[tuple[str, int]]:
    """Returns a list of pairs, each having a champion name and how many mastery points the summoner earned"""
    async with CDragonClient(default_params={"patch": "latest", "locale": "default"}) as client:
        champions = await client.get_lol_v1_champion_summary()
        champion_id_to_names = {champion["id"]: champion["name"] for champion in champions}

    async with RiotAPIClient(default_headers={"X-Riot-Token": RIOT_API_KEY}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region=REGION, name=summoner_name)
        mastery_points = await client.get_lol_champion_v4_masteries_by_puuid(
            region=REGION, puuid=summoner["puuid"]
        )

    return [
        (champion_id_to_names[champ_mastery_stats["championId"]], champ_mastery_stats["championPoints"])
        for champ_mastery_stats in mastery_points
    ]


async def main():
    summoner_name = sys.argv[1]
    mastery_points = await summoner_mastery_points(summoner_name)
    print(mastery_points)

if __name__ == "__main__":
    asyncio.run(main())
