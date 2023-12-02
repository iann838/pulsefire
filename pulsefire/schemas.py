"""Module for pulsefire schemas.

This module contains schemas used by pulsefire clients, each schema contains types used by client members.
"""

from typing import NotRequired, TypedDict


class CDragonSchema:

    LolV1ChampionTacticalInfo = TypedDict("LolV1ChampionTacticalInfo", {
        "style": int,
        "difficulty": int,
        "damageType": str
    })
    LolV1ChampionPlaystyleInfo = TypedDict("LolV1ChampionPlaystyleInfo", {
        "damage": int,
        "durability": int,
        "crowdControl": int,
        "mobility": int,
        "utility": int
    })
    LolV1ChampionSkinLine = TypedDict("LolV1ChampionSkinLine", {
        "id": int
    })
    LolV1ChampionSkinChromaDescription = TypedDict("LolV1ChampionSkinChromaDescription", {
        "region": str,
        "description": str
    })
    LolV1ChampionSkinChromaRarity = TypedDict("LolV1ChampionSkinChromaRarity", {
        "region": str,
        "rarity": int
    })
    LolV1ChampionSkinChroma = TypedDict("LolV1ChampionSkinChroma", {
        "id": int,
        "name": str,
        "chromaPath": str,
        "colors": list[str],
        "descriptions": list[LolV1ChampionSkinChromaDescription],
        "rarities": list[LolV1ChampionSkinChromaRarity]
    })
    LolV1ChampionSkin = TypedDict("LolV1ChampionSkin", {
        "id": int,
        "isBase": bool,
        "name": str,
        "splashPath": str,
        "uncenteredSplashPath": str,
        "tilePath": str,
        "loadScreenPath": str,
        "loadScreenVintagePath": NotRequired[str],
        "skinType": str,
        "rarity": str,
        "isLegacy": bool,
        "splashVideoPath": str | None,
        "collectionSplashVideoPath": str | None,
        "featuresText": str | None,
        "chromaPath": str | None,
        "emblems": str | None,
        "regionRarityId": int,
        "rarityGemPath": str | None,
        "skinLines": None | list[LolV1ChampionSkinLine],
        "skinAugments": list[str] | None,
        "description": str | None,
        "chromas": NotRequired[list[LolV1ChampionSkinChroma]]
    })
    LolV1ChampionPassive = TypedDict("LolV1ChampionPassive", {
        "name": str,
        "abilityIconPath": str,
        "abilityVideoPath": str,
        "abilityVideoImagePath": str,
        "description": str
    })
    LolV1ChampionSpellCoefficients = TypedDict("LolV1ChampionSpellCoefficients", {
        "coefficient1": float,
        "coefficient2": float
    })
    LolV1ChampionSpellEffectAmounts = TypedDict("LolV1ChampionSpellEffectAmounts", {
        "Effect1Amount": list[float],
        "Effect2Amount": list[float],
        "Effect3Amount": list[float],
        "Effect4Amount": list[float],
        "Effect5Amount": list[float],
        "Effect6Amount": list[float],
        "Effect7Amount": list[float],
        "Effect8Amount": list[float],
        "Effect9Amount": list[float],
        "Effect10Amount": list[float]
    })
    LolV1ChampionSpellAmmo = TypedDict("LolV1ChampionSpellAmmo", {
        "ammoRechargeTime": list[float],
        "maxAmmo": list[int]
    })
    LolV1ChampionSpell = TypedDict("LolV1ChampionSpell", {
        "spellKey": str,
        "name": str,
        "abilityIconPath": str,
        "abilityVideoPath": str,
        "abilityVideoImagePath": str,
        "cost": str,
        "cooldown": str,
        "description": str,
        "dynamicDescription": str,
        "range": list[float],
        "costCoefficients": list[float],
        "cooldownCoefficients": list[float],
        "coefficients": LolV1ChampionSpellCoefficients,
        "effectAmounts": LolV1ChampionSpellEffectAmounts,
        "ammo": LolV1ChampionSpellAmmo,
        "maxLevel": int
    })
    LolV1Champion = TypedDict("LolGameDataV1Champion", {
        "id": int,
        "name": str,
        "alias": str,
        "title": str,
        "shortBio": str,
        "tacticalInfo": LolV1ChampionTacticalInfo,
        "playstyleInfo": LolV1ChampionPlaystyleInfo,
        "squarePortraitPath": str,
        "stingerSfxPath": str,
        "chooseVoPath": str,
        "banVoPath": str,
        "roles": list[str],
        "recommendedItemDefaults": list[int],
        "skins": list[LolV1ChampionSkin],
        "passive": LolV1ChampionPassive,
        "spells": list[LolV1ChampionSpell]
    })
    LolChampionBinValueCatalogEntry = TypedDict("LolChampionBinValueCatalogEntry", {
        "contentId": str,
        "itemID": int,
        "offerId": str,
        "__type": str
    })
    LolChampionBinValueEventsToTrack = TypedDict("LolChampionBinValueEventsToTrack", {
        "EventToTrack": int,
        "__type": str
    })
    LolChampionBinValue = TypedDict("LolChampionBinValue", {
        "mNameTraKey": str,
        "catalogEntry": LolChampionBinValueCatalogEntry,
        "mDescriptionTraKey": str,
        "EventsToTrack": list[LolChampionBinValueEventsToTrack],
        "category": str,
        "Milestones": list[int],
        "EpicStatStone": bool,
        "TriggeredFromScript": bool,
        "stoneName": str,
        "name": str,
        "statStones": list[str],
        "__type": str
    }, total=False)
    LolV1ChampionInfo = TypedDict("LolV1ChampionInfo", {
        "id": int,
        "name": str,
        "alias": str,
        "squarePortraitPath": str,
        "roles": list[str]
    })
    LolV1Item = TypedDict("LolV1Item", {
        "id": int,
        "name": str,
        "description": str,
        "active": bool,
        "inStore": bool,
        "from": list[int],
        "to": list[int],
        "categories": list[str],
        "maxStacks": int,
        "requiredChampion": str,
        "requiredAlly": str,
        "requiredBuffCurrencyName": str,
        "requiredBuffCurrencyCost": int,
        "specialRecipe": int,
        "isEnchantment": bool,
        "price": int,
        "priceTotal": int,
        "iconPath": str
    })
    LolV1PerkDescriptorAttributes = TypedDict("LolV1PerkDescriptorAttributes", {
        "kBurstDamage": NotRequired[int],
        "kDamagePerSecond": NotRequired[int],
        "kMoveSpeed": NotRequired[int],
        "kGold": NotRequired[int],
        "kHealing": NotRequired[int],
        "kDurability": NotRequired[int],
        "kUtility": NotRequired[int],
        "kCooldown": NotRequired[int],
        "kMana": NotRequired[int],
    })
    LolV1Perk = TypedDict("LolV1Perk", {
        "id": int,
        "name": str,
        "majorChangePatchVersion": str,
        "tooltip": str,
        "shortDesc": str,
        "longDesc": str,
        "recommendationDescriptor": str,
        "iconPath": str,
        "endOfGameStatDescs": list[str],
        "recommendationDescriptorAttributes": LolV1PerkDescriptorAttributes
    })
    LolV1SummonerSpell = TypedDict("LolV1SummonerSpell", {
        "id": int,
        "name": str,
        "description": str,
        "summonerLevel": int,
        "cooldown": int,
        "gameModes": list[str],
        "iconPath": str
    })
    LolV1ProfileIcon = TypedDict("LolV1ProfileIcon", {
        "id": int,
        "iconPath": str
    })
    TftDataTftItem = TypedDict("TftDataTftItem", {
        "apiName": str,
        "associatedTraits": list[str],
        "composition": list[str],
        "desc": str,
        "effects": dict[str, int | float],
        "from": list[int] | None,
        "icon": str,
        "id": int | None,
        "incompatibleTraits": list[str],
        "name": str,
        "unique": bool
    })
    TftDataTftSetChampionAbility = TypedDict("TftDataTftSetChampionAbility", {
        "desc": str,
        "icon": str,
        "name": str,
        "variables": list[TypedDict("Variable", {
            "name": str,
            "value": list[float]
        })]
    })
    TftDataTftSetChampionStats = TypedDict("TftDataTftSetChampionStats", {
        "armor": float,
        "attackSpeed": float,
        "critChance": float,
        "critMultiplier": float,
        "damage": float,
        "hp": float | None,
        "initialMana": int,
        "magicResist": float,
        "mana": float,
        "range": float
    })
    TftDataTftSetChampion = TypedDict("TftDataTftSetChampion", {
        "ability": TftDataTftSetChampionAbility,
        "apiName": str,
        "characterName": str,
        "cost": int,
        "icon": str,
        "name": str,
        "squareIcon": str,
        "stats": TftDataTftSetChampionStats,
        "tileIcon": str,
        "traits": list[str]
    })
    TftDataTftSetTraitEffect = TypedDict("TftDataTftSetTraitEffect", {
        "maxUnits": int,
        "minUnits": int,
        "style": int,
        "variables": dict[str, int | float]
    })
    TftDataTftSetTrait = TypedDict("TftDataTftSetTrait", {
        "apiName": str,
        "desc": str,
        "effects": list[TftDataTftSetTraitEffect],
        "icon": str,
        "name": str
    })
    TftDataTftSet = TypedDict("TftDataTftSet", {
        "champions": list[TftDataTftSetChampion],
        "mutator": NotRequired[str],
        "name": NotRequired[str],
        "number": NotRequired[int],
        "traits": list[TftDataTftSetTrait],
    })
    TftData = TypedDict("TftData", {
        "items": list[TftDataTftItem],
        "setData": list[TftDataTftSet],
        "sets": dict[str, TftDataTftSet]
    })


