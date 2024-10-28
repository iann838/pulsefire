"""Module for pulsefire clients.

This module contains clients to APIs and resources in the Riot Games ecosystem.
"""
from typing import Any, Literal, TypedDict, Sequence
from types import MethodType
import abc
import asyncio
import functools
import inspect
import itertools
import sys

import aiohttp

from .middlewares import (
    http_error_middleware,
    json_response_middleware,
    rate_limiter_middleware,
)
from .ratelimiters import RiotAPIRateLimiter
from .schemas import (
    CDragonSchema,
    DDragonSchema,
    MerakiCDNSchema,
    RiotAPISchema,
    MarlonAPISchema
)
from .invocation import HttpMethod, Invocation
from .middlewares import Middleware


type _str = Sequence[str]


class BaseClient(abc.ABC):
    """Base client class.

    Inherit from this class to implement a client.
    """

    base_url: str
    """Base URL, can be extended by `invoke`."""
    default_headers: dict[str, str]
    """Default params (ignores `...`), can be overwritten by `invoke`."""
    default_params: dict[str, Any]
    """Default header params, can be overwritten by `invoke`."""
    default_queries: dict[str, str]
    """Default query params, can be overwritten by `invoke`."""
    middlewares: list[Middleware]
    """Pre and post processors during `invoke`."""
    session: aiohttp.ClientSession | None = None
    """Context manager client session."""

    def __init__(
        self,
        *,
        base_url: str,
        default_params: dict[str, Any] = {},
        default_headers: dict[str, str] = {},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [],
    ) -> None:
        self.base_url = base_url
        self.default_headers = default_headers
        self.default_params = default_params
        self.default_queries = default_queries
        self.middlewares = middlewares
        async def run_invocation(invocation: Invocation):
            return await invocation()
        self.middleware_begin = run_invocation
        for middleware in middlewares[::-1]:
            self.middleware_begin = middleware(self.middleware_begin)
            if not inspect.iscoroutinefunction(self.middleware_begin):
                raise TypeError(f"{self.middleware_begin} is not a coroutine function")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={id(self)}>"

    async def __aenter__(self):
        """Context manager, in-context invocations will reuse a single `aiohttp.ClientSession`
        improving performance and memory footprint.

        Raises:
            RuntimeError: When entering an already entered client.
        """
        if self.session:
            raise RuntimeError(f"{self!r} has been already entered")
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *_) -> None:
        transports = 0
        transports_closed = asyncio.Event()

        def connection_lost(exc, orig_lost):
            nonlocal transports
            try:
                orig_lost(exc)
            finally:
                transports -= 1
                if transports == 0:
                    transports_closed.set()

        def eof_received(orig_eof_received):
            try:
                orig_eof_received()
            except AttributeError:
                pass

        for conn in self.session.connector._conns.values():
            for handler, _ in conn:
                proto: asyncio.Protocol = getattr(handler.transport, "_ssl_protocol", None)
                if proto is None:
                    continue
                transports += 1
                orig_lost = proto.connection_lost
                orig_eof_received = proto.eof_received
                proto.connection_lost = functools.partial(
                    connection_lost, orig_lost=orig_lost
                )
                proto.eof_received = functools.partial(
                    eof_received, orig_eof_received=orig_eof_received
                )
        if transports == 0:
            transports_closed.set()

        await self.session.close()
        await transports_closed.wait()
        self.session = None

    async def invoke(self, method: HttpMethod, path_or_url: str):
        """Build an Invocation and send through the middlewares.

        Params are automatically grabbed from the outer frame (ignores `...`).
        The invoker client method is automatically grabbed from the outer frame
        and passed to the instantiation of Invocation.
        """
        params = {}
        for key, value in itertools.chain(self.default_params.items(), sys._getframe(1).f_locals.items()):
            if key != "self" and value != ...:
                params[key] = value
        params["queries"] = {**self.default_queries, **params.get("queries", {})}
        params["headers"] = {**self.default_headers, **params.get("headers", {})}
        invoker: MethodType | None = getattr(self, sys._getframe(1).f_code.co_name, None)
        invocation = Invocation(method, self.base_url + path_or_url, params, self.session, invoker=invoker)
        return await self.middleware_begin(invocation)


