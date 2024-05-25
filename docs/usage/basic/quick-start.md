---
hide:
    - toc
---

# Quick Start

Request basic info of a LoL summoner. 

```python
from pulsefire.clients import RiotAPIClient
```

```python
async with RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) as client: #(1)!
    account = await client.get_account_v1_by_riot_id(region="americas", game_name="200", tag_line="16384")
    summoner = await client.get_lol_summoner_v4_by_puuid(region="na1", puuid=account["puuid"])
    assert summoner["summonerLevel"] > 200
```

1. It's not recommended to hardcode your API keys or secrets, store them in environment variables and grab them using `os.environ`.
