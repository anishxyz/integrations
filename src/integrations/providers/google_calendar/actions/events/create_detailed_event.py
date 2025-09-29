"""Action for creating a detailed Google Calendar event."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_calendar_base_action import GoogleCalendarBaseAction


class CreateDetailedEvent(GoogleCalendarBaseAction):
    """Create an event with explicit start/end and optional metadata."""

    async def __call__(
        self,
        summary: str,
        *,
        start: Mapping[str, Any],
        end: Mapping[str, Any],
        calendar_id: str | None = None,
        description: str | None = None,
        location: str | None = None,
        attendees: Sequence[str | Mapping[str, Any]] | None = None,
        reminders: Mapping[str, Any] | None = None,
        color_id: str | None = None,
        conference_data: Mapping[str, Any] | None = None,
        transparency: str | None = None,
        visibility: str | None = None,
        extended_properties: Mapping[str, Any] | None = None,
        attachments: Sequence[Mapping[str, Any]] | None = None,
        send_updates: str | None = None,
        conference_data_version: int | None = None,
        supports_attachments: bool | None = None,
        extra_body: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        body: MutableMapping[str, Any] = {
            "summary": summary,
            "start": dict(start),
            "end": dict(end),
        }
        if description is not None:
            body["description"] = description
        if location is not None:
            body["location"] = location
        if attendees is not None:
            normalized = [self.normalize_attendee(att) for att in attendees]
            body["attendees"] = normalized
        if reminders is not None:
            body["reminders"] = dict(reminders)
        if color_id is not None:
            body["colorId"] = color_id
        if conference_data is not None:
            body["conferenceData"] = dict(conference_data)
        if transparency is not None:
            body["transparency"] = transparency
        if visibility is not None:
            body["visibility"] = visibility
        if extended_properties is not None:
            body["extendedProperties"] = dict(extended_properties)
        if attachments is not None:
            body["attachments"] = [dict(attachment) for attachment in attachments]
        if extra_body is not None:
            body.update(dict(extra_body))

        params: MutableMapping[str, Any] = {}
        if send_updates is not None:
            params["sendUpdates"] = send_updates
        if conference_data_version is not None:
            params["conferenceDataVersion"] = conference_data_version
        if supports_attachments is not None:
            params["supportsAttachments"] = supports_attachments

        response = await provider.request(
            "POST",
            f"/calendars/{calendar}/events",
            params=params or None,
            json=body,
        )
        return provider.process_httpx_response(response)