class CDragonClient(BaseClient):
    """Community Dragon Client.

    | Resources            | Support                    |
    | -------------------- | -------------------------- |
    | League of Legends    | ✅                         |
    | Legends of Runeterra | ❎ Use DDragon instead.    |
    | Teamfight Tactics    | ✅                         |
    | Valorant             | ❎                         |

    Example:
    ```python
    async with CDragonClient(
        default_params={"patch": "latest", "locale": "default"}
    ) as client:
        champion = await client.get_lol_v1_champion(id=777)
        assert champion["name"] == "Yone"
    ```
    """

    Patch = Literal["latest", "pbe"] | _str
    Locale = Literal[
        "default", "ar_ae", "cs_cz", "de_de", "el_gr", "en_au", "en_gb", "en_ph", "en_sg", "en_us",
        "es_ar", "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br",
        "ro_ro", "ru_ru", "th_th", "tr_tr", "vi_vn", "vn_vn", "zh_cn", "zh_my", "zh_tw",
    ] | _str

    def __init__(
        self,
        *,
        base_url: str = "https://raw.communitydragon.org",
        default_params: dict[str, Any] = {"patch": ..., "locale": ...},
        default_headers: dict[str, str] = {},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [
            json_response_middleware(),
            http_error_middleware(),
        ],
    ) -> None:
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            default_queries=default_queries,
            middlewares=middlewares
        )

    async def get_lol_champion_bin(self, *, patch: Patch = ..., key_lower: str = ...) -> dict[str, CDragonSchema.LolChampionBinValue]:
        return await self.invoke("GET", "/{patch}/game/data/characters/{key_lower}/{key_lower}.bin.json")

    async def get_lol_v1_champion(self, *, patch: Patch = ..., locale: Locale = ..., id: int = ...) -> CDragonSchema.LolV1Champion:
        return await self.invoke("GET", "/{patch}/plugins/rcp-be-lol-game-data/global/{locale}/v1/champions/{id}.json")

    async def get_lol_v1_champion_summary(self, *, patch: Patch = ..., locale: Locale = ...) -> list[CDragonSchema.LolV1ChampionInfo]:
        return await self.invoke("GET", "/{patch}/plugins/rcp-be-lol-game-data/global/{locale}/v1/champion-summary.json")

    async def get_lol_v1_items(self, *, patch: Patch = ..., locale: Locale = ...) -> list[CDragonSchema.LolV1Item]:
        return await self.invoke("GET", "/{patch}/plugins/rcp-be-lol-game-data/global/{locale}/v1/items.json")

    async def get_lol_v1_perks(self, *, patch: Patch = ..., locale: Locale = ...) -> list[CDragonSchema.LolV1Perk]:
        return await self.invoke("GET", "/{patch}/plugins/rcp-be-lol-game-data/global/{locale}/v1/perks.json")

    async def get_lol_v1_summoner_spells(self, *, patch: Patch = ..., locale: Locale = ...) -> list[CDragonSchema.LolV1SummonerSpell]:
        return await self.invoke("GET", "/{patch}/plugins/rcp-be-lol-game-data/global/{locale}/v1/summoner-spells.json")

    async def get_lol_v1_profile_icons(self, *, patch: Patch = ..., locale: Locale = ...) -> list[CDragonSchema.LolV1ProfileIcon]:
        return await self.invoke("GET", "/{patch}/plugins/rcp-be-lol-game-data/global/{locale}/v1/profile-icons.json")

    async def get_tft_data(self, *, patch: Patch = ..., locale: Locale = ...) -> CDragonSchema.TftData:
        return await self.invoke("GET", "/{patch}/cdragon/tft/{locale}.json")


