# HubSpot

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `access_token` | `None` | `HUBSPOT_ACCESS_TOKEN`<br>`HUBSPOT_TOKEN`<br>`HUBSPOT_PRIVATE_APP_TOKEN` | Required private app token. |
| `base_url` | `https://api.hubapi.com` | `HUBSPOT_BASE_URL` | Override for EU or custom domains. |
| `timeout` | `15.0` | `HUBSPOT_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `HUBSPOT_USER_AGENT` | Optional. |

## Quick Call

```python
from integrations import Integrations


async def upsert_contact():
    integrations = Integrations(hubspot={"access_token": "pat-..."})
    contact = await integrations.hubspot.create_or_update_contact(
        identifier="user@example.com",
        properties={"firstname": "Docs"},
    )
    return contact["id"]
```

Choose from CRM helpers for contacts, companies, deals, custom objects, marketing uploads, or fall back to `raw_request` when exploring beta features.
