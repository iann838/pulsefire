---
hide:
    - toc
---

# Don't Repeat Clients

It is generally advised to not repeat yourself; however, pulsefire clients instantiations can be repetitive in contexts such as:

- Event driven tasks.
- Web server endpoints.
- Non-aligned concurrency.

=== "Using kwargs"

    The following example is based on a [FastAPI](https://fastapi.tiangolo.com/) project.

    ```python
    from fastapi import FastAPI
    from pulsefire.clients import RiotAPIClient


    app = FastAPI()
    client_kwargs = dict(
        default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}
    )


    @app.get("/foo")
    def read_foo():
        async with RiotAPIClient(**client_kwargs) as client:
            ...


    @app.post("/bar")
    def create_bar():
        async with RiotAPIClient(**client_kwargs) as client:
            ...

    ```

=== "Using partials"

    The following example is based on a [FastAPI](https://fastapi.tiangolo.com/) project.

    ```python
    import functools

    from fastapi import FastAPI
    from pulsefire.clients import RiotAPIClient


    app = FastAPI()
    client_partial = functools.partial(
        RiotAPIClient,
        default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}
    )


    @app.get("/foo")
    def read_foo():
        async with client_partial() as client:
            ...


    @app.post("/bar")
    def create_bar():
        async with client_partial() as client:
            ...

    ```

=== "Raw instantiation"

    The following example is based on a [FastAPI](https://fastapi.tiangolo.com/) project.

    ```python
    from fastapi import FastAPI
    from pulsefire.clients import RiotAPIClient


    app = FastAPI()


    @app.get("/foo")
    def read_foo():
        async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
            ...


    @app.post("/bar")
    def create_bar():
        async with RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]}) as client:
            ...

    ```
