# Notion Auth

`NotionAuthProvider` wires OAuth tokens or integration tokens into the [Notion provider](../providers/notion.md).

## App Credentials

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `authorization_url` | `https://api.notion.com/v1/oauth/authorize` | `NOTION_AUTHORIZATION_URL`, `NOTION_AUTHORIZE_URL` | OAuth authorization endpoint. |
| `token_url` | `https://api.notion.com/v1/oauth/token` | `NOTION_TOKEN_URL`, `NOTION_ACCESS_TOKEN_URL` | Token exchange endpoint. |
| `client_id` | `None` | `NOTION_CLIENT_ID` | OAuth client ID. |
| `client_secret` | `None` | `NOTION_CLIENT_SECRET` | OAuth client secret. |
| `redirect_uri` | `None` | `NOTION_REDIRECT_URI` | Optional redirect override. |
| `token` | `None` | `NOTION_TOKEN`, `NOTION_INTEGRATION_TOKEN` | Internal integration token fallback. |
| `default_scope` | `None` | — | Provide scopes when using public OAuth. |
| `version` | `None` | `NOTION_VERSION`, `NOTION_API_VERSION` | Override API version header for all bindings. |

## User Credentials

Tokens are stored as `NotionUserCredentials`:

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
| `workspace_id` | `str` or `None` | `None` |
| `workspace_name` | `str` or `None` | `None` |
| `workspace_icon` | `str` or `None` | `None` |

Persist them with `AuthManager.store_credentials` or supply them via `with_credentials`.

## OAuth Flow

```python
from integrations.auth import AuthManager


auth = AuthManager(notion={"client_id": "...", "client_secret": "..."})
flow = auth.notion.oauth2

# Step 1: send the user to Notion's consent screen
step = await flow.authorize(state="docs-sync")

# Step 2: exchange the authorization code
token = await flow.exchange(code="code", subject="workspace-123")
await auth.store_credentials("notion", "workspace-123", token)

# Step 3: use Notion through the integrations container
async with auth.session(subject="workspace-123") as integrations:
    await integrations.notion.list_databases()
```

When you already have an internal integration token, skip the flow and set `token` on the auth provider. Bindings will automatically inject the correct version header and reuse any overrides you supplied on the app credentials.