class DDragonSchema:

    LorCardAsset = TypedDict("LorCardAsset", {
        "gameAbsolutePath": str,
        "fullAbsolutePath": str
    })
    LorCard = TypedDict("LorCard", {
        "associatedCards": list[str],
        "associatedCardRefs": list[str],
        "assets": list[LorCardAsset],
        "regions": list[str],
        "regionRefs": list[str],
        "attack": int,
        "cost": int,
        "health": int,
        "description": str,
        "descriptionRaw": str,
        "levelupDescription": str,
        "levelupDescriptionRaw": str,
        "flavorText": str,
        "artistName": str,
        "name": str,
        "cardCode": str,
        "keywords": list[str],
        "keywordRefs": list[str],
        "spellSpeed": str,
        "spellSpeedRef": str,
        "rarity": str,
        "rarityRef": str,
        "subtypes": list[str],
        "supertype": str,
        "type": str,
        "collectible": bool,
        "set": str,
        "formats": list[str],
        "formatRefs": list[str]
    })


class MerakiCDNSchema:

    LolChampionModifier = TypedDict("LolChampionModifier", {
        "values": list[float],
        "units": list[str]
    })
    LolChampionAbilityEffectLeveling = TypedDict("LolChampionAbilityEffectLeveling", {
        "attribute": str,
        "modifiers": list[LolChampionModifier]
    })
    LolChampionAbilityEffect = TypedDict("LolChampionAbilityEffect", {
        "description": str,
        "leveling": list[LolChampionAbilityEffectLeveling]
    })
    LolChampionAbilityCost = TypedDict("LolChampionAbilityCost", {
        "modifiers": list[LolChampionModifier],
    })
    LolChampionAbilityCooldown = TypedDict("LolChampionAbilityCooldown", {
        "modifiers": list[LolChampionModifier],
        "affectedByCdr": bool
    })
    LolChampionAbility = TypedDict("LolChampionAbility", {
        "name": str,
        "icon": str,
        "effects": list[LolChampionAbilityEffect],
        "cost": LolChampionAbilityCost | None,
        "cooldown": LolChampionAbilityCooldown | None,
        "targeting": str,
        "affects": str,
        "spellshieldable": str | None,
        "resource": str | None,
        "damageType": str | None,
        "spellEffects": str | None,
        "projectile": str | None,
        "onHitEffects": str | None,
        "occurrence": str | None,
        "notes": str,
        "blurb": str,
        "missileSpeed": str | None,
        "rechargeRate": list[int] | None,
        "collisionRadius": str | None,
        "tetherRadius": str | None,
        "onTargetCdStatic": str | None,
        "innerRadius": str | None,
        "speed": str | None,
        "width": str | None,
        "angle": str | None,
        "castTime": str | None,
        "effectRadius": str | None,
        "targetRange": str | None
    })
    LolChampionStat = TypedDict("LolChampionStat", {
        "flat": float,
        "percent": float,
        "perLevel": float,
        "percentPerLevel": float
    })
    LolChampionStats = TypedDict("LolChampionStats", {
        "health": LolChampionStat,
        "healthRegen": LolChampionStat,
        "mana": LolChampionStat,
        "manaRegen": LolChampionStat,
        "armor": LolChampionStat,
        "magicResistance": LolChampionStat,
        "attackDamage": LolChampionStat,
        "movespeed": LolChampionStat,
        "acquisitionRadius": LolChampionStat,
        "selectionRadius": LolChampionStat,
        "pathingRadius": LolChampionStat,
        "gameplayRadius": LolChampionStat,
        "criticalStrikeDamage": LolChampionStat,
        "criticalStrikeDamageModifier": LolChampionStat,
        "attackSpeed": LolChampionStat,
        "attackSpeedRatio": LolChampionStat,
        "attackCastTime": LolChampionStat,
        "attackTotalTime": LolChampionStat,
        "attackDelayOffset": LolChampionStat,
        "attackRange": LolChampionStat,
        "aramDamageTaken": LolChampionStat,
        "aramDamageDealt": LolChampionStat,
        "aramHealing": LolChampionStat,
        "aramShielding": LolChampionStat,
        "urfDamageTaken": LolChampionStat,
        "urfDamageDealt": LolChampionStat,
        "urfHealing": LolChampionStat,
        "urfShielding": LolChampionStat
    })
    LolChampionAttributeRatings = TypedDict("LolChampionAttributeRatings", {
        "attack": NotRequired[int],
        "damage": int,
        "defense": NotRequired[int],
        "magic": NotRequired[int],
        "toughness": int,
        "control": int,
        "mobility": int,
        "utility": int,
        "abilityReliance": int,
        "difficulty": int
    })
    LolChampionAbilities = TypedDict("LolChampionAbilities", {
        "P": list[LolChampionAbility],
        "Q": list[LolChampionAbility],
        "W": list[LolChampionAbility],
        "E": list[LolChampionAbility],
        "R": list[LolChampionAbility]
    })
    LolChampionPrice = TypedDict("LolChampionPrice", {
        "blueEssence": int,
        "rp": int,
        "saleRp": int
    })
    LolChampionSkinChromaDescription = TypedDict("LolChampionSkinChromaDescription", {
        "description": str | None,
        "region": str | None
    })
    LolChampionSkinChromaRarity = TypedDict("LolChampionSkinChromaRarity", {
        "rarity": int | None,
        "region": str | None
    })
    LolChampionSkinChroma = TypedDict("LolChampionSkinChroma", {
        "name": str,
        "id": int,
        "chromaPath": str,
        "colors": list[str],
        "descriptions": list[LolChampionSkinChromaDescription],
        "rarities": list[LolChampionSkinChromaRarity]
    })
    LolChampionSkin = TypedDict("LolChampionSkin", {
        "name": str,
        "id": int,
        "isBase": bool,
        "availability": str,
        "formatName": str,
        "lootEligible": bool,
        "cost": int | str,
        "sale": int,
        "distribution": str | None,
        "rarity": str,
        "chromas": list[LolChampionSkinChroma],
        "lore": str,
        "release": str,
        "set": list[str],
        "splashPath": str,
        "uncenteredSplashPath": str,
        "tilePath": str,
        "loadScreenPath": str,
        "loadScreenVintagePath": str | None,
        "newEffects": bool,
        "newAnimations": bool,
        "newRecall": bool,
        "newVoice": bool,
        "newQuotes": bool,
        "voiceActor": list[str],
        "splashArtist": list[str]
    })
    LolChampion = TypedDict("LolChampion", {
        "id": int,
        "key": str,
        "name": str,
        "title": str,
        "fullName": str,
        "icon": str,
        "resource": str,
        "attackType": str,
        "adaptiveType": str,
        "stats": LolChampionStats,
        "roles": list[str],
        "attributeRatings": LolChampionAttributeRatings,
        "abilities": LolChampionAbilities,
        "releaseDate": str,
        "releasePatch": str,
        "patchLastChanged": str,
        "price": LolChampionPrice,
        "lore": str,
        "faction": str,
        "skins": list[LolChampionSkin]
    })
    LolItemStat = TypedDict("LolItemStat", {
        "flat": float,
        "percent": float,
        "perLevel": float,
        "percentPerLevel": float,
        "percentBase": float,
        "percentBonus": float
    })
    LolItemStats = TypedDict("Stats", {
        "abilityPower": LolItemStat,
        "armor": LolItemStat,
        "armorPenetration": LolItemStat,
        "attackDamage": LolItemStat,
        "attackSpeed": LolItemStat,
        "cooldownReduction": LolItemStat,
        "criticalStrikeChance": LolItemStat,
        "goldPer_10": LolItemStat,
        "healAndShieldPower": LolItemStat,
        "health": LolItemStat,
        "healthRegen": LolItemStat,
        "lethality": LolItemStat,
        "lifesteal": LolItemStat,
        "magicPenetration": LolItemStat,
        "magicResistance": LolItemStat,
        "mana": LolItemStat,
        "manaRegen": LolItemStat,
        "movespeed": LolItemStat,
        "abilityHaste": LolItemStat,
        "omnivamp": LolItemStat,
        "tenacity": LolItemStat
    })
    LolItemPassive = TypedDict("LolItemPassive", {
        "unique": bool,
        "mythic": bool,
        "name": str,
        "effects": str | None,
        "range": int | None,
        "cooldown": int | None,
        "stats": LolItemStats
    })
    LolItemActive = TypedDict("LolItemActive", {
        "unique": bool,
        "name": str,
        "effects": str | None,
        "range": int | None,
        "cooldown": int | None
    })
    LolItemShopPrices = TypedDict("LolItemShopPrices", {
        "total": int,
        "combined": int,
        "sell": int
    })
    LolItemShop = TypedDict("LolItemShop", {
        "prices": LolItemShopPrices,
        "purchasable": bool,
        "tags": list[str]
    })
    LolItem = TypedDict("LolItem", {
        "name": str,
        "id": int,
        "tier": int,
        "rank": list[str],
        "buildsFrom": list[int],
        "buildsInto": list[int],
        "specialRecipe": int,
        "noEffects": bool,
        "removed": bool,
        "requiredChampion": str,
        "requiredAlly": str,
        "icon": str,
        "simpleDescription": str | None,
        "nicknames": list[str],
        "passives": list[LolItemPassive],
        "active": list[LolItemActive],
        "stats": LolItemStats,
        "shop": LolItemShop,
        "iconOverlay": bool
    })


