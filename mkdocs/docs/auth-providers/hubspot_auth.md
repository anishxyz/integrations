# HubSpot Auth

`HubspotAuthProvider` supports OAuth2 and private app tokens for the [HubSpot provider](../providers/hubspot.md).

## App Credentials

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `authorization_url` | `https://app.hubspot.com/oauth/authorize` | `HUBSPOT_AUTHORIZATION_URL`, `HUBSPOT_AUTHORIZE_URL` | OAuth authorization endpoint. |
| `token_url` | `https://api.hubapi.com/oauth/v1/token` | `HUBSPOT_TOKEN_URL`, `HUBSPOT_ACCESS_TOKEN_URL` | Token exchange endpoint. |
| `client_id` | `None` | `HUBSPOT_CLIENT_ID` | OAuth client ID. |
| `client_secret` | `None` | `HUBSPOT_CLIENT_SECRET` | OAuth client secret. |
| `redirect_uri` | `None` | `HUBSPOT_REDIRECT_URI` | Optional redirect override. |
| `token` | `None` | `HUBSPOT_ACCESS_TOKEN`, `HUBSPOT_TOKEN`, `HUBSPOT_PRIVATE_APP_TOKEN` | Private app token fallback. |
| `default_scope` | `None` | — | Provide scopes for OAuth if you need more than the defaults. |

## User Credentials

Tokens are stored as `HubspotUserCredentials`:

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

Persist them via the auth manager just like other providers.

## OAuth Flow

```python
from integrations.auth import AuthManager


auth = AuthManager(hubspot={"client_id": "...", "client_secret": "..."})
flow = auth.hubspot.oauth2

# Step 1: direct the user to HubSpot
step = await flow.authorize(state="deal-sync")

# Step 2: exchange the code and store the token
token = await flow.exchange(code="code", subject="team-123")
await auth.store_credentials("hubspot", "team-123", token)

# Step 3: request data
async with auth.session(subject="team-123") as integrations:
    await integrations.hubspot.get_contacts()
```

If you prefer private app tokens, skip the flow and configure `token` on the auth provider. The binding will fall back to that value when no user token is stored.