class DDragonClient(BaseClient):
    """Data Dragon Client.

    | Resources            | Support                    |
    | -------------------- | -------------------------- |
    | League of Legends    | ❎ Use CDragon instead.    |
    | Teamfight Tactics    | ❎                         |
    | Legends of Runeterra | ✅                         |
    | Valorant             | ❎                         |

    Example:
    ```python
    async with DDragonClient(
        default_params={"patch": "latest", "locale": "en_us"}
    ) as client:
        cards = await client.get_lor_cards(set=8)
        assert cards[0]["cardCode"]
    ```
    """

    Patch = Literal["latest"] | _str
    Locale = Literal[
        "ar_ae", "cs_cz", "de_de", "el_gr", "en_au", "en_gb", "en_ph", "en_sg", "en_us",
        "es_ar", "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br",
        "ro_ro", "ru_ru", "th_th", "tr_tr", "vi_vn", "vn_vn", "zh_cn", "zh_my", "zh_tw",
    ] | _str

    def __init__(
        self,
        *,
        base_url: str = "https://dd.b.pvp.net",
        default_params: dict[str, Any] = {"patch": ..., "locale": ...},
        default_headers: dict[str, str] = {},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [
            json_response_middleware(),
            http_error_middleware(),
        ],
    ) -> None:
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            default_queries=default_queries,
            middlewares=middlewares
        )

    async def get_lor_cards(self, *, patch: Patch = ..., locale: Locale = ..., set: str | int = ...) -> list[DDragonSchema.LorCard]:
        return await self.invoke("GET", "/{patch}/set{set}/{locale}/data/set{set}-{locale}.json")


class MerakiCDNClient(BaseClient):
    """Meraki CDN Client.

    | Resources            | Support                    |
    | -------------------- | -------------------------- |
    | League of Legends    | ✅                         |
    | Legends of Runeterra | ❎                         |
    | Teamfight Tactics    | ❎                         |
    | Valorant             | ❎                         |

    Does not support versioning by patch.

    Example:
    ```python
    async with MerakiCDNClient() as client:
        champion = await client.get_lol_champion(key="Yone")
        assert champion["id"] == 777
    ```
    """

    def __init__(
        self,
        *,
        base_url: str = "https://cdn.merakianalytics.com/riot",
        default_params: dict[str, Any] = {},
        default_headers: dict[str, str] = {},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [
            json_response_middleware(),
            http_error_middleware(),
        ],
    ) -> None:
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            default_queries=default_queries,
            middlewares=middlewares
        )

    async def get_lol_champions(self) -> dict[str, MerakiCDNSchema.LolChampion]:
        return await self.invoke("GET", "/lol/resources/latest/en-US/champions.json")

    async def get_lol_champion(self, *, key: str = ...) -> MerakiCDNSchema.LolChampion:
        return await self.invoke("GET", "/lol/resources/latest/en-US/champions/{key}.json")

    async def get_lol_items(self) -> dict[str, MerakiCDNSchema.LolItem]:
        return await self.invoke("GET", "/lol/resources/latest/en-US/items.json")

    async def get_lol_item(self, *, id: int = ...) -> MerakiCDNSchema.LolItem:
        return await self.invoke("GET", "/lol/resources/latest/en-US/items/{id}.json")
    
    async def get_lol_champion_rates(self) -> MerakiCDNSchema.LolChampionRates:
        return await self.invoke("GET", "/lol/resources/latest/en-US/championrates.json")


