"""Google Calendar provider package."""

from ...core import ProviderKey, register_provider
from .google_calendar_provider import GoogleCalendarProvider
from .google_calendar_settings import GoogleCalendarSettings

register_provider(ProviderKey.GOOGLE_CALENDAR, GoogleCalendarProvider)

__all__ = ["GoogleCalendarProvider", "GoogleCalendarSettings"]
