# Slack Auth

`SlackAuthProvider` manages OAuth and bot tokens for the [Slack provider](../providers/slack.md).

## App Credentials

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `authorization_url` | `https://slack.com/oauth/v2/authorize` | `SLACK_AUTHORIZATION_URL`, `SLACK_AUTHORIZE_URL` | OAuth authorization endpoint. |
| `token_url` | `https://slack.com/api/oauth.v2.access` | `SLACK_TOKEN_URL`, `SLACK_ACCESS_TOKEN_URL` | OAuth token exchange endpoint. |
| `client_id` | `None` | `SLACK_CLIENT_ID` | OAuth client ID. |
| `client_secret` | `None` | `SLACK_CLIENT_SECRET` | OAuth client secret. |
| `redirect_uri` | `None` | `SLACK_REDIRECT_URI` | Optional redirect override. |
| `bot_token` | `None` | `SLACK_BOT_TOKEN`, `SLACK_TOKEN` | Bot token fallback when you skip OAuth. |
| `user_token` | `None` | `SLACK_USER_TOKEN` | Alternate fallback used when no bot token is configured. |
| `default_scope` | `None` | — | Provide scopes for the OAuth flow. |

## User Credentials

Tokens are stored as `SlackUserCredentials`:

| Field | Type | Default |
| --- | --- | --- |
| `access_token` | `str` | — |
| `token_type` | `str` | `"Bearer"` |
| `refresh_token` | `str` or `None` | `None` |
| `scope` | `tuple[str, ...]` or `None` | `None` |
| `expires_in` | `int` or `None` | `None` |
| `expires_at` | `float` or `None` | `None` |
| `id_token` | `str` or `None` | `None` |
| `raw` | `dict[str, Any]` | `{}` |
| `bot_user_id` | `str` or `None` | `None` |
| `team_id` | `str` or `None` | `None` |
| `team_name` | `str` or `None` | `None` |
| `authed_user_id` | `str` or `None` | `None` |

Persist them via `AuthManager.store_credentials` or supply them through `with_credentials`.

## OAuth Flow

```python
from integrations.auth import AuthManager


auth = AuthManager(slack={"client_id": "...", "client_secret": "..."})
flow = auth.slack.oauth2

# Step 1: redirect to Slack
step = await flow.authorize(state="workspace-join")

# Step 2: exchange the code
token = await flow.exchange(code="code", subject="team-123")
await auth.store_credentials("slack", "team-123", token)

# Step 3: call Slack APIs
async with auth.session(subject="team-123") as integrations:
    await integrations.slack.conversations_list()
```

If you already have a bot token, skip the flow and configure `bot_token` (or `user_token`). Bindings will automatically propagate any overrides you attach to the app credentials, such as custom base URLs or timeouts.
