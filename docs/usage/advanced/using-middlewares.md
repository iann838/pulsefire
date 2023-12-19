---
hide:
    - toc
---

# Using Middlewares

Middlewares are components that acts as a bridge between the client and the data source, responsible for doing specific tasks with the request and response of an invocation. For instance, some of the tasks involved are error handling, rate limiting, deserialization, caching, etc. Additionally, see reference of [built-in middlewares](../../reference/middlewares/http_error_middleware.md) with source codes.

=== "Generalized Syntax"

    Middleware Syntax:

    ```python

    def middleware_1(): #(1)!
        #(2)!
        def constructor(next: MiddlewareCallable): #(3)!
            #(4)!
            async def middleware(invocation: Invocation): #(5)!
                ... #(6)!
                response = await next(invocation) #(7)!
                ... #(8)!
                return response #(9)!

            return middleware

        return constructor
    
    def middleware_2(): ...
    def middleware_3(): ...
    ```

    1. Middleware configuration. May accept configuration parameters.
    2. Middleware setup during configuration (runs only once).
    3. Middleware constructor. Called during client `__init__` with `next` being the next middleware.
    4. Middleware setup during instantiation (runs once for each client).
    5. Middleware function. Called for each invocation.
    6. Tasks to be done with the invocation.
    7. Calls the next middleware with the invocation, this may happen more than once (e.g. in an error handling middleware).
    8. Tasks to be done with the invocation and response.
    9. Returns a value to the previous middleware, this may happen prematurely (e.g. in a cache middleware).

    Client Syntax:

    ```python
    Client(
        middlewares=[
            middleware_1(),
            middleware_2(),
            middleware_3(),
        ]
    )
    ```

=== "Sequence Diagram"

    ```mermaid
    sequenceDiagram
        autonumber
        Client->>middleware_1: invocation
        par middleware_1
            middleware_1->>middleware_2: invocation
            par middleware_2
                middleware_2->>middleware_3: invocation
                par middleware_3
                    middleware_3->>Data Source: invocation
                    Data Source->>middleware_3: response
                end
                middleware_3->>middleware_2: response
            end
            middleware_2->>middleware_1: response
        end
        middleware_1->>Client: response
    ```

## Custom Middlewares

You may write custom middlewares following the syntax above for your own use-cases. 

Clients comes with a default list of middlewares, to change them, provide a new list of middlewares to the `middlewares` parameter during instantiation as a replacement. The following example adds a [cache middleware](../../reference/middlewares/cache_middleware.md) with an [in-memory cache](../../reference/caches/memory-cache.md) to the CDragonClient. 

```python
from pulsefire.caches import MemoryCache
from pulsefire.clients import CDragonClient
from pulsefire.middlewares import (
    cache_middleware,
    http_error_middleware,
    json_response_middleware,
)
```

```python

cache = MemoryCache()

async with CDragonClient(
    default_params={"patch": "latest", "locale": "default"},
    middlewares=[
        cache_middleware(cache, [
            (lambda inv: inv.invoker.__name__ == "get_lol_v1_champion", 3600), #(1)!
        ]),
        json_response_middleware(),
        http_error_middleware(),
    ]
) as client:
    champion = await client.get_lol_v1_champion(id=777) #(2)!
    assert champion["name"] == "Yone"
    champion = await client.get_lol_v1_champion(id=777) #(3)!
    assert champion["name"] == "Yone"
```

1. Cache middleware defining a TTL of 1 hour and applies to all requests. See reference for detailed usage.
2. This request misses the cache, proceeds to next middleware, then cache the response.
3. This request hits the cache, returns the cached response immediately.

!!! info "Contributing"
    Please consider creating a pull request if you consider your custom middlewares to be in scope and useful for most users.
