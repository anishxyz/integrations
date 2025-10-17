# Notion

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `NOTION_TOKEN`<br>`NOTION_INTEGRATION_TOKEN` | Required integration secret. |
| `version` | `2022-06-28` | `NOTION_VERSION`<br>`NOTION_API_VERSION` | Overrides API version header. |
| `base_url` | `https://api.notion.com/v1` | `NOTION_BASE_URL` | Override for proxy setups. |
| `timeout` | `10.0` | `NOTION_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `NOTION_USER_AGENT` | Optional. |

## Quick Call

```python
from integrations import Integrations


async def add_page():
    integrations = Integrations(notion={"token": "secret_..."})
    page = await integrations.notion.create_page(
        parent_database_id="abc123",
        title="Docs Launch",
    )
    return page["id"]
```

Other helpers: `update_database_item`, `add_content_to_page`, `add_comment`, plus `raw_request` for experimental APIs.
