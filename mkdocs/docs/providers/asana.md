# Asana

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `ASANA_ACCESS_TOKEN`<br>`ASANA_PERSONAL_ACCESS_TOKEN`<br>`ASANA_TOKEN` | Required for authenticated requests. |
| `workspace_gid` | `None` | `ASANA_WORKSPACE_GID`<br>`ASANA_WORKSPACE` | Optional default workspace context. |
| `base_url` | `https://app.asana.com/api/1.0` | `ASANA_BASE_URL` | Override for self-hosted proxies. |
| `timeout` | `10.0` | `ASANA_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `ASANA_USER_AGENT` | Added to every request. |

## Quick Call

```python
from integrations import Integrations


async def new_task():
    integrations = Integrations(asana={"token": "...", "workspace_gid": "123"})
    task = await integrations.asana.create_task(
        workspace_gid="123",
        name="Ship docs",
    )
    return task["gid"]
```

Notable actions: `create_task`, `find_project`, `raw_request`. Responses are auto-unwrapped so `.create_task` returns the Asana `"data"` payload.
