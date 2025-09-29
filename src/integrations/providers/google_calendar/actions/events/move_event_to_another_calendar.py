"""Action for moving a Google Calendar event between calendars."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class MoveEventToAnotherCalendar(GoogleCalendarBaseAction):
    """Move an event from one Google Calendar to another."""

    async def __call__(
        self,
        event_id: str,
        destination_calendar_id: str,
        *,
        source_calendar_id: str | None = None,
        send_updates: str | None = None,
    ) -> MutableMapping[str, Any]:
        provider = self.provider
        source = self.resolve_calendar_id(source_calendar_id)
        params: MutableMapping[str, Any] = {"destination": destination_calendar_id}
        if send_updates is not None:
            params["sendUpdates"] = send_updates

        response = await provider.request(
            "POST",
            f"/calendars/{source}/events/{event_id}/move",
            params=params or None,
        )
        return provider.process_httpx_response(response)
