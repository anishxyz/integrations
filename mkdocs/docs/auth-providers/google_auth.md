# Google Auth

`GoogleAuthProvider` centralizes OAuth for Gmail, Google Calendar, Google Docs, Google Drive, and Google Sheets. One set of app credentials can hydrate every Google Workspace provider.

## App Credentials

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `authorization_url` | `https://accounts.google.com/o/oauth2/v2/auth` | `GOOGLE_AUTHORIZATION_URL`, `GOOGLE_AUTHORIZE_URL` | Authorization endpoint for Google OAuth. |
| `token_url` | `https://oauth2.googleapis.com/token` | `GOOGLE_TOKEN_URL`, `GOOGLE_ACCESS_TOKEN_URL` | Token exchange endpoint. |
| `client_id` | `None` | `GOOGLE_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_ID` | OAuth client ID. |
| `client_secret` | `None` | `GOOGLE_CLIENT_SECRET`, `GOOGLE_OAUTH_CLIENT_SECRET` | OAuth client secret. |
| `redirect_uri` | `None` | `GOOGLE_REDIRECT_URI`, `GOOGLE_OAUTH_REDIRECT_URI` | Optional redirect override. |
| `token` | `None` | `GOOGLE_TOKEN`, `GOOGLE_ACCESS_TOKEN` | Service account or manually issued access token fallback. |
| `refresh_token` | `None` | `GOOGLE_REFRESH_TOKEN`, `GOOGLE_OAUTH_REFRESH_TOKEN` | Optional refresh token when bootstrapping from a service account. |
| `default_scope` | `None` | — | Provide scopes for the OAuth flow (string or sequence). |

Extra keys defined on the credentials (for example `default_spreadsheet_id`, `default_drive_id`, or provider-specific base URLs) are forwarded to the corresponding provider settings.

## User Credentials

Tokens are stored as `GoogleUserCredentials`:

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

Persist them through `AuthManager.store_credentials` or supply them via `with_credentials` when opening a session.

## OAuth Flow

```python
from integrations.auth import AuthManager


auth = AuthManager(
    google={
        "client_id": "...",
        "client_secret": "...",
        "redirect_uri": "https://example.com/oauth2/callback",
        "default_scope": [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.events",
        ],
    }
)
flow = auth.google.oauth2

# Step 1: redirect the user through Google's consent screen
step = await flow.authorize(state="subject-123")

# Step 2: exchange the authorization code
token = await flow.exchange(code="auth-code", subject="user-123")
await auth.store_credentials("google", "user-123", token)

# Step 3: build a session and use any Google provider
async with auth.session(subject="user-123") as integrations:
    await integrations.gmail.get_profile()
    await integrations.google_calendar.list_events()
```

Bindings fan out to each Google provider, so one stored token unlocks Gmail, Calendar, Docs, Drive, and Sheets simultaneously.
