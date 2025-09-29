"""Action for finding Google Calendar events."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class FindEvents(GoogleCalendarBaseAction):
    """Search for events on a Google Calendar."""

    async def __call__(
        self,
        *,
        calendar_id: str | None = None,
        query: str | None = None,
        time_min: str | None = None,
        time_max: str | None = None,
        max_results: int | None = None,
        single_events: bool | None = None,
        order_by: str | None = None,
        show_deleted: bool | None = None,
        show_hidden_invitees: bool | None = None,
        time_zone: str | None = None,
        updated_min: str | None = None,
        i_cal_uid: str | None = None,
        sync_token: str | None = None,
        page_token: str | None = None,
        params_override: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: MutableMapping[str, Any] = {}
        if query is not None:
            params["q"] = query
        if time_min is not None:
            params["timeMin"] = time_min
        if time_max is not None:
            params["timeMax"] = time_max
        if max_results is not None:
            params["maxResults"] = max_results
        if single_events is not None:
            params["singleEvents"] = single_events
        if order_by is not None:
            params["orderBy"] = order_by
        if show_deleted is not None:
            params["showDeleted"] = show_deleted
        if show_hidden_invitees is not None:
            params["showHiddenInvitations"] = show_hidden_invitees
        if time_zone is not None:
            params["timeZone"] = time_zone
        if updated_min is not None:
            params["updatedMin"] = updated_min
        if i_cal_uid is not None:
            params["iCalUID"] = i_cal_uid
        if sync_token is not None:
            params["syncToken"] = sync_token
        if page_token is not None:
            params["pageToken"] = page_token
        if params_override is not None:
            params.update(dict(params_override))

        response = await provider.request(
            "GET",
            f"/calendars/{calendar}/events",
            params=params or None,
        )
        return provider.process_httpx_response(response)
