"""Action for updating a Google Calendar event."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class UpdateEvent(GoogleCalendarBaseAction):
    """Update selected fields of a Google Calendar event."""

    async def __call__(
        self,
        event_id: str,
        changes: Mapping[str, Any],
        *,
        calendar_id: str | None = None,
        send_updates: str | None = None,
    ) -> MutableMapping[str, Any]:
        if not changes:
            raise ValueError("Provide at least one change to apply")

        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: dict[str, Any] = {}
        if send_updates is not None:
            params["sendUpdates"] = send_updates

        response = await provider.request(
            "PATCH",
            f"/calendars/{calendar}/events/{event_id}",
            params=params or None,
            json=dict(changes),
        )
        return provider.process_httpx_response(response)
