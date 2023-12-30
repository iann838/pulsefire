import asyncio
import os
import statistics
import sys

from pulsefire.clients import RiotAPIClient
from pulsefire.schemas import RiotAPISchema
from pulsefire.taskgroups import TaskGroup

REGION = "na1"
RIOT_API_KEY = os.environ["RIOT_API_KEY"]


async def get_last_20_winrate(summoner_name: str) -> float:
    """Returns a float representing the winrate of a given summoner, of the last 20 games they've played."""
    async with RiotAPIClient(default_headers={"X-Riot-Token": RIOT_API_KEY}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region=REGION, name=summoner_name)
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(
            region="americas", puuid=summoner["puuid"]
        )

        async with TaskGroup(asyncio.Semaphore(100)) as tg:
            for match_id in match_ids[:20]:
                await tg.create_task(client.get_lol_match_v5_match(region="americas", id=match_id))
        matches: list[RiotAPISchema.LolMatchV5Match] = tg.results()

    match_outcomes = []
    for match in matches:
        for participant in match["info"]["participants"]:
            if summoner["puuid"] == participant["puuid"]:
                match_outcomes.append(participant["win"])
    return statistics.mean(match_outcomes)


async def main():
    summoner_name = sys.argv[1]
    win_rate = await get_last_20_winrate(summoner_name)
    print(f"{summoner_name} has won {round(win_rate * 100)}% of their last 20 games.")

if __name__ == "__main__":
    asyncio.run(main())