class RiotAPISchema:

    # Account Types

    AccountV1Account = TypedDict("AccountV1Account", {
        "puuid": str,
        "gameName": str,
        "tagLine": str,
    })
    AccountV1ActiveShard = TypedDict("AccountV1ActiveShard", {
        "puuid": str,
        "game": str,
        "activeShard": str,
    })

    # League of Legends Types

    LolChampionV3Rotation = TypedDict("LolChampionV3Rotation", {
        "freeChampionIds": list[int],
        "freeChampionIdsForNewPlayers": list[int],
        "maxNewPlayerLevel": int
    })
    LolChampionV4Mastery = TypedDict("LolChampionV4Mastery", {
        "puuid": str,
        "championId": int,
        "championLevel": int,
        "championPoints": int,
        "lastPlayTime": int,
        "championPointsSinceLastLevel": int,
        "championPointsUntilNextLevel": int,
        "chestGranted": bool,
        "tokensEarned": int,
        "summonerId": str
    })
    LolClashV1Player = TypedDict("LolClashV1Player", {
        "summonerId": str,
        "teamId": str,
        "position": str,
        "role": str,
    })
    LolClashV1Team = TypedDict("LolClashV1Team", {
        "id": str,
        "tournamentId": int,
        "name": str,
        "iconId": int,
        "tier": int,
        "captain": str,
        "abbreviation": str,
        "players": list[LolClashV1Player],
    })
    LolClashV1TournamentSchedule = TypedDict("LolClashV1TournamentSchedule", {
        "id": int,
        "registrationTime": int,
        "startTime": int,
        "cancelled": bool,
    })
    LolClashV1Tournament = TypedDict("LolClashV1Tournament", {
        "id": int,
        "themeId": int,
        "nameKey": str,
        "nameKeySecondary": str,
        "schedule": list[LolClashV1TournamentSchedule]
    })
    LolLeagueV4LeagueEntryMiniSeries = TypedDict("LolLeagueV4LeagueEntryMiniSeries", {
        "losses": int,
        "progress": str,
        "target": int,
        "wins": int,
    })
    LolLeagueV4LeagueEntry = TypedDict("LolLeagueV4LeagueEntry", {
        "summonerId": str,
        "summonerName": str,
        "rank": str,
        "leaguePoints": int,
        "wins": int,
        "losses": int,
        "hotStreak": bool,
        "veteran": bool,
        "freshBlood": bool,
        "inactive": bool,
    })
    LolLeagueV4LeagueFullEntry = TypedDict("LolLeagueV4LeagueFullEntry", {
        "leagueId": str,
        "summonerId": str,
        "summonerName": str,
        "queueType": str,
        "tier": str,
        "rank": str,
        "leaguePoints": int,
        "wins": int,
        "losses": int,
        "hotStreak": bool,
        "veteran": bool,
        "freshBlood": bool,
        "inactive": bool,
        "miniSeries": NotRequired[LolLeagueV4LeagueEntryMiniSeries],
    })
    LolLeagueV4League = TypedDict("LolLeagueV4League", {
        "tier": str,
        "leagueId": str,
        "queue": str,
        "name": str,
        "entries": list[LolLeagueV4LeagueEntry]
    })
    LolMatchV5MatchMetadata = TypedDict("LolMatchV5MatchMetadata", {
        "dataVersion": str,
        "matchId": str,
        "participants": list[str]
    })
    LolMatchV5MatchTeamObjective = TypedDict("LolMatchV5MatchTeamObjective", {
        "first": bool,
        "kills": int
    })
    LolMatchV5MatchInfoParticipantChallenges = TypedDict("LolMatchV5MatchInfoParticipantChallenges", {
        "12AssistStreakCount": int,
        "abilityUses": int,
        "acesBefore15Minutes": int,
        "alliedJungleMonsterKills": int,
        "baronTakedowns": int,
        "blastConeOppositeOpponentCount": int,
        "bountyGold": int,
        "buffsStolen": int,
        "completeSupportQuestInTime": int,
        "controlWardTimeCoverageInRiverOrEnemyHalf": NotRequired[float],
        "controlWardsPlaced": int,
        "damagePerMinute": float,
        "damageTakenOnTeamPercentage": float,
        "dancedWithRiftHerald": int,
        "deathsByEnemyChamps": int,
        "dodgeSkillShotsSmallWindow": int,
        "doubleAces": int,
        "dragonTakedowns": int,
        "earliestBaron": float,
        "earlyLaningPhaseGoldExpAdvantage": int,
        "effectiveHealAndShielding": float,
        "elderDragonKillsWithOpposingSoul": int,
        "elderDragonMultikills": int,
        "enemyChampionImmobilizations": int,
        "enemyJungleMonsterKills": int,
        "epicMonsterKillsNearEnemyJungler": int,
        "epicMonsterKillsWithin30SecondsOfSpawn": int,
        "epicMonsterSteals": int,
        "epicMonsterStolenWithoutSmite": int,
        "firstTurretKilled": int,
        "firstTurretKilledTime": NotRequired[float],
        "flawlessAces": int,
        "fullTeamTakedown": int,
        "gameLength": float,
        "getTakedownsInAllLanesEarlyJungleAsLaner": NotRequired[int],
        "goldPerMinute": float,
        "hadOpenNexus": int,
        "immobilizeAndKillWithAlly": int,
        "initialBuffCount": int,
        "initialCrabCount": int,
        "jungleCsBefore10Minutes": float,
        "junglerTakedownsNearDamagedEpicMonster": int,
        "kTurretsDestroyedBeforePlatesFall": int,
        "kda": float,
        "killAfterHiddenWithAlly": int,
        "killParticipation": float,
        "killedChampTookFullTeamDamageSurvived": int,
        "killingSprees": int,
        "killsNearEnemyTurret": int,
        "killsOnOtherLanesEarlyJungleAsLaner": NotRequired[int],
        "killsOnRecentlyHealedByAramPack": int,
        "killsUnderOwnTurret": int,
        "killsWithHelpFromEpicMonster": int,
        "knockEnemyIntoTeamAndKill": int,
        "landSkillShotsEarlyGame": int,
        "laneMinionsFirst10Minutes": int,
        "laningPhaseGoldExpAdvantage": int,
        "legendaryCount": int,
        "lostAnInhibitor": int,
        "maxCsAdvantageOnLaneOpponent": float,
        "maxKillDeficit": int,
        "maxLevelLeadLaneOpponent": int,
        "mejaisFullStackInTime": int,
        "moreEnemyJungleThanOpponent": float,
        "multiKillOneSpell": int,
        "multiTurretRiftHeraldCount": int,
        "multikills": int,
        "multikillsAfterAggressiveFlash": int,
        "mythicItemUsed": NotRequired[int],
        "outerTurretExecutesBefore10Minutes": int,
        "outnumberedKills": int,
        "outnumberedNexusKill": int,
        "perfectDragonSoulsTaken": int,
        "perfectGame": int,
        "pickKillWithAlly": int,
        "playedChampSelectPosition": NotRequired[int],
        "poroExplosions": int,
        "quickCleanse": int,
        "quickFirstTurret": int,
        "quickSoloKills": int,
        "riftHeraldTakedowns": int,
        "saveAllyFromDeath": int,
        "scuttleCrabKills": int,
        "shortestTimeToAceFromFirstTakedown": NotRequired[float],
        "skillshotsDodged": int,
        "skillshotsHit": int,
        "snowballsHit": int,
        "soloBaronKills": int,
        "soloKills": int,
        "stealthWardsPlaced": int,
        "survivedSingleDigitHpCount": int,
        "survivedThreeImmobilizesInFight": int,
        "takedownOnFirstTurret": int,
        "takedowns": int,
        "takedownsAfterGainingLevelAdvantage": int,
        "takedownsBeforeJungleMinionSpawn": int,
        "takedownsFirstXMinutes": int,
        "takedownsInAlcove": int,
        "takedownsInEnemyFountain": int,
        "teamBaronKills": int,
        "teamDamagePercentage": float,
        "teamElderDragonKills": int,
        "teamRiftHeraldKills": int,
        "tookLargeDamageSurvived": int,
        "turretPlatesTaken": int,
        "turretTakedowns": int,
        "turretsTakenWithRiftHerald": int,
        "twentyMinionsIn3SecondsCount": int,
        "twoWardsOneSweeperCount": int,
        "unseenRecalls": int,
        "visionScoreAdvantageLaneOpponent": float,
        "visionScorePerMinute": float,
        "wardTakedowns": int,
        "wardTakedownsBefore20M": int,
        "wardsGuarded": int,
        "earliestDragonTakedown": NotRequired[float],
        "baronBuffGoldAdvantageOverThreshold": NotRequired[int],
        "teleportTakedowns": NotRequired[int],
        "fastestLegendary": NotRequired[float],
        "highestChampionDamage": NotRequired[int],
        "highestCrowdControlScore": NotRequired[int],
        "junglerKillsEarlyJungle": NotRequired[int],
        "killsOnLanersEarlyJungleAsJungler": NotRequired[int],
        "fasterSupportQuestCompletion": NotRequired[int],
        "highestWardKills": NotRequired[int],
        "soloTurretsLategame": NotRequired[int],
        "thirdInhibitorDestroyedTime": NotRequired[float],
    }, total=False) | dict[str, int | float]
    LolMatchV5MatchInfoParticipantPerksStatPerks = TypedDict("LolMatchV5MatchInfoParticipantPerksStatPerks", {
        "defense": int,
        "flex": int,
        "offense": int
    })
    LolMatchV5MatchInfoParticipantPerksStyleSelection = TypedDict("LolMatchV5MatchInfoParticipantPerksStyleSelection", {
        "perk": int,
        "var1": int,
        "var2": int,
        "var3": int}
    )
    LolMatchV5MatchInfoParticipantPerksStyle = TypedDict("LolMatchV5MatchInfoParticipantPerksStyle", {
        "description": str,
        "selections": list[LolMatchV5MatchInfoParticipantPerksStyleSelection],
        "style": int
    })
    LolMatchV5MatchInfoParticipantPerks = TypedDict("LolMatchV5MatchInfoParticipantPerks", {
        "statPerks": LolMatchV5MatchInfoParticipantPerksStatPerks,
        "styles": list[LolMatchV5MatchInfoParticipantPerksStyle]
    })
    LolMatchV5MatchInfoParticipantMissions = TypedDict("LolMatchV5MatchInfoParticipant", {
        "playerScore0": float,
        "playerScore1": float,
        "playerScore10": float,
        "playerScore11": float,
        "playerScore2": float,
        "playerScore3": float,
        "playerScore4": float,
        "playerScore5": float,
        "playerScore6": float,
        "playerScore7": float,
        "playerScore8": float,
        "playerScore9": float,
    })
    LolMatchV5MatchInfoParticipant = TypedDict("LolMatchV5MatchInfoParticipant", {
        "allInPings": int,
        "assistMePings": int,
        "assists": int,
        "baitPings": int,
        "baronKills": int,
        "basicPings": int,
        "bountyLevel": int,
        "challenges": NotRequired[LolMatchV5MatchInfoParticipantChallenges],
        "champExperience": int,
        "champLevel": int,
        "championId": int,
        "championName": str,
        "championTransform": int,
        "commandPings": int,
        "consumablesPurchased": int,
        "damageDealtToBuildings": int,
        "damageDealtToObjectives": int,
        "damageDealtToTurrets": int,
        "damageSelfMitigated": int,
        "dangerPings": int,
        "deaths": int,
        "detectorWardsPlaced": int,
        "doubleKills": int,
        "dragonKills": int,
        "eligibleForProgression": bool,
        "enemyMissingPings": int,
        "enemyVisionPings": int,
        "firstBloodAssist": bool,
        "firstBloodKill": bool,
        "firstTowerAssist": bool,
        "firstTowerKill": bool,
        "gameEndedInEarlySurrender": bool,
        "gameEndedInSurrender": bool,
        "getBackPings": int,
        "goldEarned": int,
        "goldSpent": int,
        "holdPings": int,
        "individualPosition": str,
        "inhibitorKills": int,
        "inhibitorTakedowns": int,
        "inhibitorsLost": int,
        "item0": int,
        "item1": int,
        "item2": int,
        "item3": int,
        "item4": int,
        "item5": int,
        "item6": int,
        "itemsPurchased": int,
        "killingSprees": int,
        "kills": int,
        "lane": str,
        "largestCriticalStrike": int,
        "largestKillingSpree": int,
        "largestMultiKill": int,
        "longestTimeSpentLiving": int,
        "magicDamageDealt": int,
        "magicDamageDealtToChampions": int,
        "magicDamageTaken": int,
        "missions": NotRequired[LolMatchV5MatchInfoParticipantMissions],
        "needVisionPings": int,
        "neutralMinionsKilled": int,
        "nexusKills": int,
        "nexusLost": int,
        "nexusTakedowns": int,
        "objectivesStolen": int,
        "objectivesStolenAssists": int,
        "onMyWayPings": int,
        "participantId": int,
        "pentaKills": int,
        "perks": LolMatchV5MatchInfoParticipantPerks,
        "physicalDamageDealt": int,
        "physicalDamageDealtToChampions": int,
        "physicalDamageTaken": int,
        "placement": int,
        "playerAugment1": int,
        "playerAugment2": int,
        "playerAugment3": int,
        "playerAugment4": int,
        "playerSubteamId": int,
        "playerScore0": NotRequired[float],
        "playerScore1": NotRequired[float],
        "playerScore10": NotRequired[float],
        "playerScore11": NotRequired[float],
        "playerScore2": NotRequired[float],
        "playerScore3": NotRequired[float],
        "playerScore4": NotRequired[float],
        "playerScore5": NotRequired[float],
        "playerScore6": NotRequired[float],
        "playerScore7": NotRequired[float],
        "playerScore8": NotRequired[float],
        "playerScore9": NotRequired[float],
        "profileIcon": int,
        "pushPings": int,
        "puuid": str,
        "quadraKills": int,
        "riotIdName": NotRequired[str],
        "riotIdTagline": str,
        "riotIdGameName": NotRequired[str],
        "role": str,
        "sightWardsBoughtInGame": int,
        "spell1Casts": int,
        "spell2Casts": int,
        "spell3Casts": int,
        "spell4Casts": int,
        "subteamPlacement": int,
        "summoner1Casts": int,
        "summoner1Id": int,
        "summoner2Casts": int,
        "summoner2Id": int,
        "summonerId": str,
        "summonerLevel": int,
        "summonerName": str,
        "teamEarlySurrendered": bool,
        "teamId": int,
        "teamPosition": str,
        "timeCCingOthers": int,
        "timePlayed": int,
        "totalAllyJungleMinionsKilled": int,
        "totalDamageDealt": int,
        "totalDamageDealtToChampions": int,
        "totalDamageShieldedOnTeammates": int,
        "totalDamageTaken": int,
        "totalEnemyJungleMinionsKilled": int,
        "totalHeal": int,
        "totalHealsOnTeammates": int,
        "totalMinionsKilled": int,
        "totalTimeCCDealt": int,
        "totalTimeSpentDead": int,
        "totalUnitsHealed": int,
        "tripleKills": int,
        "trueDamageDealt": int,
        "trueDamageDealtToChampions": int,
        "trueDamageTaken": int,
        "turretKills": int,
        "turretTakedowns": int,
        "turretsLost": int,
        "unrealKills": int,
        "visionClearedPings": int,
        "visionScore": int,
        "visionWardsBoughtInGame": int,
        "wardsKilled": int,
        "wardsPlaced": int,
        "win": bool
    })
    LolMatchV5MatchInfoTeamBan = TypedDict("LolMatchV5MatchInfoTeamBan", {
        "championId": int,
        "pickTurn": int
    })
    LolMatchV5MatchInfoTeamObjectives = TypedDict("LolMatchV5MatchInfoTeamObjectives", {
        "baron": LolMatchV5MatchTeamObjective,
        "champion": LolMatchV5MatchTeamObjective,
        "dragon": LolMatchV5MatchTeamObjective,
        "horde": LolMatchV5MatchTeamObjective,
        "inhibitor": LolMatchV5MatchTeamObjective,
        "riftHerald": LolMatchV5MatchTeamObjective,
        "tower": LolMatchV5MatchTeamObjective
    })
    LolMatchV5MatchInfoTeam = TypedDict("LolMatchV5MatchInfoTeam", {
        "bans": list[LolMatchV5MatchInfoTeamBan],
        "objectives": LolMatchV5MatchInfoTeamObjectives,
        "teamId": int,
        "win": bool
    })
    LolMatchV5MatchInfo = TypedDict("LolMatchV5MatchInfo", {
        "gameCreation": int,
        "gameDuration": int,
        "gameEndTimestamp": int,
        "gameId": int,
        "gameMode": str,
        "gameName": str,
        "gameStartTimestamp": int,
        "gameType": str,
        "gameVersion": str,
        "mapId": int,
        "participants": list[LolMatchV5MatchInfoParticipant],
        "platformId": str,
        "queueId": int,
        "teams": list[LolMatchV5MatchInfoTeam],
        "tournamentCode": str
    })
    LolMatchV5Match = TypedDict("LolMatchV5Match", {
        "metadata": LolMatchV5MatchMetadata,
        "info": LolMatchV5MatchInfo
    })
    LolMatchV5MatchTimelineParticipantFrameChampionStats = TypedDict("LolMatchV5MatchTimelineParticipantFrameChampionStats", {
        "abilityHaste": int,
        "abilityPower": int,
        "armor": int,
        "armorPen": int,
        "armorPenPercent": int,
        "attackDamage": int,
        "attackSpeed": int,
        "bonusArmorPenPercent": int,
        "bonusMagicPenPercent": int,
        "ccReduction": int,
        "cooldownReduction": int,
        "health": int,
        "healthMax": int,
        "healthRegen": int,
        "lifesteal": int,
        "magicPen": int,
        "magicPenPercent": int,
        "magicResist": int,
        "movementSpeed": int,
        "omnivamp": int,
        "physicalVamp": int,
        "power": int,
        "powerMax": int,
        "powerRegen": int,
        "spellVamp": int
    })
    LolMatchV5MatchTimelineParticipantFrameDamageStats = TypedDict("LolMatchV5MatchTimelineParticipantFrameDamageStats", {
        "magicDamageDone": int,
        "magicDamageDoneToChampions": int,
        "magicDamageTaken": int,
        "physicalDamageDone": int,
        "physicalDamageDoneToChampions": int,
        "physicalDamageTaken": int,
        "totalDamageDone": int,
        "totalDamageDoneToChampions": int,
        "totalDamageTaken": int,
        "trueDamageDone": int,
        "trueDamageDoneToChampions": int,
        "trueDamageTaken": int
    })
    LolMatchV5MatchTimelinePosition = TypedDict("LolMatchV5MatchTimelinePosition", {
        "x": int,
        "y": int
    })
    LolMatchV5MatchTimelineParticipantFrame = TypedDict("LolMatchV5MatchTimelineParticipantFrame", {
        "championStats": LolMatchV5MatchTimelineParticipantFrameChampionStats,
        "currentGold": int,
        "damageStats": LolMatchV5MatchTimelineParticipantFrameDamageStats,
        "goldPerSecond": int,
        "jungleMinionsKilled": int,
        "level": int,
        "minionsKilled": int,
        "participantId": int,
        "position": LolMatchV5MatchTimelinePosition,
        "timeEnemySpentControlled": int,
        "totalGold": int,
        "xp": int
    })
    LolMatchV5MatchTimelineEventDamage = TypedDict("LolMatchV5MatchTimelineEventDamage", {
        "basic": bool,
        "magicDamage": int,
        "name": str,
        "participantId": int,
        "physicalDamage": int,
        "spellName": str,
        "spellSlot": int,
        "trueDamage": int,
        "type": str
    })
    LolMatchV5MatchTimelineMetadata = TypedDict("LolMatchV5MatchTimelineMetadata", {
        "dataVersion": str,
        "matchId": str,
        "participants": list[str]
    })
    LolMatchV5MatchTimelineInfoFrameEvent = TypedDict("LolMatchV5MatchTimelineInfoFrameEvent", {
        "afterId": NotRequired[int],
        "beforeId": NotRequired[int],
        "goldGain": NotRequired[int],
        "participantId": NotRequired[int],
        "timestamp": int,
        "type": str,
        "creatorId": NotRequired[int],
        "wardType": NotRequired[str],
        "level": NotRequired[int],
        "itemId": NotRequired[int],
        "assistingParticipantIds": NotRequired[list[int]],
        "bounty": NotRequired[int],
        "killStreakLength": NotRequired[int],
        "killerId": NotRequired[int],
        "position": NotRequired[LolMatchV5MatchTimelinePosition],
        "shutdownBounty": NotRequired[int],
        "victimDamageDealt": NotRequired[list[LolMatchV5MatchTimelineEventDamage]],
        "victimDamageReceived": NotRequired[list[LolMatchV5MatchTimelineEventDamage]],
        "victimId": NotRequired[int],
        "levelUpType": NotRequired[str],
        "skillSlot": NotRequired[int],
        "realTimestamp": NotRequired[int],
    })
    LolMatchV5MatchTimelineInfoFrameParticipantFrames = TypedDict("LolMatchV5MatchTimelineInfoFrameParticipantFrames", {
        "1": LolMatchV5MatchTimelineParticipantFrame,
        "2": LolMatchV5MatchTimelineParticipantFrame,
        "3": LolMatchV5MatchTimelineParticipantFrame,
        "4": LolMatchV5MatchTimelineParticipantFrame,
        "5": LolMatchV5MatchTimelineParticipantFrame,
        "6": LolMatchV5MatchTimelineParticipantFrame,
        "7": LolMatchV5MatchTimelineParticipantFrame,
        "8": LolMatchV5MatchTimelineParticipantFrame,
        "9": LolMatchV5MatchTimelineParticipantFrame,
        "10": LolMatchV5MatchTimelineParticipantFrame
    })
    LolMatchV5MatchTimelineInfoFrame = TypedDict("LolMatchV5MatchTimelineInfoFrame", {
        "events": list[LolMatchV5MatchTimelineInfoFrameEvent],
        "participantFrames": LolMatchV5MatchTimelineInfoFrameParticipantFrames,
        "timestamp": int
    })
    LolMatchV5MatchTimelineInfoParticipants = TypedDict("LolMatchV5MatchTimelineInfoParticipants", {
        "participantId": int,
        "puuid": str,
    })
    LolMatchV5MatchTimelineInfo = TypedDict("LolMatchV5MatchTimelineInfo", {
        "frameInterval": int,
        "frames": list[LolMatchV5MatchTimelineInfoFrame],
        "gameId": int,
        "participants": list[LolMatchV5MatchTimelineInfoParticipants]
    })
    LolMatchV5MatchTimeline = TypedDict("LolMatchV5MatchTimeline", {
        "metadata": LolMatchV5MatchTimelineMetadata,
        "info": LolMatchV5MatchTimelineInfo
    })
    LolSpectatorV4GameParticipantPerks = TypedDict("LolSpectatorV4GameParticipantPerks", {
        "perkIds": list[int],
        "perkStyle": int,
        "perkSubStyle": int
    })
    LolSpectatorV4GameParticipant = TypedDict("LolSpectatorV4GameParticipant", {
        "gameCustomizationObjects": NotRequired[list[str]],
        "perks": NotRequired[LolSpectatorV4GameParticipantPerks],
        "puuid": str,
        "summonerId": str,
        "teamId": int,
        "spell1Id": int,
        "spell2Id": int,
        "championId": int,
        "profileIconId": int,
        "summonerName": str,
        "bot": bool
    })
    LolSpectatorV4GameObservers = TypedDict("LolSpectatorV4GameObservers", {
        "encryptionKey": str
    })
    LolSpectatorV4Game = TypedDict("LolSpectatorV4Game", {
        "gameId": int,
        "mapId": int,
        "gameMode": str,
        "gameType": str,
        "gameQueueConfigId": int,
        "participants": list[LolSpectatorV4GameParticipant],
        "observers": LolSpectatorV4GameObservers,
        "platformId": str,
        "bannedChampions": list[int],
        "gameStartTime": int,
        "gameLength": int
    })
    LolSpectatorV4GameList = TypedDict("LolSpectatorV4GameList", {
        "gameList": list[LolSpectatorV4Game],
        "clientRefreshInterval": int
    })
    LolSummonerV4Summoner = TypedDict("SummonerV4Summoner", {
        "id": str,
        "accountId": str,
        "puuid": str,
        "name": str,
        "profileIconId": int,
        "revisionDate": int,
        "summonerLevel": int
    })

    # Teamfight Tactics Types

    TftLeagueV1LeagueEntry = TypedDict("TftLeagueV1LeagueEntry", {
        "summonerId": str,
        "summonerName": str,
        "rank": str,
        "leaguePoints": int,
        "wins": int,
        "losses": int,
        "hotStreak": bool,
        "veteran": bool,
        "freshBlood": bool,
        "inactive": bool,
    })
    TftLeagueV1LeagueFullEntry = TypedDict("TftLeagueV1LeagueFullEntry", {
        "leagueId": str,
        "puuid": str,
        "summonerId": str,
        "summonerName": str,
        "queueType": str,
        "tier": str,
        "rank": str,
        "leaguePoints": int,
        "wins": int,
        "losses": int,
        "hotStreak": bool,
        "veteran": bool,
        "freshBlood": bool,
        "inactive": bool,
        "miniSeries": NotRequired[LolLeagueV4LeagueEntryMiniSeries],
    })
    TftLeagueV1League = TypedDict("TftLeagueV1League", {
        "tier": str,
        "leagueId": NotRequired[str],
        "queue": NotRequired[str],
        "name": NotRequired[str],
        "entries": list[TftLeagueV1LeagueEntry]
    })
    TftMatchV1MatchMetadata = TypedDict("TftMatchV1MatchMetadata", {
        "data_version": str,
        "match_id": str,
        "participants": list[str]
    })
    TftMatchV1MatchInfoParticipantCompanion = TypedDict("TftMatchV1MatchInfoParticipantCompanion", {
        "content_ID": str,
        "item_ID": int,
        "skin_ID": int,
        "species": str
    })
    TftMatchV1MatchInfoParticipantTrait = TypedDict("TftMatchV1MatchInfoParticipantTrait", {
        "name": str,
        "num_units": int,
        "style": int,
        "tier_current": int,
        "tier_total": int
    })
    TftMatchV1MatchInfoParticipantUnit = TypedDict("TftMatchV1MatchInfoParticipantUnit", {
        "character_id": str,
        "itemNames": list[str],
        "name": str,
        "rarity": int,
        "tier": int
    })
    TftMatchV1MatchInfoParticipant = TypedDict("TftMatchV1MatchInfoParticipant", {
        "augments": list[str],
        "companion": TftMatchV1MatchInfoParticipantCompanion,
        "gold_left": int,
        "last_round": int,
        "level": int,
        "placement": int,
        "players_eliminated": int,
        "puuid": str,
        "time_eliminated": float,
        "total_damage_to_players": int,
        "traits": list[TftMatchV1MatchInfoParticipantTrait],
        "units": list[TftMatchV1MatchInfoParticipantUnit]
    })
    TftMatchV1MatchInfo = TypedDict("TftMatchV1MatchInfo", {
        "game_datetime": int,
        "game_length": float,
        "game_version": str,
        "participants": list[TftMatchV1MatchInfoParticipant],
        "queue_id": int,
        "tft_game_type": str,
        "tft_set_core_name": str,
        "tft_set_number": int
    })
    TftMatchV1Match = TypedDict("TftMatchV1Match", {
        "metadata": TftMatchV1MatchMetadata,
        "info": TftMatchV1MatchInfo
    })
    TftSummonerV1Summoner = LolSummonerV4Summoner

    # Legends of Runeterra Types

    LorRankedV1LeaderboardPlayer = TypedDict("LorRankedV1LeaderboardPlayer", {
        "name": str,
        "rank": int,
        "lp": float
    })
    LorRankedV1Leaderboard = TypedDict("LorRankedV1Leaderboard", {
        "players": list[LorRankedV1LeaderboardPlayer]
    })
    LorMatchV1MatchMetadata = TypedDict("LorMatchV1MatchMetadata", {
        "data_version": str,
        "match_id": str,
        "participants": list[str]
    })
    LorMatchV1MatchInfoPlayer = TypedDict("LorMatchV1MatchInfoPlayer", {
        "puuid": str,
        "deck_id": str,
        "deck_code": str,
        "factions": list[str],
        "game_outcome": str,
        "order_of_play": int
    })
    LorMatchV1MatchInfo = TypedDict("LorMatchV1MatchInfo", {
        "game_mode": str,
        "game_type": str,
        "game_start_time_utc": str,
        "game_version": str,
        "players": list[LorMatchV1MatchInfoPlayer],
        "total_turn_count": int
    })
    LorMatchV1Match = TypedDict("LorMatchV1Match", {
        "metadata": LorMatchV1MatchMetadata,
        "info": LorMatchV1MatchInfo
    })

    # Valorant Types

    ValContentV1ContentsAssetLocalizedNames = TypedDict("ValContentV1ContentsAssetLocalizedNames", {
        "ar-AE": str,
        "de-DE": str,
        "en-US": str,
        "es-ES": str,
        "es-MX": str,
        "fr-FR": str,
        "id-ID": str,
        "it-IT": str,
        "ja-JP": str,
        "ko-KR": str,
        "pl-PL": str,
        "pt-BR": str,
        "ru-RU": str,
        "th-TH": str,
        "tr-TR": str,
        "vi-VN": str,
        "zh-CN": str,
        "zh-TW": str,
    })
    ValContentV1ContentsAsset = TypedDict("ValContentV1ContentsAsset", {
        "name": str,
        "id": str,
        "localizedNames": NotRequired[ValContentV1ContentsAssetLocalizedNames],
        "assetName": str,
        "assetPath": NotRequired[str]
    })
    ValContentV1ContentsAct = TypedDict("ValContentV1ContentsAct", {
        "id": str,
        "localizedNames": NotRequired[ValContentV1ContentsAssetLocalizedNames],
        "parentId": str,
        "type": str,
        "name": str,
        "isActive": bool
    })
    ValContentV1Contents = TypedDict("ValContentV1Contents", {
        "version": str,
        "characters": list[ValContentV1ContentsAsset],
        "maps": list[ValContentV1ContentsAsset],
        "chromas": list[ValContentV1ContentsAsset],
        "skins": list[ValContentV1ContentsAsset],
        "skinLevels": list[ValContentV1ContentsAsset],
        "equips": list[ValContentV1ContentsAsset],
        "gameModes": list[ValContentV1ContentsAsset],
        "totems": list[ValContentV1ContentsAsset],
        "sprays": list[ValContentV1ContentsAsset],
        "sprayLevels": list[ValContentV1ContentsAsset],
        "charms": list[ValContentV1ContentsAsset],
        "charmLevels": list[ValContentV1ContentsAsset],
        "playerCards": list[ValContentV1ContentsAsset],
        "playerTitles": list[ValContentV1ContentsAsset],
        "acts": list[ValContentV1ContentsAct],
        "ceremonies": list[ValContentV1ContentsAsset]
    })
    
    ValRankedV1LeaderboardTierDetail = TypedDict("ValRankedV1LeaderboardTierDetail", {
        "rankedRatingThreshold": int,
        "startingPage": int,
        "startingIndex": int
    })
    ValRankedV1LeaderboardPlayer = TypedDict("ValRankedV1LeaderboardPlayer", {
        "puuid": str,
        "gameName": str,
        "tagLine": str,
        "leaderboardRank": int,
        "rankedRating": int,
        "numberOfWins": int,
        "competitiveTier": int
    })
    ValRankedV1LeaderboardTierDetails = TypedDict("ValRankedV1LeaderboardTierDetails", {
        "24": ValRankedV1LeaderboardTierDetail,
        "25": ValRankedV1LeaderboardTierDetail,
        "26": ValRankedV1LeaderboardTierDetail,
        "27": ValRankedV1LeaderboardTierDetail
    })
    ValRankedV1Leaderboard = TypedDict("ValRankedV1Leaderboard", {
        "actId": str,
        "players": list[ValRankedV1LeaderboardPlayer],
        "totalPlayers": int,
        "immortalStartingPage": int,
        "immortalStartingIndex": int,
        "topTierRRThreshold": int,
        "tierDetails": ValRankedV1LeaderboardTierDetails,
        "startIndex": int,
        "query": str,
        "shard": str
    })
    ValMatchV1MatchLocation = TypedDict("ValMatchV1MatchLocation", {
        "x": float,
        "y": float
    })
    ValMatchV1MatchPlayerLocation = TypedDict("ValMatchV1MatchPlayerLocation", {
        "puuid": str,
        "viewRadians": float,
        "location": ValMatchV1MatchLocation
    })
    ValMatchV1MatchInfo = TypedDict("ValMatchV1MatchInfo", {
        "matchId": str,
        "mapId": str,
        "gameVersion": str,
        "gameLengthMillis": int,
        "region": str,
        "gameStartMillis": int,
        "provisioningFlowId": str,
        "isCompleted": bool,
        "customGameName": str,
        "queueId": str,
        "gameMode": str,
        "isRanked": bool,
        "premierMatchInfo": dict,
        "seasonId": str
    })
    ValMatchV1MatchPlayerStatsAbilityCasts = TypedDict("ValMatchV1MatchPlayerStatsAbilityCasts", {
        "grenadeCasts": int,
        "ability1Casts": int,
        "ability2Casts": int,
        "ultimateCasts": int
    })
    ValMatchV1MatchPlayerStats = TypedDict("ValMatchV1MatchPlayerStats", {
        "score": int,
        "roundsPlayed": int,
        "kills": int,
        "deaths": int,
        "assists": int,
        "playtimeMillis": int,
        "abilityCasts": ValMatchV1MatchPlayerStatsAbilityCasts | None
    })
    ValMatchV1MatchPlayer = TypedDict("ValMatchV1MatchPlayer", {
        "puuid": str,
        "gameName": str,
        "tagLine": str,
        "teamId": str,
        "partyId": str,
        "characterId": str,
        "stats": ValMatchV1MatchPlayerStats,
        "competitiveTier": int,
        "isObserver": bool,
        "playerCard": str,
        "playerTitle": str,
        "accountLevel": int
    })
    ValMatchV1MatchTeam = TypedDict("ValMatchV1MatchTeam", {
        "teamId": str,
        "won": bool,
        "roundsPlayed": int,
        "roundsWon": int,
        "numPoints": int
    })
    ValMatchV1MatchRoundResultPlayerStatKill = TypedDict("ValMatchV1MatchRoundResultPlayerStatKill", {
        "timeSinceGameStartMillis": int,
        "timeSinceRoundStartMillis": int,
        "killer": str,
        "victim": str,
        "victimLocation": ValMatchV1MatchLocation,
        "assistants": list[str],
        "playerLocations": list[ValMatchV1MatchPlayerLocation],
        "finishingDamage": TypedDict("FinishingDamage", {
            "damageType": str,
            "damageItem": str,
            "isSecondaryFireMode": bool
        })
    })
    ValMatchV1MatchRoundResultPlayerStatDamage = TypedDict("ValMatchV1MatchRoundResultPlayerStatDamage", {
        "receiver": str,
        "damage": int,
        "legshots": int,
        "bodyshots": int,
        "headshots": int
    })
    ValMatchV1MatchRoundResultPlayerStatEconomy = TypedDict("ValMatchV1MatchRoundResultPlayerStatEconomy", {
        "loadoutValue": int,
        "weapon": str,
        "armor": str,
        "remaining": int,
        "spent": int
    })
    ValMatchV1MatchRoundResultPlayerStatAbility = TypedDict("ValMatchV1MatchRoundResultPlayerStatAbility", {
        "grenadeEffects": str | None,
        "ability1Effects": str | None,
        "ability2Effects": str | None,
        "ultimateEffects": str | None
    })
    ValMatchV1MatchRoundResultPlayerStat = TypedDict("ValMatchV1MatchRoundResultPlayerStat", {
        "puuid": str,
        "kills": list[ValMatchV1MatchRoundResultPlayerStatKill],
        "damage": list[ValMatchV1MatchRoundResultPlayerStatDamage],
        "score": int,
        "economy": ValMatchV1MatchRoundResultPlayerStatEconomy,
        "ability": ValMatchV1MatchRoundResultPlayerStatAbility
    })
    ValMatchV1MatchRoundResult = TypedDict("ValMatchV1MatchRoundResult", {
        "roundNum": int,
        "roundResult": str,
        "roundCeremony": str,
        "winningTeam": str,
        "bombPlanter": str | None,
        "bombDefuser": str | None,
        "plantRoundTime": int,
        "plantPlayerLocations": list[ValMatchV1MatchPlayerLocation] | None,
        "plantLocation": ValMatchV1MatchLocation,
        "plantSite": str,
        "defuseRoundTime": int,
        "defusePlayerLocations": list[ValMatchV1MatchPlayerLocation] | None,
        "defuseLocation": ValMatchV1MatchLocation,
        "playerStats": list[ValMatchV1MatchRoundResultPlayerStat],
        "roundResultCode": str
    })
    ValMatchV1Match = TypedDict("ValMatchV1Match", {
        "matchInfo": ValMatchV1MatchInfo,
        "players": list[ValMatchV1MatchPlayer],
        "coaches": list[str],
        "teams": list[ValMatchV1MatchTeam],
        "roundResults": list[ValMatchV1MatchRoundResult]
    })
    ValMatchV1MatchlistHistory = TypedDict("ValMatchV1MatchlistHistory", {
        "matchId": str,
        "gameStartTimeMillis": int,
        "queueId": str
    })
    ValMatchV1Matchlist = TypedDict("ValMatchV1Matchlist", {
        "puuid": str,
        "history": list[ValMatchV1MatchlistHistory]
    })
    ValMatchV1RecentMatches = TypedDict("ValMatchV1RecentMatches", {
        "currentTime": int,
        "matchIds": list[str]
    })

    # Status Types

    StatusV1PlatformDataLocaleContent = TypedDict("StatusV1PlatformDataLocaleContent", {
        "locale": str,
        "content": str
    })
    StatusV1PlatformDataEntryUpdate = TypedDict("StatusV1PlatformDataEntryUpdate", {
        "id": int,
        "created_at": str,
        "updated_at": str,
        "publish": bool,
        "author": str,
        "translations": list[StatusV1PlatformDataLocaleContent],
        "publish_locations": list[str]
    })
    StatusV1PlatformDataEntry = TypedDict("StatusV1PlatformDataEntry", {
        "id": int,
        "created_at": str,
        "updated_at": str | None,
        "archive_at": str | None,
        "titles": list[StatusV1PlatformDataLocaleContent],
        "updates": list[StatusV1PlatformDataEntryUpdate],
        "platforms": list[str],
        "maintenance_status": str | None,
        "incident_severity": str | None
    })
    StatusV1PlatformData = TypedDict("StatusV4PlatformData", {
        "id": str,
        "name": str,
        "locales": list[str],
        "maintenances": list[StatusV1PlatformDataEntry],
        "incidents": list[StatusV1PlatformDataEntry]
    })


