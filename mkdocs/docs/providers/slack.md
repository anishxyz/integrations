# Slack

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `SLACK_BOT_TOKEN`<br>`SLACK_TOKEN`<br>`SLACK_USER_TOKEN` | User or bot token required. |
| `base_url` | `https://slack.com/api` | `SLACK_BASE_URL` | Override for testing proxies. |
| `user_agent` | `integrations-sdk` | `SLACK_USER_AGENT` | Optional. |
| `timeout` | `10.0` | `SLACK_TIMEOUT` | Seconds. |

## Quick Call

```python
from integrations import Integrations


async def post_message():
    integrations = Integrations(slack={"token": "xoxb-..."})
    await integrations.slack.send_channel_message(
        channel="#docs",
        text="Documentation shipped.",
    )
```

You also get helpers for DMs, reminders, channel administration, and profile status management. Use `raw_request` when you need a Slack API that is not wrapped yet.
