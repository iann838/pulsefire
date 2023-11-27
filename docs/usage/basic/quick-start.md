---
hide:
    - toc
---

# Quick Start

Request basic info of a LoL summoner. 

=== "async with (recommended)"

    ```python
    from pulsefire.clients import RiotAPIClient
    ```

    ```python
    async def main()
        async with RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) as client: #(1)!
            summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
            print(summoner["name"])
            print(summoner["summonerLevel"])
            print(summoner["profileIconId"])
            print(summoner["puuid"])
    ```

    1. It's not recommended to hardcode your API keys or secrets, store them in environment variables and grab them using `os.environ`.

=== "decorator (as context manager)"

    ```python
    from pulsefire.clients import RiotAPIClient
    ```

    ```python
    client = RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) #(1)!

    @client
    async def main()
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        print(summoner["name"])
        print(summoner["summonerLevel"])
        print(summoner["profileIconId"])
        print(summoner["puuid"])
    ```

    1. It's not recommended to hardcode your API keys or secrets, store them in environment variables and grab them using `os.environ`.

=== "standalone (no resource reuse)"

    ```python
    from pulsefire.clients import RiotAPIClient
    ```

    ```python
    async def main()
        client = RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) #(1)!
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        print(summoner["name"])
        print(summoner["summonerLevel"])
        print(summoner["profileIconId"])
        print(summoner["puuid"])
    ```

    1. It's not recommended to hardcode your API keys or secrets, store them in environment variables and grab them using `os.environ`.

!!! info "Client context manager"
    Clients can be used with or without context managers (`async with` or `@`), doing so will speed up consecutive and concurrent requests to the internet as it uses a shared `aiohttp.ClientSession`.