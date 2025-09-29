"""Action for listing Google Calendars accessible to the user."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class FindCalendars(GoogleCalendarBaseAction):
    """Retrieve calendars accessible to the authenticated user."""

    async def __call__(
        self,
        *,
        min_access_role: str | None = None,
        show_deleted: bool | None = None,
        show_hidden: bool | None = None,
        max_results: int | None = None,
        page_token: str | None = None,
        sync_token: str | None = None,
        params_override: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        params: MutableMapping[str, Any] = {}
        if min_access_role is not None:
            params["minAccessRole"] = min_access_role
        if show_deleted is not None:
            params["showDeleted"] = show_deleted
        if show_hidden is not None:
            params["showHidden"] = show_hidden
        if max_results is not None:
            params["maxResults"] = max_results
        if page_token is not None:
            params["pageToken"] = page_token
        if sync_token is not None:
            params["syncToken"] = sync_token
        if params_override is not None:
            params.update(dict(params_override))

        response = await self.provider.request(
            "GET",
            "/users/me/calendarList",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
