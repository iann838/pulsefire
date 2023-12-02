from typing import NoReturn
import collections
import random
import time

from .base import Invocation, RateLimiter


class RiotAPIRateLimiter(RateLimiter):
    """Riot API rate limiter.

    This rate limiter can be served stand-alone for centralized rate limiting,
    also accepting proxy configuration towards said centralized rate limiter.

    Example:
    ```python
    RiotAPIRateLimiter() # Local rate limiter

    RiotAPIRateLimiter().serve() # Served at 127.0.0.1:12227
    RiotAPIRateLimiter().serve(port=<PORT>) # Served at 127.0.0.1:<PORT>
    RiotAPIRateLimiter().serve("0.0.0.0", 12227) # Served at 0.0.0.0:12227 (public)
    RiotAPIRateLimiter().serve("0.0.0.0", 12227, secret=<SECRET>) # Add authentication

    RiotAPIRateLimiter(proxy="http://127.0.0.1:12227") # Proxy to 127.0.0.1:12227
    RiotAPIRateLimiter(proxy="http://127.0.0.1:12227", proxy_secret=<SECRET>) # Proxy authentication
    RiotAPIRateLimiter(proxy="<SCHEME>://<HOST>:<PORT>")
    RiotAPIRateLimiter(proxy="<SCHEME>://<HOST>:<PORT>", proxy_secret=<SECRET>)
    ```

    Parameters:
        proxy: URL of the proxy rate limiter.
        proxy_secret: Secret of the proxy rate limiter if required.
    """

    _index: dict[tuple[str, int, *tuple[str]], tuple[int, int, float, float, float]] = \
        collections.defaultdict(lambda: (0, 0, 0, 0, 0))

    def __init__(self, *, proxy: str | None = None, proxy_secret: str | None = None) -> None:
        self.proxy = proxy
        self.proxy_secret = proxy_secret
        self._track_syncs: dict[float, list] = {}

    async def acquire(self, invocation: Invocation) -> float:
        if self.proxy:
            response = await invocation.session.post(
                self.proxy + "/acquire",
                json={
                    "invocation": {
                        "uid": invocation.uid,
                        "method": invocation.method,
                        "urlformat": invocation.urlformat,
                        "params": invocation.params,
                    }
                },
                headers=self.proxy_secret and {"Authorization": "Bearer " + self.proxy_secret}
            )
            response.raise_for_status()
            return await response.json()

        wait_for = 0
        pinging_targets = []
        requesting_targets = []
        request_time = time.time()
        for target in [
            ("app", 0, invocation.params.get("region", ""), invocation.method),
            ("app", 1, invocation.params.get("region", ""), invocation.method),
            ("method", 0, invocation.params.get("region", ""), invocation.method, invocation.urlformat),
            ("method", 1, invocation.params.get("region", ""), invocation.method, invocation.urlformat),
        ]:
            count, limit, expire, latency, pinged = self._index[target]
            pinging = pinged and request_time - pinged < 10
            if pinging:
                wait_for = max(wait_for, 0.1)
            elif request_time > expire:
                pinging_targets.append(target)
            elif request_time > expire - latency * 1.1 + 0.01 or count >= limit:
                wait_for = max(wait_for, expire - request_time)
            else:
                requesting_targets.append(target)
        if wait_for <= 0:
            if pinging_targets:
                self._track_syncs[invocation.uid] = (request_time, pinging_targets)
                for pinging_target in pinging_targets:
                    self._index[pinging_target] = (0, 0, 0, 0, time.time())
                wait_for = -1
            for requesting_target in requesting_targets:
                count, *values = self._index[requesting_target]
                self._index[requesting_target] = (count + 1, *values)
        return wait_for

    async def synchronize(self, invocation: Invocation, headers: dict[str, str]) -> None:
        if self.proxy:
            response = await invocation.session.post(
                self.proxy + "/synchronize",
                json={
                    "invocation": {
                        "uid": invocation.uid,
                        "method": invocation.method,
                        "urlformat": invocation.urlformat,
                        "params": invocation.params,
                    },
                    "headers": dict(headers)
                },
                headers=self.proxy_secret and {"Authorization": "Bearer " + self.proxy_secret}
            )
            return response.raise_for_status()

        response_time = time.time()
        request_time, pinging_targets = self._track_syncs.pop(invocation.uid)
        if random.random() < 0.1:
            for prev_request_time in self._track_syncs:
                if response_time - prev_request_time > 600:
                    self._track_syncs.pop(prev_request_time, None)

        try:
            header_limits = {
                "app": [[int(v) for v in t.split(':')] for t in headers["X-App-Rate-Limit"].split(',')],
                "method": [[int(v) for v in t.split(':')] for t in headers["X-Method-Rate-Limit"].split(',')],
            }
            header_counts = {
                "app": [[int(v) for v in t.split(':')] for t in headers["X-App-Rate-Limit-Count"].split(',')],
                "method": [[int(v) for v in t.split(':')] for t in headers["X-Method-Rate-Limit-Count"].split(',')],
            }
        except KeyError:
            for pinging_target in pinging_targets:
                self._index[pinging_target] = (0, 0, 0, 0, 0)
        for scope, idx, *subscopes in pinging_targets:
            if idx >= len(header_limits[scope]):
                self._index[(scope, idx, *subscopes)] = (0, 10**10, response_time + 3600, 0, 0)
                continue
            self._index[(scope, idx, *subscopes)] = (
                header_counts[scope][idx][0],
                header_limits[scope][idx][0],
                header_limits[scope][idx][1] + response_time,
                response_time - request_time,
                0
            )

    def serve(self, host="127.0.0.1", port=12227, *, secret: str | None = None) -> NoReturn:
        from aiohttp import web

        app = web.Application(client_max_size=4096)
        routes = web.RouteTableDef()

        def is_authenticated(request: web.Request):
            if not secret:
                return True
            request_secret = request.headers.get("Authorization", "Bearer ").lstrip("Bearer ")
            return request_secret == secret

        @routes.post("/acquire")
        async def acquire(request: web.Request) -> web.Response:
            if not is_authenticated(request):
                return web.Response(status=401)
            try:
                data = await request.json()
                wait_for = await self.acquire(Invocation(**data["invocation"]))
                return web.json_response(wait_for)
            except (KeyError, ValueError):
                return web.Response(status=400)

        @routes.post("/synchronize")
        async def synchronize(request: web.Request) -> web.Response:
            if not is_authenticated(request):
                return web.Response(status=401)
            try:
                data = await request.json()
                await self.synchronize(Invocation(**data["invocation"]), data["headers"])
                return web.Response()
            except (KeyError, ValueError):
                return web.Response(status=400)

        app.add_routes(routes)
        web.run_app(app, host=host, port=port)
