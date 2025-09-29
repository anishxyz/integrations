"""Action for deleting a Google Calendar event."""

from __future__ import annotations

from typing import Any

from ..google_calendar_base_action import GoogleCalendarBaseAction


class DeleteEvent(GoogleCalendarBaseAction):
    """Delete an event from a Google Calendar."""

    async def __call__(
        self,
        event_id: str,
        *,
        calendar_id: str | None = None,
        send_updates: str | None = None,
    ) -> dict[str, bool]:
        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: dict[str, Any] = {}
        if send_updates is not None:
            params["sendUpdates"] = send_updates

        response = await provider.request(
            "DELETE",
            f"/calendars/{calendar}/events/{event_id}",
            params=params or None,
        )
        provider.process_httpx_response(response)
        return {"deleted": True}
