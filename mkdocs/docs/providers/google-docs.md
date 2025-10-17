# Google Docs

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `GOOGLE_DOCS_ACCESS_TOKEN`<br>`GOOGLE_DOCS_TOKEN`<br>`GOOGLE_TOKEN`<br>`GOOGLE_ACCESS_TOKEN` | OAuth token with docs scope. |
| `authorization_scheme` | `Bearer` | `GOOGLE_DOCS_AUTHORIZATION_SCHEME` | Change only for custom auth. |
| `base_url` | `https://docs.googleapis.com/v1` | `GOOGLE_DOCS_BASE_URL` | Override for mocks. |
| `timeout` | `10.0` | `GOOGLE_DOCS_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `GOOGLE_DOCS_USER_AGENT` | Optional. |

## Quick Call

```python
from integrations import Integrations


async def append_text():
    integrations = Integrations(google_docs={"token": "ya29..."})
    await integrations.google_docs.append_text_to_document(
        document_id="1A2B...",
        text="Release notes updated.",
    )
```

Use helpers like `insert_text`, `find_and_replace_text`, `format_text`, or fall back to `raw_request` for uncommon operations.
