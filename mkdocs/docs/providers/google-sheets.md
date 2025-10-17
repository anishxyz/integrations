# Google Sheets

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `GOOGLE_SHEETS_ACCESS_TOKEN`<br>`GOOGLE_SHEETS_TOKEN`<br>`GOOGLE_TOKEN`<br>`GOOGLE_ACCESS_TOKEN` | OAuth token with Sheets scope. |
| `authorization_scheme` | `Bearer` | `GOOGLE_SHEETS_AUTHORIZATION_SCHEME` | Adjust only if headers must change. |
| `base_url` | `https://sheets.googleapis.com/v4/spreadsheets` | `GOOGLE_SHEETS_BASE_URL` | API base. |
| `timeout` | `10.0` | `GOOGLE_SHEETS_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `GOOGLE_SHEETS_USER_AGENT` | Optional. |
| `default_spreadsheet_id` | `None` | `GOOGLE_SHEETS_DEFAULT_SPREADSHEET_ID`<br>`GOOGLE_SHEETS_SPREADSHEET_ID` | Used when actions omit the spreadsheet. |

## Quick Call

```python
from integrations import Integrations


async def append_row():
    integrations = Integrations(google_sheets={"token": "ya29..."})
    await integrations.google_sheets.create_spreadsheet_row(
        spreadsheet_id="1A2B...",
        worksheet_title="Summary",
        values=["Docs", "Shipped"],
    )
```

Sheets helpers cover formatting, lookups, conditional rules, and bulk updates. `raw_request` remains available for niche endpoints.
