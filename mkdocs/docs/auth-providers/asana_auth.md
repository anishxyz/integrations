# Asana Auth

`AsanaAuthProvider` exchanges OAuth tokens or personal access tokens for the [Asana provider](../providers/asana.md).

## App Credentials

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `authorization_url` | `https://app.asana.com/-/oauth_authorize` | `ASANA_AUTHORIZATION_URL`, `ASANA_AUTHORIZE_URL` | Override when using a self-hosted OAuth screen. |
| `token_url` | `https://app.asana.com/-/oauth_token` | `ASANA_TOKEN_URL`, `ASANA_ACCESS_TOKEN_URL` | Exchange endpoint for OAuth2. |
| `client_id` | `None` | `ASANA_CLIENT_ID` | OAuth client ID. |
| `client_secret` | `None` | `ASANA_CLIENT_SECRET` | OAuth client secret. |
| `redirect_uri` | `None` | `ASANA_REDIRECT_URI` | Optional redirect override. |
| `token` | `None` | `ASANA_ACCESS_TOKEN`, `ASANA_PERSONAL_ACCESS_TOKEN`, `ASANA_TOKEN` | Personal access token fallback when skipping OAuth. |
| `default_scope` | `None` | — | Comma/space separated scopes or a sequence. |
| `workspace_gid` | `None` | `ASANA_WORKSPACE_GID`, `ASANA_WORKSPACE` | Default workspace to inject into settings. |

## User Credentials

Tokens are stored as `AsanaUserCredentials`:

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
| `workspace_gid` | `str` or `None` | `None` |

Persist them with `AuthManager.store_credentials` or pass them via `with_credentials`.

## OAuth Flow

```python
from integrations.auth import AuthManager


auth = AuthManager(asana={"client_id": "...", "client_secret": "..."})
flow = auth.asana.oauth2

# Step 1: send the user through Asana's consent screen
step = await flow.authorize(state="example-state")

# Step 2: exchange the code for a token
token = await flow.exchange(code="authorization-code", subject="user-123")
await auth.store_credentials("asana", "user-123", token)

# Step 3: build a session with hydrated Asana settings
async with auth.session(subject="user-123") as integrations:
    await integrations.asana.get_user("me")
```

The binding prefers stored OAuth tokens but will fall back to the app-level personal access token when present.
