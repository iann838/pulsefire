import os

import aiohttp
from pulsefire.clients import (
    CDragonClient,
    DDragonClient,
    MarlonAPIClient,
    MerakiCDNClient,
    RiotAPIClient,
)
from pulsefire.functools import async_to_sync


@async_to_sync()
async def test_cdragon_client():
    async with CDragonClient(default_params={"patch": "latest", "locale": "default"}) as client:
        await client.get_lol_champion_bin(key_lower="yone")
        await client.get_lol_v1_champion(id=777)
        await client.get_lol_v1_champion_summary()
        await client.get_lol_v1_items()
        await client.get_lol_v1_perks()
        await client.get_lol_v1_summoner_spells()
        await client.get_lol_v1_profile_icons()
        await client.get_tft_data(locale="en_us")


@async_to_sync()
async def test_ddragon_client():
    async with DDragonClient(default_params={"patch": "latest", "locale": "en_us"}) as client:
        await client.get_lor_cards(set=8)
        await client.get_lor_cards(patch="latest", locale="en_us", set=8)


@async_to_sync()
async def test_marlon_api_client():
    async with MarlonAPIClient() as client:
        agents = await client.get_val_v1_agents()
        await client.get_val_v1_agent(uuid=agents["data"][0]["uuid"])
        buddies = await client.get_val_v1_buddies()
        await client.get_val_v1_buddy(uuid=buddies["data"][0]["uuid"])
        bundles = await client.get_val_v1_bundles()
        await client.get_val_v1_bundle(uuid=bundles["data"][0]["uuid"])
        ceremonies = await client.get_val_v1_ceremonies()
        await client.get_val_v1_ceremony(uuid=ceremonies["data"][0]["uuid"])
        competitive_tiers = await client.get_val_v1_competitive_tiers()
        await client.get_val_v1_competitive_tier(uuid=competitive_tiers["data"][0]["uuid"])
        content_tiers = await client.get_val_v1_content_tiers()
        await client.get_val_v1_content_tier(uuid=content_tiers["data"][0]["uuid"])
        contracts = await client.get_val_v1_contracts()
        await client.get_val_v1_contract(uuid=contracts["data"][0]["uuid"])
        currencies = await client.get_val_v1_currencies()
        await client.get_val_v1_currency(uuid=currencies["data"][0]["uuid"])
        events = await client.get_val_v1_events()
        await client.get_val_v1_event(uuid=events["data"][0]["uuid"])
        gamemodes = await client.get_val_v1_gamemodes()
        await client.get_val_v1_gamemode(uuid=gamemodes["data"][0]["uuid"])
        gears = await client.get_val_v1_gears()
        await client.get_val_v1_gear(uuid=gears["data"][0]["uuid"])
        maps = await client.get_val_v1_maps()
        await client.get_val_v1_map(uuid=maps["data"][0]["uuid"])
        playercards = await client.get_val_v1_playercards()
        await client.get_val_v1_playercard(uuid=playercards["data"][0]["uuid"])
        playertitles = await client.get_val_v1_playertitles()
        await client.get_val_v1_playertitle(uuid=playertitles["data"][0]["uuid"])
        seasons = await client.get_val_v1_seasons()
        await client.get_val_v1_season(uuid=seasons["data"][0]["uuid"])
        sprays = await client.get_val_v1_sprays()
        await client.get_val_v1_spray(uuid=sprays["data"][0]["uuid"])
        themes = await client.get_val_v1_themes()
        await client.get_val_v1_theme(uuid=themes["data"][0]["uuid"])
        weapons = await client.get_val_v1_weapons()
        await client.get_val_v1_weapon(uuid=weapons["data"][0]["uuid"])
        await client.get_val_v1_version()


@async_to_sync()
async def test_maraki_cdn_client():
    async with MerakiCDNClient() as client:
        await client.get_lol_champions()
        await client.get_lol_champion(key="Yone")
        await client.get_lol_items()
        await client.get_lol_item(id=3031)


@async_to_sync()
async def test_acc_riot_api_client():    
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["PYOT_DEV_KEY"]}) as client:
        account = await client.get_account_v1_by_riot_id(region="americas", game_name="Not a Whale", tag_line="NA1")
        await client.get_account_v1_by_puuid(region="americas", puuid=account["puuid"])
        await client.get_account_v1_active_shard_by_puuid(region="americas", puuid=account["puuid"], game="val")


