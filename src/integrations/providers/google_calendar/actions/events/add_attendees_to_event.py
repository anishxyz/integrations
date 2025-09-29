"""Action for adding attendees to an existing event."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_calendar_base_action import GoogleCalendarBaseAction


class AddAttendeesToEvent(GoogleCalendarBaseAction):
    """Invite one or more attendees to an existing Google Calendar event."""

    async def __call__(
        self,
        event_id: str,
        attendees: Sequence[str | Mapping[str, Any]],
        *,
        calendar_id: str | None = None,
        send_updates: str | None = "all",
        always_include_email: bool = True,
        max_attendees: int | None = None,
    ) -> MutableMapping[str, Any]:
        if not attendees:
            raise ValueError("Provide at least one attendee to add")

        provider = self.provider
        calendar = self.resolve_calendar_id(calendar_id)
        params: MutableMapping[str, Any] = {"fields": "attendees"}
        if always_include_email is not None:
            params["alwaysIncludeEmail"] = always_include_email
        if max_attendees is not None:
            params["maxAttendees"] = max_attendees

        response = await provider.request(
            "GET",
            f"/calendars/{calendar}/events/{event_id}",
            params=params or None,
        )
        existing_event = provider.process_httpx_response(response)

        existing_attendees_raw = existing_event.get("attendees") or []
        existing_attendees: list[MutableMapping[str, Any]] = [
            dict(attendee)
            for attendee in existing_attendees_raw
            if isinstance(attendee, Mapping)
        ]
        existing_emails = {
            attendee.get("email", "").lower()
            for attendee in existing_attendees
            if isinstance(attendee.get("email"), str)
        }

        new_attendees = [self.normalize_attendee(att) for att in attendees]
        combined = self.deduplicate_attendees(existing_attendees + new_attendees)
        added_attendees = [
            attendee
            for attendee in new_attendees
            if attendee.get("email", "").lower() not in existing_emails
        ]

        patch_params: MutableMapping[str, Any] = {}
        if send_updates is not None:
            patch_params["sendUpdates"] = send_updates

        response = await provider.request(
            "PATCH",
            f"/calendars/{calendar}/events/{event_id}",
            params=patch_params or None,
            json={"attendees": combined},
        )
        updated_event = provider.process_httpx_response(response)
        return {
            "event": updated_event,
            "added_count": len(added_attendees),
            "added_attendees": added_attendees,
        }
