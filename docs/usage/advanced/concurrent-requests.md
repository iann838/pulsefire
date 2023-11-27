---
hide:
    - toc
---

# Concurrent Requests

[Asyncio](https://docs.python.org/3/library/asyncio-task.html) provides multiple ways to run tasks concurrently:

- `asyncio.gather`
- `asyncio.TaskGroup` (Python 3.11+)

These are convenient ways to get the job done for general use-cases, however, they may not be the best fit for Pulsefire use-cases, as such, an extended [`TaskGroup`](../../reference/utilities/task-group.md) is provided out of the box with custom modifications.

## Example usage

Request first 20 matches of a LoL summoner.

=== "pulsefire.taskgroups.TaskGroup"
    ```python
    from pulsefire.clients import RiotAPIClient
    from pulsefire.schemas import RiotAPISchema
    from pulsefire.taskgroups import TaskGroup
    ```

    ```python
    async with RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        async with TaskGroup(asyncio.Semaphore(50)) as tg:
            for match_id in match_ids[:20]:
                tg.create_task(client.get_lol_match_v5_match(region="americas", id=match_id))
        matches: list[RiotAPISchema.LolMatchV5Match] = tg.results()

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids
    ```

    !!! info "Key differences from `asyncio.TaskGroup`"
        - Accepts a semaphore to restrict the amount of concurrent running coroutines.
        - Due to semaphore support, the `create_task` method is now async.
        - Allows internal collection of results and exceptions, similar to `asyncio.Task`.
        - If exception collection is on (default), the task group will not abort on task exceptions.


=== "asyncio.TaskGroup"
    ```python
    from pulsefire.clients import RiotAPIClient
    from pulsefire.schemas import RiotAPISchema
    ```

    ```python
    async with RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        tasks: list[asyncio.Task] = []
        async with asyncio.TaskGroup() as tg:
            for match_id in match_ids[:20]:
                tasks.append(tg.create_task(client.get_lol_match_v5_match(region="americas", id=match_id)))
        matches: list[RiotAPISchema.LolMatchV5Match] = [task.result() for task in tasks]

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids
    ```

    !!! warning "About `asyncio.TaskGroup`"
        - The first time any of the tasks belonging to the group fails with an exception other than `asyncio.CancelledError`, the remaining tasks in the group are cancelled, and exceptions are raised to the scope.
        - Tasks may start to **crowd up on memory** if task creation is faster than task execution.


=== "asyncio.gather"
    ```python
    from pulsefire.clients import RiotAPIClient
    from pulsefire.schemas import RiotAPISchema
    ```

    ```python
    async with RiotAPIClient(default_headers={"X-Riot-Token": <API_KEY>}) as client:
        summoner = await client.get_lol_summoner_v4_by_name(region="na1", name="Not a Whale")
        match_ids = await client.get_lol_match_v5_match_ids_by_puuid(region="americas", puuid=summoner["puuid"])

        matches: list[RiotAPISchema.LolMatchV5Match] = await asyncio.gather(*[
            client.get_lol_match_v5_match(region="americas", id=match_id)
            for match_id in match_ids[:20]
        ])

        for match in matches:
            assert match["metadata"]["matchId"] in match_ids
    ```

    !!! warning "About `asyncio.gather`"
        - Requires scheduling **all** coroutines at once, may cause **memory issues** if not properly controlled or semaphored.
