import asyncio
import os
import sys

from pulsefire.clients import RiotAPIClient

REGION = "na1"
RIOT_API_KEY = os.environ["RIOT_API_KEY"]


async def print_summoner_ranks(summoner_name: str) -> None:
    """Prints stats related to a given summoner's rank for each game mode, if any"""
    # Define client context
    async with RiotAPIClient(default_headers={"X-Riot-Token": RIOT_API_KEY}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region=REGION, name=summoner_name)
        league_entries = await client.get_lol_league_v4_entries_by_summoner(
            region=REGION, summoner_id=summoner["id"]
        )

    if not league_entries:
        return print(f"{summoner["name"]} is not yet ranked in any queue type.")

    for entry in league_entries:
        wins = entry["wins"]
        losses = entry["losses"]
        win_rate = f"{round(wins / (losses + wins) * 100)}%"
        queue_type = ""
        match entry["queueType"]:
            case "RANKED_SOLO_5x5":
                queue_type = "Solo/Duo"
            case "RANKED_FLEX_SR":
                queue_type = "Flex"
            case _ as unknown_type:
                queue_type = unknown_type

        # Output
        print(f"# {queue_type} #")
        print(f"{entry["tier"].title()} {entry["rank"]} ({entry["leaguePoints"]}lp)")
        print("Wins", wins)
        print("Losses", losses)
        print("Win rate", win_rate)


async def main():
    summoner_name = sys.argv[1]
    await print_summoner_ranks(summoner_name)


if __name__ == "__main__":
    asyncio.run(main())