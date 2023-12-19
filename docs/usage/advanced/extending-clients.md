---
hide:
    - toc
---

# Extending Clients

You may extend pulsefire clients if doing so is required. For example:

- A data source is not implemented.
- An endpoint is not implemented.
- An endpoint has an outdated or incorrect signature.

See reference for [base client class](../../reference/clients/base-client.md).

```python
from pulsefire.clients import BaseClient
```

```python

class AnotherClient(BaseClient):

    def __init__(
        self,
        *,
        base_url: str = <BASE_URL>, #(1)!
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

    async def get_sample_resource_by_param_1(self, *, param_1: str = ...) -> <ReturnType>: #(2)!
        return await self.invoke("GET", <PATH_OR_URL>) #(3)!
```

1. Base URL of the data source, may be blank.
2. Defines an endpoint, may provide parameters or a return type (schema). **Special parameters** that are passed directly to HTTP requests and **not considered as path parameters**: `queries`, `headers`, `json`, `data`. If the value of the parameter is Ellipsis (`...`), it will be ignored and considered empty.
3. Calls `invoke` to build an invocation and send through the middlewares. Requires the HTTP method and the path or url of the endpoint, bracket formatting (`{param_1}`) is allowed. All local variables (e.g. `param_1`) in this scope are implicitly grabbed.

!!! info "Contributing"
    Please consider creating a pull request if you consider your changes to be in scope and useful for most users.
