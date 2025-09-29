"""Action for retrieving a Google Calendar event."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class RetrieveEventById(GoogleCalendarBaseAction):
    """Retrieve a Google Calendar event by its identifier."""

    async def __call__(
        self,
        event_id: str,
        *,
        calendar_id: str | None = None,
        always_include_email: bool | None = None,
        max_attendees: int | None = None,
        time_zone: str | None = None,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: MutableMapping[str, Any] = {}
        if always_include_email is not None:
            params["alwaysIncludeEmail"] = always_include_email
        if max_attendees is not None:
            params["maxAttendees"] = max_attendees
        if time_zone is not None:
            params["timeZone"] = time_zone
        if fields is not None:
            params["fields"] = fields

        response = await provider.request(
            "GET",
            f"/calendars/{calendar}/events/{event_id}",
            params=params or None,
        )
        return provider.process_httpx_response(response)
