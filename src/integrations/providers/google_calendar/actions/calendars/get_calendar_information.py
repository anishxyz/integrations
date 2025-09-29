"""Action for retrieving Google Calendar metadata."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class GetCalendarInformation(GoogleCalendarBaseAction):
    """Retrieve metadata about a specific Google Calendar."""

    async def __call__(
        self,
        *,
        calendar_id: str | None = None,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        calendar = self.resolve_calendar_id(calendar_id)
        params: MutableMapping[str, Any] = {}
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "GET",
            f"/calendars/{calendar}",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
