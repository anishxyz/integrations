# GitHub Auth

`GithubAuthProvider` wires OAuth or personal access tokens into the [GitHub provider](../providers/github.md).

## App Credentials

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `authorization_url` | `https://github.com/login/oauth/authorize` | `GITHUB_AUTHORIZATION_URL`, `GITHUB_AUTHORIZE_URL` | Override when hosting your own OAuth app UI. |
| `token_url` | `https://github.com/login/oauth/access_token` | `GITHUB_TOKEN_URL` | Rarely changed. |
| `client_id` | `None` | `GITHUB_CLIENT_ID` | OAuth app client ID. |
| `client_secret` | `None` | `GITHUB_CLIENT_SECRET` | OAuth app client secret. |
| `redirect_uri` | `None` | `GITHUB_REDIRECT_URI` | Optional override per environment. |
| `token` | `None` | `GITHUB_TOKEN`, `GITHUB_API_TOKEN` | Drop in a PAT when you skip OAuth. |

Supply these via keyword args when constructing `AuthManager` or rely on environment variables.

## User Credentials

Tokens are stored as `GithubUserCredentials`:

| Field | Type | Default |
| --- | --- | --- |
| `access_token` | `str` or `None` | `None` |
| `token_type` | `str` or `None` | `"Bearer"` |
| `refresh_token` | `str` or `None` | `None` |
| `scope` | `tuple[str, ...]` or `None` | `None` |
| `expires_in` | `int` or `None` | `None` |
| `expires_at` | `float` or `None` | `None` |
| `id_token` | `str` or `None` | `None` |
| `raw` | `dict[str, Any]` | `{}` |

Persist them through `AuthManager.store_credentials` or plug them into `with_credentials`.

## OAuth Flow

```python
from integrations.auth import AuthManager


auth = AuthManager(
    github={"client_id": "...", "client_secret": "...", "redirect_uri": "..."},
)
flow = auth.github.oauth2

# Step 1: send user to GitHub
step = await flow.authorize(state="optional-state")

# Step 2: exchange code after redirect
token = await flow.exchange(code="authorization-code", subject="user-123")
await auth.store_credentials("github", "user-123", token)

# Step 3: build a session
async with auth.session(subject="user-123") as integrations:
    await integrations.github.get_authenticated_user()
```

Bindings automatically convert the stored token into `GithubSettings`, so `Integrations.github` gains the right authorization headers without additional wiring.