class MarlonAPISchema:

    ValV1AgentRole = TypedDict("ValV1AgentRole", {
        "uuid": str,
        "displayName": str,
        "description": str,
        "displayIcon": str,
        "assetPath": str
    })
    ValV1AgentRecruitmentData = TypedDict("ValV1AgentRecruitmentData", {
        "counterId": str,
        "milestoneId": str,
        "milestoneThreshold": int,
        "useLevelVpCostOverride": bool,
        "levelVpCostOverride": int,
        "startDate": str,
        "endDate": str
    })
    ValV1AgentAbility = TypedDict("ValV1AgentAbility", {
        "slot": str,
        "displayName": str,
        "description": str,
        "displayIcon": str | None
    })
    ValV1Agent = TypedDict("ValV1Agent", {
        "uuid": str,
        "displayName": str,
        "description": str,
        "developerName": str,
        "characterTags": list[str] | None,
        "displayIcon": str,
        "displayIconSmall": str,
        "bustPortrait": str,
        "fullPortrait": str,
        "fullPortraitV2": str,
        "killfeedPortrait": str,
        "background": str,
        "backgroundGradientColors": list[str],
        "assetPath": str,
        "isFullPortraitRightFacing": bool,
        "isPlayableCharacter": bool,
        "isAvailableForTest": bool,
        "isBaseContent": bool,
        "role": ValV1AgentRole,
        "recruitmentData": ValV1AgentRecruitmentData | None,
        "abilities": list[ValV1AgentAbility],
        "voiceLine": str | None
    })
    ValV1BuddyLevel = TypedDict("ValV1BuddyLevel", {
        "uuid": str,
        "charmLevel": int,
        "hideIfNotOwned": bool,
        "displayName": str,
        "displayIcon": str,
        "assetPath": str
    })
    ValV1Buddy = TypedDict("ValV1Buddy", {
        "uuid": str,
        "displayName": str,
        "isHiddenIfNotOwned": bool,
        "themeUuid": str | None,
        "displayIcon": str,
        "assetPath": str,
        "levels": list[ValV1BuddyLevel]
    })
    ValV1Bundle = TypedDict("ValV1Bundle", {
        "uuid": str,
        "displayName": str,
        "displayNameSubText": str | None,
        "description": str,
        "extraDescription": str | None,
        "promoDescription": str | None,
        "useAdditionalContext": bool,
        "displayIcon": str,
        "displayIcon2": str,
        "verticalPromoImage": str | None,
        "assetPath": str
    })
    ValV1Ceremony = TypedDict("ValV1Ceremony", {
        "uuid": str,
        "displayName": str,
        "assetPath": str
    })
    ValV1CompetitiveTierTier = TypedDict("ValV1CompetitiveTierTier", {
        "tier": int,
        "tierName": str,
        "division": str,
        "divisionName": str,
        "color": str,
        "backgroundColor": str,
        "smallIcon": str | None,
        "largeIcon": str | None,
        "rankTriangleDownIcon": str | None,
        "rankTriangleUpIcon": str | None
    })
    ValV1CompetitiveTier = TypedDict("ValV1CompetitiveTier", {
        "uuid": str,
        "assetObjectName": str,
        "tiers": list[ValV1CompetitiveTierTier],
        "assetPath": str
    })
    ValV1ContentTier = TypedDict("ValV1ContentTier", {
        "uuid": str,
        "displayName": str,
        "devName": str,
        "rank": int,
        "juiceValue": int,
        "juiceCost": int,
        "highlightColor": str,
        "displayIcon": str,
        "assetPath": str
    })
    ValV1ContractReward = TypedDict("ValV1ContractReward", {
        "type": str,
        "uuid": str,
        "amount": int,
        "isHighlighted": bool
    })
    ValV1ContractContentChapterLevel = TypedDict("ValV1ContractContentChapterLevel", {
        "reward": ValV1ContractReward,
        "xp": int,
        "vpCost": int,
        "isPurchasableWithVP": bool,
        "doughCost": int,
        "isPurchasableWithDough": bool
    })
    ValV1ContractContentChapter = TypedDict("ValV1ContractContentChapter", {
        "isEpilogue": bool,
        "levels": list[ValV1ContractContentChapterLevel],
        "freeRewards": list[ValV1ContractReward] | None
    })
    ValV1ContractContent = TypedDict("ValV1ContractContent", {
        "relationType": str | None,
        "relationUuid": str | None,
        "chapters": list[ValV1ContractContentChapter],
        "premiumRewardScheduleUuid": str | None,
        "premiumVPCost": int
    })
    ValV1Contract = TypedDict("ValV1Contract", {
        "uuid": str,
        "displayName": str,
        "displayIcon": str | None,
        "shipIt": bool,
        "freeRewardScheduleUuid": str,
        "content": ValV1ContractContent,
        "assetPath": str
    })
    ValV1Currency = TypedDict("ValV1Currency", {
        "uuid": str,
        "displayName": str,
        "displayNameSingular": str,
        "displayIcon": str,
        "largeIcon": str,
        "assetPath": str
    })
    ValV1Event = TypedDict("ValV1Event", {
        "uuid": str,
        "displayName": str,
        "shortDisplayName": str,
        "startTime": str,
        "endTime": str,
        "assetPath": str
    })
    ValV1GameModeGameRuleBoolOverride = TypedDict("ValV1GameModeGameRuleBoolOverride", {
        "ruleName": str,
        "state": bool
    })
    ValV1GameModeGameFeatureOverride = TypedDict("ValV1GameModeGameFeatureOverride", {
        "featureName": str,
        "state": bool
    })
    ValV1GameMode = TypedDict("ValV1GameMode", {
        "uuid": str,
        "displayName": str,
        "duration": str,
        "economyType": str,
        "allowsMatchTimeouts": bool,
        "isTeamVoiceAllowed": bool,
        "isMinimapHidden": bool,
        "orbCount": int,
        "roundsPerHalf": int,
        "teamRoles": list[str] | None,
        "gameFeatureOverrides": list[ValV1GameModeGameFeatureOverride] | None,
        "gameRuleBoolOverrides": list[ValV1GameModeGameRuleBoolOverride] | None,
        "displayIcon": str,
        "assetPath": str
    })
    ValV1GearShopData = TypedDict("ValV1GearShopData", {
        "cost": int,
        "category": str,
        "categoryText": str,
        "gridPosition": str | None,
        "canBeTrashed": bool,
        "image": str | None,
        "newImage": str | None,
        "newImage2": str | None,
        "assetPath": str
    })
    ValV1Gear = TypedDict("ValV1Gear", {
        "uuid": str,
        "displayName": str,
        "description": str,
        "displayIcon": str,
        "assetPath": str,
        "shopData": ValV1GearShopData
    })
    ValV1MapCalloutLocation = TypedDict("ValV1MapCalloutLocation", {
        "x": float,
        "y": float
    })
    ValV1MapCallout = TypedDict("ValV1MapCallout", {
        "regionName": str,
        "superRegionName": str,
        "location": ValV1MapCalloutLocation
    })
    ValV1Map = TypedDict("ValV1Map", {
        "uuid": str,
        "displayName": str,
        "narrativeDescription": str,
        "tacticalDescription": str,
        "coordinates": str,
        "displayIcon": str,
        "listViewIcon": str,
        "splash": str,
        "assetPath": str,
        "mapUrl": str,
        "xMultiplier": float,
        "yMultiplier": float,
        "xScalarToAdd": float,
        "yScalarToAdd": float,
        "callouts": list[ValV1MapCallout]
    })
    ValV1PlayerCard = TypedDict("ValV1PlayerCard", {
        "uuid": str,
        "displayName": str,
        "isHiddenIfNotOwned": bool,
        "themeUuid": str | None,
        "displayIcon": str,
        "smallArt": str,
        "wideArt": str,
        "largeArt": str,
        "assetPath": str
    })
    ValV1PlayerTitle = TypedDict("ValV1PlayerTitle", {
        "uuid": str,
        "displayName": str,
        "titleText": str,
        "isHiddenIfNotOwned": bool,
        "assetPath": str
    })
    ValV1Season = TypedDict("ValV1Season", {
        "uuid": str,
        "displayName": str,
        "type": str | None,
        "startTime": str,
        "endTime": str,
        "parentUuid": str | None,
        "assetPath": str
    })
    ValV1SprayLevel = TypedDict("ValV1SprayLevel", {
        "uuid": str,
        "sprayLevel": int,
        "displayName": str,
        "displayIcon": str,
        "assetPath": str
    })
    ValV1Spray = TypedDict("ValV1Spray", {
        "uuid": str,
        "displayName": str,
        "category": str | None,
        "themeUuid": str | None,
        "isNullSpray": bool,
        "hideIfNotOwned": bool,
        "displayIcon": str,
        "fullIcon": str,
        "fullTransparentIcon": str,
        "animationPng": str | None,
        "animationGif": str | None,
        "assetPath": str,
        "levels": list[ValV1SprayLevel]
    })
    ValV1Theme = TypedDict("ValV1Theme", {
        "uuid": str,
        "displayName": str,
        "displayIcon": str | None,
        "storeFeaturedImage": str | None,
        "assetPath": str
    })
    ValV1WeaponSkinLevel = TypedDict("ValV1WeaponSkinLevel", {
        "uuid": str,
        "displayName": str,
        "levelItem": str | None,
        "displayIcon": str | None,
        "streamedVideo": str | None,
        "assetPath": str
    })
    ValV1WeaponSkinChroma = TypedDict("ValV1WeaponSkinChroma", {
        "uuid": str,
        "displayName": str,
        "displayIcon": str | None,
        "fullRender": str,
        "swatch": str | None,
        "streamedVideo": str | None,
        "assetPath": str
    })
    ValV1WeaponSkin = TypedDict("ValV1WeaponSkin", {
        "uuid": str,
        "displayName": str,
        "themeUuid": str,
        "contentTierUuid": None | str,
        "displayIcon": str | None,
        "wallpaper": str | None,
        "assetPath": str,
        "chromas": list[ValV1WeaponSkinChroma],
        "levels": list[ValV1WeaponSkinLevel]
    })
    ValV1WeaponShopDataGridPosition = TypedDict("ValV1WeaponShopDataGridPosition", {
        "row": int,
        "column": int
    })
    ValV1WeaponShopData = TypedDict("ValV1WeaponShopData", {
        "cost": int,
        "category": str,
        "categoryText": str,
        "gridPosition": ValV1WeaponShopDataGridPosition,
        "canBeTrashed": bool,
        "image": str | None,
        "newImage": str | None,
        "newImage2": str | None,
        "assetPath": str
    })
    ValV1WeaponStatsDamageRange = TypedDict("ValV1WeaponStatsDamageRange", {
        "rangeStartMeters": int,
        "rangeEndMeters": int,
        "headDamage": float,
        "bodyDamage": int,
        "legDamage": float
    })
    ValV1WeaponStatsAdsStats = TypedDict("ValV1WeaponStatsAdsStats", {
        "zoomMultiplier": float,
        "fireRate": float,
        "runSpeedMultiplier": float,
        "burstCount": int,
        "firstBulletAccuracy": float
    })
    ValV1WeaponStatsAltShotgunStats = TypedDict("ValV1WeaponStatsAltShotgunStats", {
        "shotgunPelletCount": float,
        "burstRate": float
    })
    ValV1WeaponStatsAirBurstStats = TypedDict("ValV1WeaponStatsAirBurstStats", {
        "shotgunPelletCount": float,
        "burstDistance": float
    })
    ValV1WeaponStats = TypedDict("ValV1WeaponStats", {
        "fireRate": int,
        "magazineSize": int,
        "runSpeedMultiplier": float,
        "equipTimeSeconds": float,
        "reloadTimeSeconds": int,
        "firstBulletAccuracy": float,
        "shotgunPelletCount": int,
        "wallPenetration": str,
        "feature": str | None,
        "fireMode": str | None,
        "altFireType": str | None,
        "adsStats": ValV1WeaponStatsAdsStats,
        "altShotgunStats": ValV1WeaponStatsAltShotgunStats,
        "airBurstStats": ValV1WeaponStatsAirBurstStats,
        "damageRanges": list[ValV1WeaponStatsDamageRange]
    })
    ValV1Weapon = TypedDict("ValV1Weapon", {
        "uuid": str,
        "displayName": str,
        "category": str,
        "defaultSkinUuid": str,
        "displayIcon": str,
        "killStreamIcon": str,
        "assetPath": str,
        "weaponStats": ValV1WeaponStats,
        "shopData": ValV1WeaponShopData,
        "skins": list[ValV1WeaponSkin]
    })
    ValV1Version = TypedDict("ValV1Version", {
        "manifestId": str,
        "branch": str,
        "version": str,
        "buildVersion": str,
        "engineVersion": str,
        "riotClientVersion": str,
        "riotClientBuild": str,
        "buildDate": str
    })

