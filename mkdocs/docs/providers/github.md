# GitHub

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `GITHUB_TOKEN`<br>`GITHUB_PAT`<br>`GITHUB_OAUTH_TOKEN`<br>`GITHUB_APP_TOKEN` | Required for authenticated calls. |
| `authorization_scheme` | `Bearer` | `GITHUB_TOKEN_TYPE` | Usually leave as-is. |
| `base_url` | `https://api.github.com` | `GITHUB_BASE_URL` | Point at GHES if needed. |
| `user_agent` | `integrations-sdk` | `GITHUB_USER_AGENT` | GitHub requires a UA string. |
| `timeout` | `10.0` | `GITHUB_TIMEOUT` | Seconds. |

## Quick Call

```python
from integrations import Integrations


async def open_issue():
    integrations = Integrations(github={"token": "ghp_..."})
    issue = await integrations.github.create_issue(
        owner="octocat",
        repo="hello-world",
        title="Docs shipped",
    )
    return issue["number"]
```

Highlights: repository utilities (`find_repository`, `create_branch`), pull-request helpers, Codespaces lifecycle, and `raw_request` for any endpoint. Responses keep GitHub's JSON shape; extend the provider if you need something custom.
