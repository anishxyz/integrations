"""Action for finding or creating a Google Calendar event."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_calendar_base_action import GoogleCalendarBaseAction


class FindOrCreateEvent(GoogleCalendarBaseAction):
    """Find an event or create it when no match exists."""

    async def __call__(
        self,
        *,
        calendar_id: str | None = None,
        search_query: str | None = None,
        search_params: Mapping[str, Any] | None = None,
        event_body: Mapping[str, Any] | None = None,
        summary: str | None = None,
        start: Mapping[str, Any] | None = None,
        end: Mapping[str, Any] | None = None,
        send_updates: str | None = None,
        conference_data_version: int | None = None,
        supports_attachments: bool | None = None,
    ) -> MutableMapping[str, Any]:
        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: MutableMapping[str, Any] = {
            "maxResults": 1,
            "singleEvents": True,
        }
        if search_params is not None:
            params.update(dict(search_params))
        if search_query is not None:
            params.setdefault("q", search_query)

        response = await provider.request(
            "GET",
            f"/calendars/{calendar}/events",
            params=params or None,
        )
        events = provider.process_httpx_response(response)
        items = events.get("items") or []
        if items:
            first = items[0]
            if isinstance(first, Mapping):
                return {"created": False, "event": dict(first)}
            return {"created": False, "event": first}

        if event_body is None:
            if summary is None or start is None or end is None:
                raise ValueError(
                    "Provide an 'event_body' mapping or summary/start/end details to create the event"
                )
            body: MutableMapping[str, Any] = {
                "summary": summary,
                "start": dict(start),
                "end": dict(end),
            }
        else:
            body = dict(event_body)

        request_params: MutableMapping[str, Any] = {}
        if send_updates is not None:
            request_params["sendUpdates"] = send_updates
        if conference_data_version is not None:
            request_params["conferenceDataVersion"] = conference_data_version
        if supports_attachments is not None:
            request_params["supportsAttachments"] = supports_attachments

        response = await provider.request(
            "POST",
            f"/calendars/{calendar}/events",
            params=request_params or None,
            json=body,
        )
        created = provider.process_httpx_response(response)
        return {"created": True, "event": created}
