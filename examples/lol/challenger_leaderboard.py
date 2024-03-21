import asyncio
import operator
import os

from pulsefire.clients import RiotAPIClient

REGION = "na1"
RIOT_API_KEY = os.environ["RIOT_API_KEY"]


async def get_challenger_leaderboard_top_10():
    """Print the top 10 summoners + LP"""
    async with RiotAPIClient(default_headers={"X-Riot-Token": RIOT_API_KEY}) as client:
        challenger_league = await client.get_lol_league_v4_challenger_league_by_queue(
            queue="RANKED_SOLO_5x5", region=REGION
        )

    challenger_summoners = sorted(
        challenger_league["entries"],
        key=operator.itemgetter("leaguePoints"),  # Sort by league points
        reverse=True,  # Sort in descending order
    )
    top_10_challenger_summoners = challenger_summoners[:10]

    # Output
    print("Top 10 challenger players!\n")
    longest_name = max([len(summoner["summonerName"]) for summoner in top_10_challenger_summoners])
    for indx, summoner in enumerate(top_10_challenger_summoners):
        name = summoner["summonerName"]
        lp = summoner["leaguePoints"]
        print(f"{indx + 1:02d}. {name:<{longest_name}} ({lp:,d} lp)")


async def main():
    await get_challenger_leaderboard_top_10()

if __name__ == "__main__":
    asyncio.run(main())
