import asyncio
import os
import sys

from pulsefire.clients import CDragonClient

REGION = "na1"
RIOT_API_KEY = os.environ["RIOT_API_KEY"]

async def get_champion_id_by_name(champion_name: str) -> int:
    async with CDragonClient(default_params={"patch": "latest", "locale": "default"}) as client:
        champions = await client.get_lol_v1_champion_summary()

    champion_ids = {champion["name"]: champion["id"] for champion in champions}
    for champ in champion_ids.keys():
        if champion_name.lower() in champ.lower():
            return champion_ids[champ]
    raise KeyError(f"{champion_name} was not found in the champion pool.")

async def get_champion_abilities(champion_id: int):
    """Print out the abilities of a given champion"""
    async with CDragonClient(default_params={"patch": "latest", "locale": "default"}) as client:
        champion = await client.get_lol_v1_champion(id=champion_id)

    print("Champion name:", champion["name"])
    print(f"(P) {champion["passive"]["name"]}")
    print(champion["passive"]['description'])
    for spell in champion["spells"]:
        print(f"({spell["spellKey"].upper()}) {spell["name"]}")
        print(spell["description"])


async def main():
    champion_name = sys.argv[1]
    champion_id = await get_champion_id_by_name(champion_name)
    await get_champion_abilities(champion_id)

if __name__ == "__main__":
    asyncio.run(main())