@async_to_sync()
async def test_lol_riot_api_client():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
        await client.get_lol_champion_v3_rotation(region="na1")
        plat_league = await client.get_lol_league_v4_entries_by_division(region="na1", queue="RANKED_SOLO_5x5", tier="PLATINUM", division="IV")
        summoner = await client.get_lol_summoner_v4_by_id(region="na1", id=plat_league[0]["summonerId"])
        masteries = await client.get_lol_champion_v4_masteries_by_summoner(region="na1", summoner_id=summoner["id"])
        await client.get_lol_champion_v4_mastery_by_summoner(region="na1", summoner_id=summoner["id"], champion_id=masteries[10]["championId"])
        # await client.get_lol_champion_v4_top_masteries_by_summoner(region="na1", summoner_id=summoner["id"])
        await client.get_lol_champion_v4_mastery_by_puuid(region="na1", puuid=summoner["puuid"], champion_id=masteries[10]["championId"])
        await client.get_lol_champion_v4_masteries_by_puuid(region="na1", puuid=summoner["puuid"])
        await client.get_lol_champion_v4_top_masteries_by_puuid(region="na1", puuid=summoner["puuid"])
        await client.get_lol_clash_v1_tournaments(region="na1")
        await client.get_lol_league_v4_entries_by_summoner(region="na1", summoner_id=summoner["id"])
        await client.get_lol_league_v4_challenger_league_by_queue(region="na1", queue="RANKED_SOLO_5x5")
        await client.get_lol_league_v4_grandmaster_league_by_queue(region="na1", queue="RANKED_SOLO_5x5")
        await client.get_lol_league_v4_master_league_by_queue(region="na1", queue="RANKED_SOLO_5x5")
        await client.get_lol_league_v4_entries_by_division(region="na1", queue="RANKED_SOLO_5x5", tier="EMERALD", division="IV", queries={"page": 10})
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])
        print(match_ids[0])
        await client.get_lol_match_v5_match(region="americas", id=match_ids[0])
        await client.get_lol_match_v5_match_timeline(region="americas", id=match_ids[0])
        featured_games = await client.get_lol_spectator_v4_featured_games(region="na1")
        await client.get_lol_spectator_v4_active_game_by_summoner(region="na1", summoner_id=featured_games["gameList"][0]["participants"][0]["summonerId"])
        await client.get_lol_status_v4_platform_data(region="na1")
        await client.get_lol_summoner_v4_by_id(region="na1", id=summoner["id"])
        await client.get_lol_summoner_v4_by_name(region="na1", name=summoner["name"])
        await client.get_lol_summoner_v4_by_puuid(region="na1", puuid=summoner["puuid"])


@async_to_sync()
async def test_tft_riot_api_client():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["TFT_API_KEY"]}) as client:
        plat_league = await client.get_tft_league_v1_entries_by_division(region="na1", tier="PLATINUM", division="IV")
        summoner = await client.get_tft_summoner_v1_by_id(region="na1", id=plat_league[0]["summonerId"])
        await client.get_tft_league_v1_entries_by_summoner(region="na1", summoner_id=summoner["id"])
        await client.get_tft_league_v1_challenger_league(region="na1")
        await client.get_tft_league_v1_grandmaster_league(region="na1")
        await client.get_tft_league_v1_master_league(region="na1", queries={"queue": "RANKED_TFT"})
        await client.get_tft_league_v1_entries_by_division(region="na1", tier="PLATINUM", division="IV", queries={"page": 10})
        match_ids = await client.get_tft_match_v1_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])
        await client.get_tft_match_v1_match(region="americas", id=match_ids[0])
        await client.get_tft_status_v1_platform_data(region="na1")
        await client.get_tft_summoner_v1_by_id(region="na1", id=summoner["id"])
        await client.get_tft_summoner_v1_by_name(region="na1", name=summoner["name"])
        await client.get_tft_summoner_v1_by_puuid(region="na1", puuid=summoner["puuid"])


@async_to_sync()
async def test_lor_riot_api_client():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["LOR_API_KEY"]}) as client:
        leaderboard = await client.get_lor_ranked_v1_leaderboard(region="americas")
        account = None
        for player in leaderboard["players"]:
            try:
                account = await client.get_account_v1_by_riot_id(region="americas", game_name=player["name"], tag_line="NA1")
                match_ids = await client.get_lor_match_v1_match_ids_by_puuid(region="americas", puuid=account["puuid"])
                if match_ids:
                    await client.get_lor_match_v1_match(region="americas", id=match_ids[0])
                    break
            except aiohttp.ClientResponseError:
                continue
        else:
            assert False, "Expected break"
        await client.get_lor_status_v1_platform_data(region="americas")


@async_to_sync()
async def test_val_riot_api_client():
    async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["PYOT_DEV_KEY"]}) as client:
        await client.get_val_content_v1_contents(region="na")
        contents = await client.get_val_content_v1_contents(region="na", queries={"locale": "en-US"})
        latest_act = next(act for act in reversed(contents["acts"]) if act["isActive"] and act["type"] == 'act')
        await client.get_val_ranked_v1_leaderboard_by_act(region="na", act_id=latest_act["id"])
        recent_spikerush_matches = await client.get_val_match_v1_recent_matches_by_queue(region="na", queue="spikerush")
        recent_deathmatch_matches = await client.get_val_match_v1_recent_matches_by_queue(region="na", queue="deathmatch")
        recent_competitive_matches = await client.get_val_match_v1_recent_matches_by_queue(region="na", queue="competitive")
        await client.get_val_match_v1_match(region="na", id=recent_spikerush_matches["matchIds"][0])
        await client.get_val_match_v1_match(region="na", id=recent_deathmatch_matches["matchIds"][0])
        match = await client.get_val_match_v1_match(region="na", id=recent_competitive_matches["matchIds"][0])
        await client.get_val_match_v1_matchlist_by_puuid(region="na", puuid=match["players"][0]["puuid"])
        await client.get_val_status_v1_platform_data(region="na")
