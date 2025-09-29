"""Google Calendar provider implementation."""

from __future__ import annotations

from typing import Any, MutableMapping

import httpx

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddAttendeesToEvent,
    CreateCalendar,
    CreateDetailedEvent,
    DeleteEvent,
    FindBusyPeriods,
    FindCalendars,
    FindEvents,
    FindOrCreateEvent,
    GetCalendarInformation,
    MoveEventToAnotherCalendar,
    QuickAddEvent,
    RetrieveEventById,
    UpdateEvent,
)
from .google_calendar_settings import GoogleCalendarSettings


class GoogleCalendarProvider(HttpxClientMixin, BaseProvider[GoogleCalendarSettings]):
    """Provider exposing Google Calendar scheduling operations."""

    settings_class = GoogleCalendarSettings

    add_attendees_to_event: AddAttendeesToEvent
    delete_event: DeleteEvent
    quick_add_event: QuickAddEvent
    update_event: UpdateEvent
    retrieve_event_by_id: RetrieveEventById
    find_busy_periods: FindBusyPeriods
    get_calendar_information: GetCalendarInformation
    create_calendar: CreateCalendar
    create_detailed_event: CreateDetailedEvent
    move_event_to_another_calendar: MoveEventToAnotherCalendar
    raw_request: RawHttpRequestAction
    find_events: FindEvents
    find_calendars: FindCalendars
    find_or_create_event: FindOrCreateEvent

    add_attendees_to_event = action(
        AddAttendeesToEvent,
        description="Invite attendees to an existing Google Calendar event.",
    )
    delete_event = action(
        DeleteEvent,
        description="Delete a Google Calendar event.",
    )
    quick_add_event = action(
        QuickAddEvent,
        description="Create an event from natural language text.",
    )
    update_event = action(
        UpdateEvent,
        description="Update fields on a Google Calendar event.",
    )
    retrieve_event_by_id = action(
        RetrieveEventById,
        description="Retrieve a Google Calendar event by its identifier.",
    )
    find_busy_periods = action(
        FindBusyPeriods,
        description="Find busy time periods across calendars.",
    )
    get_calendar_information = action(
        GetCalendarInformation,
        description="Retrieve metadata for a Google Calendar.",
    )
    create_calendar = action(
        CreateCalendar,
        description="Create a new Google Calendar.",
    )
    create_detailed_event = action(
        CreateDetailedEvent,
        description="Create a detailed Google Calendar event.",
    )
    move_event_to_another_calendar = action(
        MoveEventToAnotherCalendar,
        description="Move a Google Calendar event to another calendar.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Execute a raw Google Calendar API request (beta).",
    )
    find_events = action(
        FindEvents,
        description="Find events on a Google Calendar.",
    )
    find_calendars = action(
        FindCalendars,
        description="List calendars accessible to the user.",
    )
    find_or_create_event = action(
        FindOrCreateEvent,
        description="Find an event or create it when missing.",
    )

    def httpx_headers(self) -> MutableMapping[str, str]:
        token = self.settings.token
        if not token:
            raise ValueError("Google Calendar access token is required")
        scheme = self.settings.authorization_scheme or "Bearer"
        headers: MutableMapping[str, str] = {
            "Authorization": f"{scheme} {token}".strip(),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        user_agent = self.settings.user_agent
        if user_agent:
            headers["User-Agent"] = user_agent
        return headers

    def process_httpx_response(self, response: httpx.Response) -> Any:
        def fallback(resp: httpx.Response) -> dict[str, str]:
            return {"value": resp.text}

        payload = self.parse_httpx_response(
            response,
            require_json=True,
            fallback=fallback,
        )
        return self.postprocess_httpx_payload(payload)
