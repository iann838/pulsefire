---
hide:
    - toc
---

# Don't Repeat Clients

It is generally advised to not repeat yourself; however, pulsefire clients instantiations can be repetitive in contexts such as:

- Event driven tasks.
- Web server endpoints.
- Non-aligned concurrency.

There are two recommended options to solve this:

- Using lifespan, startup, and shutdown events. Event-based and web frameworks typically provide these hooks for resource management, these hooks will only be executed once, before the application starts; and once, after the application is ready to shutdown. 

    === "Using lifespan events"

        !!! info
            The following example is based on a [FastAPI](https://fastapi.tiangolo.com/) project.

        ```python
        from contextlib import asynccontextmanager

        from fastapi import FastAPI
        from pulsefire.clients import RiotAPIClient


        client = RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]})

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            async with client:
                yield

        app = FastAPI(lifespan=lifespan)

        @app.get("/foo")
        def read_foo():
            ... #(1)!

        @app.post("/bar")
        def create_bar():
            ...

        ```

        1. Already in client context due to lifespan.


    === "Using startup and shutdown events"

        !!! info
            The following example is based on a [FastAPI](https://fastapi.tiangolo.com/) project.

        ```python
        from contextlib import asynccontextmanager

        from fastapi import FastAPI
        from pulsefire.clients import RiotAPIClient


        app = FastAPI()
        client = RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]})

        @app.on_event("startup")
        async def startup_event():
            await client.__aenter__()

        @app.on_event("shutdown")
        def shutdown_event():
            await client.__aexit__()

        @app.get("/foo")
        def read_foo():
            ... #(1)!

        @app.post("/bar")
        def create_bar():
            ...

        ```

        1. Already in client context due to startup.

- Simplifying the client instantiation code. Client instantiation is fast (if middleware instantiation is fast too), so it is completely fine to instantiate a client for each time it is invoked.

    === "Using kwargs"

        !!! info
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

        !!! info
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