class RiotAPIClient(BaseClient):
    """Riot API Client.

    | Resources            | Support                    |
    | -------------------- | -------------------------- |
    | League of Legends    | ✅                         |
    | Legends of Runeterra | ✅                         |
    | Teamfight Tactics    | ✅                         |
    | Valorant             | ✅                         |

    Example:
    ```python
    async with RiotAPIClient(
        default_headers={"X-Riot-Token": <API_KEY>}
    ) as client:
        account = await client.get_account_v1_by_riot_id(region="americas", game_name="200", tag_line="16384")
        summoner = await client.get_lol_summoner_v4_by_puuid(region="na1", puuid=account["puuid"])
        assert summoner["summonerLevel"] > 200
    ```
    """

    Region = Literal[
        "americas", "europe", "asia", "sea", "esports",
        "br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "me1",
        "na1", "oc1", "tr1", "ru", "ph2", "sg2", "th2", "tw2", "vn2",
        "ap", "br", "eu", "kr", "latam", "na",
    ] | _str

    def __init__(
        self,
        *,
        base_url: str = "https://{region}.api.riotgames.com",
        default_params: dict[str, Any] = {},
        default_headers: dict[str, str] = {"X-Riot-Token": ""},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [
            json_response_middleware(),
            http_error_middleware(),
            rate_limiter_middleware(RiotAPIRateLimiter()),
        ],
    ) -> None:
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            default_queries=default_queries,
            middlewares=middlewares
        )

    # Account Endpoints

    async def get_account_v1_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> RiotAPISchema.AccountV1Account:
        return await self.invoke("GET", "/riot/account/v1/accounts/by-puuid/{puuid}")

    async def get_account_v1_by_riot_id(self, *, region: Region = ..., game_name: str = ..., tag_line: str = ...) -> RiotAPISchema.AccountV1Account:
        return await self.invoke("GET", "/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}")

    async def get_account_v1_me(self, *, region: Region = ..., headers: dict = {"Authorization": ""}) -> RiotAPISchema.AccountV1Account:
        return await self.invoke("GET", "/riot/account/v1/accounts/me")

    async def get_account_v1_active_shard_by_puuid(self, *, region: Region = ..., puuid: str = ..., game: str = ...) -> RiotAPISchema.AccountV1ActiveShard:
        return await self.invoke("GET", "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}")

    # League of Legends Endpoints

    async def get_lol_champion_v3_rotation(self, *, region: Region = ...) -> RiotAPISchema.LolChampionV3Rotation:
        return await self.invoke("GET", "/lol/platform/v3/champion-rotations")

    async def get_lol_champion_v4_mastery_by_summoner(self, *, region: Region = ..., summoner_id: str = ..., champion_id: int = ...) -> RiotAPISchema.LolChampionV4Mastery:
        return await self.invoke("GET", "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}")

    async def get_lol_champion_v4_masteries_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> list[RiotAPISchema.LolChampionV4Mastery]:
        return await self.invoke("GET", "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}")

    async def get_lol_champion_v4_top_masteries_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> list[RiotAPISchema.LolChampionV4Mastery]:
        return await self.invoke("GET", "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/top")

    async def get_lol_champion_v4_mastery_score_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> int:
        return await self.invoke("GET", "/lol/champion-mastery/v4/scores/by-summoner/{summoner_id}")

    async def get_lol_champion_v4_mastery_by_puuid(self, *, region: Region = ..., puuid: str = ..., champion_id: int = ...) -> RiotAPISchema.LolChampionV4Mastery:
        return await self.invoke("GET", "/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}")

    async def get_lol_champion_v4_masteries_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> list[RiotAPISchema.LolChampionV4Mastery]:
        return await self.invoke("GET", "/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}")

    async def get_lol_champion_v4_top_masteries_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> list[RiotAPISchema.LolChampionV4Mastery]:
        return await self.invoke("GET", "/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top")

    async def get_lol_champion_v4_mastery_score_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> int:
        return await self.invoke("GET", "/lol/champion-mastery/v4/scores/by-puuid/{puuid}")

    async def get_lol_clash_v1_players_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> list[RiotAPISchema.LolClashV1Player]:
        return await self.invoke("GET", "/lol/clash/v1/players/by-summoner/{summoner_id}")

    async def get_lol_clash_v1_players_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> list[RiotAPISchema.LolClashV1Player]:
        return await self.invoke("GET", "/lol/clash/v1/players/by-puuid/{puuid}")

    async def get_lol_clash_v1_team(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LolClashV1Team:
        return await self.invoke("GET", "/lol/clash/v1/teams/{id}")

    async def get_lol_clash_v1_tournament_by_team(self, *, region: Region = ..., team_id: str = ...) -> RiotAPISchema.LolClashV1Tournament:
        return await self.invoke("GET", "/lol/clash/v1/tournaments/by-team/{team_id}")

    async def get_lol_clash_v1_tournament(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LolClashV1Tournament:
        return await self.invoke("GET", "/lol/clash/v1/tournaments/{id}")

    async def get_lol_clash_v1_tournaments(self, *, region: Region = ...) -> list[RiotAPISchema.LolClashV1Tournament]:
        return await self.invoke("GET", "/lol/clash/v1/tournaments")

    async def get_lol_league_v4_entries_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> list[RiotAPISchema.LolLeagueV4LeagueFullEntry]:
        return await self.invoke("GET", "/lol/league/v4/entries/by-summoner/{summoner_id}")

    async def get_lol_league_v4_challenger_league_by_queue(self, *, region: Region = ..., queue: str = ...) -> RiotAPISchema.LolLeagueV4League:
        return await self.invoke("GET", "/lol/league/v4/challengerleagues/by-queue/{queue}")

    async def get_lol_league_v4_grandmaster_league_by_queue(self, *, region: Region = ..., queue: str = ...) -> RiotAPISchema.LolLeagueV4League:
        return await self.invoke("GET", "/lol/league/v4/grandmasterleagues/by-queue/{queue}")

    async def get_lol_league_v4_master_league_by_queue(self, *, region: Region = ..., queue: str = ...) -> RiotAPISchema.LolLeagueV4League:
        return await self.invoke("GET", "/lol/league/v4/masterleagues/by-queue/{queue}")

    async def get_lol_league_v4_entries_by_division(
        self, *, region: Region = ..., queue: str = ..., tier: str = ..., division: str = ..., queries: dict = {"page": 1}
    ) -> list[RiotAPISchema.LolLeagueV4LeagueFullEntry]:
        return await self.invoke("GET", "/lol/league/v4/entries/{queue}/{tier}/{division}")

    async def get_lol_league_v4_league(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LolLeagueV4League:
        return await self.invoke("GET", "/lol/league/v4/leagues/{id}")

    async def get_lol_match_v5_match(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LolMatchV5Match:
        return await self.invoke("GET", "/lol/match/v5/matches/{id}")

    async def get_lol_match_v5_match_timeline(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LolMatchV5MatchTimeline:
        return await self.invoke("GET", "/lol/match/v5/matches/{id}/timeline")

    async def get_lol_match_v5_match_ids_by_puuid(self, *, region: Region = ..., puuid: str = ..., queries: dict = {"start": 0, "count": 100}) -> list[str]:
        return await self.invoke("GET", "/lol/match/v5/matches/by-puuid/{puuid}/ids")

    async def get_lol_spectator_v4_active_game_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> RiotAPISchema.LolSpectatorV4Game:
        return await self.invoke("GET", "/lol/spectator/v4/active-games/by-summoner/{summoner_id}")

    async def get_lol_spectator_v4_featured_games(self, *, region: Region = ...) -> RiotAPISchema.LolSpectatorV4GameList:
        return await self.invoke("GET", "/lol/spectator/v4/featured-games")

    async def get_lol_spectator_v5_active_game_by_summoner(self, *, region: Region = ..., puuid: str = ...) -> RiotAPISchema.LolSpectatorV5Game:
        return await self.invoke("GET", "/lol/spectator/v5/active-games/by-summoner/{puuid}")

    async def get_lol_spectator_v5_featured_games(self, *, region: Region = ...) -> RiotAPISchema.LolSpectatorV5GameList:
        return await self.invoke("GET", "/lol/spectator/v5/featured-games")

    async def get_lol_status_v4_platform_data(self, *, region: Region = ...) -> RiotAPISchema.StatusV1PlatformData:
        return await self.invoke("GET", "/lol/status/v4/platform-data")

    async def get_lol_summoner_v4_by_id(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LolSummonerV4Summoner:
        return await self.invoke("GET", "/lol/summoner/v4/summoners/{id}")

    async def get_lol_summoner_v4_by_name(self, *, region: Region = ..., name: str = ...) -> RiotAPISchema.LolSummonerV4Summoner:
        return await self.invoke("GET", "/lol/summoner/v4/summoners/by-name/{name}")

    async def get_lol_summoner_v4_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> RiotAPISchema.LolSummonerV4Summoner:
        return await self.invoke("GET", "/lol/summoner/v4/summoners/by-puuid/{puuid}")

    async def get_lol_summoner_v4_me(self, *, region: Region = ..., headers: dict = {"Authorization": ""}) -> RiotAPISchema.LolSummonerV4Summoner:
        return await self.invoke("GET", "/lol/summoner/v4/summoners/me")

    async def get_lol_summoner_v4_by_rso_puuid(self, *, region: Region = ..., rso_puuid: str = ...) -> RiotAPISchema.LolSummonerV4Summoner:
        return await self.invoke("GET", "/fulfillment/v1/summoners/by-puuid/{rso_puuid}")

    # Teamfight Tactics Endpoints

    async def get_tft_league_v1_entries_by_summoner(self, *, region: Region = ..., summoner_id: str = ...) -> list[RiotAPISchema.TftLeagueV1LeagueFullEntry]:
        return await self.invoke("GET", "/tft/league/v1/entries/by-summoner/{summoner_id}")

    async def get_tft_league_v1_challenger_league(self, *, region: Region = ..., queries: dict = {}) -> RiotAPISchema.TftLeagueV1League:
        return await self.invoke("GET", "/tft/league/v1/challenger")

    async def get_tft_league_v1_grandmaster_league(self, *, region: Region = ..., queries: dict = {}) -> RiotAPISchema.TftLeagueV1League:
        return await self.invoke("GET", "/tft/league/v1/grandmaster")

    async def get_tft_league_v1_master_league(self, *, region: Region = ..., queries: dict = {}) -> RiotAPISchema.TftLeagueV1League:
        return await self.invoke("GET", "/tft/league/v1/master")

    async def get_tft_league_v1_entries_by_division(
        self, *, region: Region = ..., tier: str = ..., division: str = ..., queries: dict = {"page": 1}
    ) -> list[RiotAPISchema.TftLeagueV1LeagueFullEntry]:
        return await self.invoke("GET", "/tft/league/v1/entries/{tier}/{division}")

    async def get_tft_league_v1_league(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.TftLeagueV1League:
        return await self.invoke("GET", "/tft/league/v1/leagues/{id}")

    async def get_tft_match_v1_match(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.TftMatchV1Match:
        return await self.invoke("GET", "/tft/match/v1/matches/{id}")

    async def get_tft_match_v1_match_ids_by_puuid(self, *, region: Region = ..., puuid: str = ..., queries: dict = {"start": 0, "count": 100}) -> list[str]:
        return await self.invoke("GET", "/tft/match/v1/matches/by-puuid/{puuid}/ids")

    async def get_tft_status_v1_platform_data(self, *, region: Region = ...) -> RiotAPISchema.StatusV1PlatformData:
        return await self.invoke("GET", "/tft/status/v1/platform-data")

    async def get_tft_summoner_v1_by_id(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.TftSummonerV1Summoner:
        return await self.invoke("GET", "/tft/summoner/v1/summoners/{id}")

    async def get_tft_summoner_v1_by_name(self, *, region: Region = ..., name: str = ...) -> RiotAPISchema.TftSummonerV1Summoner:
        return await self.invoke("GET", "/tft/summoner/v1/summoners/by-name/{name}")

    async def get_tft_summoner_v1_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> RiotAPISchema.TftSummonerV1Summoner:
        return await self.invoke("GET", "/tft/summoner/v1/summoners/by-puuid/{puuid}")

    async def get_tft_summoner_v1_me(self, *, region: Region = ..., headers: dict = {"Authorization": ""}) -> RiotAPISchema.TftSummonerV1Summoner:
        return await self.invoke("GET", "/tft/summoner/v1/summoners/me")

    # Legends of Runeterra Endpoints

    async def get_lor_ranked_v1_leaderboard(self, *, region: Region = ...) -> RiotAPISchema.LorRankedV1Leaderboard:
        return await self.invoke("GET", "/lor/ranked/v1/leaderboards")

    async def get_lor_match_v1_match(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.LorMatchV1Match:
        return await self.invoke("GET", "/lor/match/v1/matches/{id}")

    async def get_lor_match_v1_match_ids_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> list[str]:
        return await self.invoke("GET", "/lor/match/v1/matches/by-puuid/{puuid}/ids")

    async def get_lor_status_v1_platform_data(self, *, region: Region = ...) -> RiotAPISchema.StatusV1PlatformData:
        return await self.invoke("GET", "/lor/status/v1/platform-data")

    # Valorant Endpoints

    async def get_val_content_v1_contents(self, *, region: Region = ..., queries: dict = {}) -> RiotAPISchema.ValContentV1Contents:
        return await self.invoke("GET", "/val/content/v1/contents")

    async def get_val_ranked_v1_leaderboard_by_act(self, *, region: Region = ..., act_id: str = ...) -> RiotAPISchema.ValRankedV1Leaderboard:
        return await self.invoke("GET", "/val/ranked/v1/leaderboards/by-act/{act_id}")

    async def get_val_match_v1_match(self, *, region: Region = ..., id: str = ...) -> RiotAPISchema.ValMatchV1Match:
        return await self.invoke("GET", "/val/match/v1/matches/{id}")

    async def get_val_match_v1_matchlist_by_puuid(self, *, region: Region = ..., puuid: str = ...) -> RiotAPISchema.ValMatchV1Matchlist:
        return await self.invoke("GET", "/val/match/v1/matchlists/by-puuid/{puuid}")

    async def get_val_match_v1_recent_matches_by_queue(self, *, region: Region = ..., queue: str = ...) -> RiotAPISchema.ValMatchV1RecentMatches:
        return await self.invoke("GET", "/val/match/v1/recent-matches/by-queue/{queue}")

    async def get_val_status_v1_platform_data(self, *, region: Region = ...) -> RiotAPISchema.StatusV1PlatformData:
        return await self.invoke("GET", "/val/status/v1/platform-data")


class MarlonAPIClient(BaseClient):
    """Marlon API Client.

    | Resources            | Support                    |
    | -------------------- | -------------------------- |
    | League of Legends    | ❎                         |
    | Legends of Runeterra | ❎                         |
    | Teamfight Tactics    | ❎                         |
    | Valorant             | ✅                         |

    Does not support versioning by patch.

    Example:
    ```python
    async with MarlonAPIClient() as client:
        agents = await client.get_val_v1_agents()
        assert agents[0]["uuid"]
    ```
    """

    class ResponseData[T](TypedDict):
        status: int
        data: T

    def __init__(
        self,
        *,
        base_url: str = "https://valorant-api.com",
        default_params: dict[str, Any] = {},
        default_headers: dict[str, str] = {},
        default_queries: dict[str, str] = {},
        middlewares: list[Middleware] = [
            json_response_middleware(),
            http_error_middleware(),
        ],
    ) -> None:
        super().__init__(
            base_url=base_url,
            default_params=default_params,
            default_headers=default_headers,
            default_queries=default_queries,
            middlewares=middlewares
        )

    async def get_val_v1_agents(self, *, queries: dict = {"isPlayableCharacter": "true"}) -> ResponseData[list[MarlonAPISchema.ValV1Agent]]:
        return await self.invoke("GET", "/v1/agents")

    async def get_val_v1_agent(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Agent]:
        return await self.invoke("GET", "/v1/agents/{uuid}")

    async def get_val_v1_buddies(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Buddy]]:
        return await self.invoke("GET", "/v1/buddies")

    async def get_val_v1_buddy(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Buddy]:
        return await self.invoke("GET", "/v1/buddies/{uuid}")

    async def get_val_v1_bundles(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Bundle]]:
        return await self.invoke("GET", "/v1/bundles")

    async def get_val_v1_bundle(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Bundle]:
        return await self.invoke("GET", "/v1/bundles/{uuid}")

    async def get_val_v1_ceremonies(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Ceremony]]:
        return await self.invoke("GET", "/v1/ceremonies")

    async def get_val_v1_ceremony(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Ceremony]:
        return await self.invoke("GET", "/v1/ceremonies/{uuid}")

    async def get_val_v1_competitive_tiers(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1CompetitiveTier]]:
        return await self.invoke("GET", "/v1/competitivetiers")

    async def get_val_v1_competitive_tier(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1CompetitiveTier]:
        return await self.invoke("GET", "/v1/competitivetiers/{uuid}")

    async def get_val_v1_content_tiers(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1ContentTier]]:
        return await self.invoke("GET", "/v1/contenttiers")

    async def get_val_v1_content_tier(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1ContentTier]:
        return await self.invoke("GET", "/v1/contenttiers/{uuid}")

    async def get_val_v1_contracts(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Contract]]:
        return await self.invoke("GET", "/v1/contracts")

    async def get_val_v1_contract(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Contract]:
        return await self.invoke("GET", "/v1/contracts/{uuid}")

    async def get_val_v1_currencies(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Contract]]:
        return await self.invoke("GET", "/v1/currencies")

    async def get_val_v1_currency(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Contract]:
        return await self.invoke("GET", "/v1/currencies/{uuid}")

    async def get_val_v1_events(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Event]]:
        return await self.invoke("GET", "/v1/events")

    async def get_val_v1_event(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Event]:
        return await self.invoke("GET", "/v1/events/{uuid}")

    async def get_val_v1_gamemodes(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1GameMode]]:
        return await self.invoke("GET", "/v1/gamemodes")

    async def get_val_v1_gamemode(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1GameMode]:
        return await self.invoke("GET", "/v1/gamemodes/{uuid}")

    async def get_val_v1_gears(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Gear]]:
        return await self.invoke("GET", "/v1/gear")

    async def get_val_v1_gear(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Gear]:
        return await self.invoke("GET", "/v1/gear/{uuid}")

    async def get_val_v1_maps(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Map]]:
        return await self.invoke("GET", "/v1/maps")

    async def get_val_v1_map(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Map]:
        return await self.invoke("GET", "/v1/maps/{uuid}")

    async def get_val_v1_playercards(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1PlayerCard]]:
        return await self.invoke("GET", "/v1/playercards")

    async def get_val_v1_playercard(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1PlayerCard]:
        return await self.invoke("GET", "/v1/playercards/{uuid}")

    async def get_val_v1_playertitles(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1PlayerTitle]]:
        return await self.invoke("GET", "/v1/playertitles")

    async def get_val_v1_playertitle(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1PlayerTitle]:
        return await self.invoke("GET", "/v1/playertitles/{uuid}")

    async def get_val_v1_seasons(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Season]]:
        return await self.invoke("GET", "/v1/seasons")

    async def get_val_v1_season(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Season]:
        return await self.invoke("GET", "/v1/seasons/{uuid}")

    async def get_val_v1_sprays(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Spray]]:
        return await self.invoke("GET", "/v1/sprays")

    async def get_val_v1_spray(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Spray]:
        return await self.invoke("GET", "/v1/sprays/{uuid}")

    async def get_val_v1_themes(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Theme]]:
        return await self.invoke("GET", "/v1/themes")

    async def get_val_v1_theme(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Theme]:
        return await self.invoke("GET", "/v1/themes/{uuid}")

    async def get_val_v1_weapons(self, *, queries: dict = {}) -> ResponseData[list[MarlonAPISchema.ValV1Weapon]]:
        return await self.invoke("GET", "/v1/weapons")

    async def get_val_v1_weapon(self, *, uuid: str = ..., queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Weapon]:
        return await self.invoke("GET", "/v1/weapons/{uuid}")

    async def get_val_v1_version(self, *, queries: dict = {}) -> ResponseData[MarlonAPISchema.ValV1Version]:
        return await self.invoke("GET", "/v1/version")
