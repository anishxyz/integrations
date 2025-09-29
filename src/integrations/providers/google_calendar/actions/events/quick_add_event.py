"""Action for quick-adding a Google Calendar event via natural language."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class QuickAddEvent(GoogleCalendarBaseAction):
    """Create an event by letting Google Calendar parse natural language text."""

    async def __call__(
        self,
        text: str,
        *,
        calendar_id: str | None = None,
        send_updates: str | None = None,
        conference_data_version: int | None = None,
    ) -> MutableMapping[str, Any]:
        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: MutableMapping[str, Any] = {"text": text}
        if send_updates is not None:
            params["sendUpdates"] = send_updates
        if conference_data_version is not None:
            params["conferenceDataVersion"] = conference_data_version

        response = await provider.request(
            "POST",
            f"/calendars/{calendar}/events/quickAdd",
            params=params or None,
        )
        return provider.process_httpx_response(response)
