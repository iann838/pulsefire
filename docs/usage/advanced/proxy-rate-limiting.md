# Proxy Rate Limiting

Proxy rate limiting allows rate limiting tasks to be performed at a centralized location. In typical rate limiting, each runtime has its own rate limiter and in-memory index, which can lead to inconsistent results when multiple runtimes are accessing a shared resource. Proxy rate limiting is useful for scenarios that require more than one runtime, such as:

- Serverless computing.
- Multi-processing.
- Sharding and replication.

=== "Proxied flowchart"

    The flowchart is based on a project that contains:

    - Application APIs on serverless computing.
    - Cronjobs on compute instances.

    ```mermaid
    flowchart TB
        subgraph "Compute"
            A{"RateLimiter"}
        end
        B["DataSource"]
        C["AppAPI:1"] --> A
        D["AppAPI:2"] --> A
        subgraph "Serverless"
            C; D
        end
        E[CronJob] --> A
        subgraph "Compute"
            E
        end
        A --> B
    ```

    !!! info
        The centralized rate limiter is hosted on a compute instance.

=== "Non-Proxied flowchart"

    The flowchart is based on a project that contains:

    - Application APIs on serverless computing.
    - Cronjobs on compute instances.

    ```mermaid
    flowchart TB
        B["DataSource"]
        subgraph "Serverless"
            P{"RateLimiter:1"}
            Q{"RateLimiter:2"}
            C["AppAPI:1"] --> P
            D["AppAPI:2"] --> Q
        end
        subgraph "Compute"
            R{"RateLimiter:3"}
            E[CronJob] --> R
        end
        P --> B
        Q --> B
        R --> B
    ```

    !!! warning
        Each runtime has its own rate limiter, and is not aware of other runtimes.


## Configuration

The following instructions shows how to configure a centralized [`RiotAPIRateLimiter`](../../reference/ratelimiters/riot-api-rate-limiter.md).

On your hardware that will host the centralized rate limiter:

1. Setup python and install pulsefire.

2. Create a python file `ratelimiter.py` with the following code:

    === "Local default"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter().serve() # Served at 127.0.0.1:12227
        ```

    === "Local custom port"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter().serve(port=<PORT>) # Served at 127.0.0.1:<PORT>
        ```

    === "Public unprotected"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter().serve("0.0.0.0", 12227) # Served at 0.0.0.0:12227 (public)
        ```

    === "Public protected"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter().serve("0.0.0.0", 12227, secret=<SECRET>) # Add authentication
        ```

        !!! warning "About secret"
            Ensure that the secret is hard to bruteforce, otherwise defeats the purpose.

3. Manage the execution with a service manager such as [systemd](https://systemd.io/).

    ```sh
    [Unit]
    Description=Rate Limiter
    After=multi-user.target

    [Service]
    Type=simple
    Restart=always
    ExecStart=<PYTHON_EXECUTABLE> <FILE_DIR>/ratelimiter.py

    [Install]
    WantedBy=multi-user.target
    ```

4. (Public only) A reverse proxy (e.g. nginx) may be set up if HTTPS is needed.

5. (Public only) Ensure that the firewall is configured correctly to allow incoming traffic.

On each of your runtimes:

1. Provide proxy target to the rate limiter:

    === "Local default"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter(proxy="http://127.0.0.1:12227")
        ```

    === "Local custom port"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter(proxy="http://127.0.0.1:<PORT>")
        ```

    === "Public unprotected"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter(proxy="<SCHEME>://<HOST>:<PORT>")
        ```

    === "Public protected"

        ```python
        from pulsefire.ratelimiters import RiotAPIRateLimiter

        RiotAPIRateLimiter(proxy="<SCHEME>://<HOST>:<PORT>", proxy_secret=<SECRET>)
        ```

2. Run a test invocation to ensure the proxy is reachable.

    ```python
    async with RiotAPIClient(
        default_headers={"X-Riot-Token": <API_KEY>},
        middlewares=[
            json_response_middleware(),
            http_error_middleware(),
            rate_limiter_middleware(RiotAPIRateLimiter(
                proxy="<PROXY_TARGET>"
            )),
        ]
    ) as client:
        await client.get_lol_champion_v3_rotation(region="na1")
    ```
