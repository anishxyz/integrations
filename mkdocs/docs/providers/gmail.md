# Gmail

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `GMAIL_TOKEN`<br>`GMAIL_ACCESS_TOKEN`<br>`GOOGLE_TOKEN`<br>`GOOGLE_ACCESS_TOKEN` | Required OAuth access token. |
| `authorization_scheme` | `Bearer` | `GMAIL_TOKEN_TYPE` | Rarely overridden. |
| `base_url` | `https://gmail.googleapis.com/gmail/v1` | `GMAIL_BASE_URL` | Change for testing stubs. |
| `user_id` | `"me"` | `GMAIL_USER_ID` | Override when acting for another mailbox. |
| `timeout` | `10.0` | `GMAIL_TIMEOUT` | Seconds. |

## Quick Call

```python
from integrations import Integrations


async def send_email():
    integrations = Integrations(gmail={"token": "ya29..."})
    await integrations.gmail.send_email(
        to=["ops@example.com"],
        subject="Deploy finished",
        body="All green.",
    )
```

Use `add_label_to_email`, `move_email`, or `raw_request` when you need lower-level Gmail API access. The provider raises if no token is supplied.
