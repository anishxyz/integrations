"""Action for creating a Google Calendar."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class CreateCalendar(GoogleCalendarBaseAction):
    """Create a new Google Calendar for the authenticated user."""

    async def __call__(
        self,
        summary: str,
        *,
        description: str | None = None,
        time_zone: str | None = None,
        location: str | None = None,
        extra_properties: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        body: MutableMapping[str, Any] = {"summary": summary}
        if description is not None:
            body["description"] = description
        if time_zone is not None:
            body["timeZone"] = time_zone
        if location is not None:
            body["location"] = location
        if extra_properties is not None:
            body.update(dict(extra_properties))

        response = await self.provider.request("POST", "/calendars", json=body)
        return self.provider.process_httpx_response(response)
