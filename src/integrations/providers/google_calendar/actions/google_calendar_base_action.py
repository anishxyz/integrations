"""Shared helpers for Google Calendar actions."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping
from typing import TYPE_CHECKING, Any

from integrations.core.actions import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoid runtime import cycle
    from ..google_calendar_provider import GoogleCalendarProvider


class GoogleCalendarBaseAction(BaseAction):
    """Base class exposing reusable Google Calendar helpers."""

    provider: "GoogleCalendarProvider"

    def resolve_calendar_id(self, calendar_id: str | None) -> str:
        if calendar_id:
            return calendar_id
        settings = self.provider.settings
        if settings.default_calendar_id:
            return settings.default_calendar_id
        return "primary"

    def normalize_attendee(
        self, attendee: str | Mapping[str, Any]
    ) -> MutableMapping[str, Any]:
        if isinstance(attendee, str):
            return {"email": attendee}
        normalized = dict(attendee)
        if "email" not in normalized:
            raise ValueError("Attendee mapping must include an 'email' value")
        return normalized

    def deduplicate_attendees(
        self, attendees: Iterable[Mapping[str, Any]]
    ) -> list[MutableMapping[str, Any]]:
        seen: dict[str, MutableMapping[str, Any]] = {}
        for attendee in attendees:
            normalized = dict(attendee)
            email = normalized.get("email")
            if not isinstance(email, str):
                raise ValueError("Attendee entries must include an 'email' string")
            seen[email.lower()] = normalized
        return list(seen.values())
