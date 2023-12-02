---
hide:
    - toc
---

# Modifying Schemas

You may modify pulsefire schemas if doing so is required. For example:

- An schema is outdated, incorrect, or incomplete.
- Due to middlewares, the return value is no longer compatible with the schema.

!!! info "Contributing"
    Please consider creating a bugfix pull request if an schema is outdated, incorrect, or incomplete.

Currently the only way to modify schemas is by monkey-patching, do not import any pulsefire module other than `pulsefire.schemas` before the monkey-patching.

```python
from typing import TypedDict

from pulsefire.schemas import RiotAPISchema

RiotAPISchema.LolClashV1Team = TypedDict("LolClashV1Team", {
    "key1": str,
    "key2": int,
})

from pulsefire.clients import RiotAPIClient #(1)!
```

1. Import only after monkey-patching for it take effect.
