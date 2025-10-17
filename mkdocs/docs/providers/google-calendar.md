# Google Calendar

## Settings

| Field | Default | Env keys | Notes |
| --- | --- | --- | --- |
| `token` | `None` | `GOOGLE_CALENDAR_ACCESS_TOKEN`<br>`GOOGLE_CALENDAR_TOKEN`<br>`GOOGLE_TOKEN`<br>`GOOGLE_ACCESS_TOKEN` | OAuth token with calendar scopes. |
| `authorization_scheme` | `Bearer` | `GOOGLE_CALENDAR_AUTHORIZATION_SCHEME` | Adjust only for custom auth. |
| `base_url` | `https://www.googleapis.com/calendar/v3` | `GOOGLE_CALENDAR_BASE_URL` | Override for mocks. |
| `timeout` | `10.0` | `GOOGLE_CALENDAR_TIMEOUT` | Seconds. |
| `user_agent` | `integrations-sdk` | `GOOGLE_CALENDAR_USER_AGENT` | Optional. |
| `default_calendar_id` | `None` | `GOOGLE_CALENDAR_DEFAULT_CALENDAR_ID` | Used when actions omit the calendar. |

## Quick Call

```python
from integrations import Integrations


async def block_time():
    integrations = Integrations(google_calendar={"token": "ya29..."})
    event = await integrations.google_calendar.find_or_create_event(
        calendar_id="primary",
        summary="Pairing session",
        start_time="2024-05-01T16:00:00Z",
        end_time="2024-05-01T17:00:00Z",
    )
    return event["id"]
```

Calendar utilities include `find_busy_periods`, `quick_add_event`, and `raw_request` for anything outside the high-level surface. JSON errors bubble up with readable messages.
