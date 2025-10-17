# Google Drive

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `GOOGLE_DRIVE_ACCESS_TOKEN`<br>`GOOGLE_DRIVE_TOKEN`<br>`GOOGLE_TOKEN`<br>`GOOGLE_ACCESS_TOKEN` | OAuth token with Drive scope. |
| `authorization_scheme` | `Bearer` | `GOOGLE_DRIVE_AUTHORIZATION_SCHEME` | Change only if you alter auth headers. |
| `base_url` | `https://www.googleapis.com/drive/v3` | `GOOGLE_DRIVE_BASE_URL` | Core API endpoint. |
| `upload_base_url` | `https://www.googleapis.com/upload/drive/v3` | `GOOGLE_DRIVE_UPLOAD_BASE_URL` | Used automatically for uploads. |
| `timeout` | `10.0` | `GOOGLE_DRIVE_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `GOOGLE_DRIVE_USER_AGENT` | Optional. |
| `default_drive_id` | `None` | `GOOGLE_DRIVE_DEFAULT_DRIVE_ID` | Set when you work inside a shared drive. |
| `default_parent_id` | `None` | `GOOGLE_DRIVE_DEFAULT_PARENT_ID` | Used when actions omit a parent folder. |

## Quick Call

```python
from integrations import Integrations


async def upload_text():
    integrations = Integrations(google_drive={"token": "ya29..."})
    file = await integrations.google_drive.create_file_from_text(
        name="release-notes.txt",
        content="Docs shipped.",
        mime_type="text/plain",
    )
    return file["id"]
```

Drive actions cover uploads, conversions, sharing, and lookup helpers. Reach for `raw_request` to call any endpoint directly.
