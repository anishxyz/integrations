"""Settings for the Google Calendar provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class GoogleCalendarSettings(ProviderSettings):
    """Configuration options for accessing the Google Calendar API."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_CALENDAR_ACCESS_TOKEN",
            "GOOGLE_CALENDAR_TOKEN",
            "GOOGLE_TOKEN",
            "GOOGLE_ACCESS_TOKEN",
        ),
    )
    authorization_scheme: str | None = Field(
        default="Bearer",
        validation_alias="GOOGLE_CALENDAR_AUTHORIZATION_SCHEME",
    )
    base_url: str = Field(
        default="https://www.googleapis.com/calendar/v3",
        validation_alias="GOOGLE_CALENDAR_BASE_URL",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="GOOGLE_CALENDAR_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="GOOGLE_CALENDAR_USER_AGENT",
    )
    default_calendar_id: str | None = Field(
        default=None,
        validation_alias="GOOGLE_CALENDAR_DEFAULT_CALENDAR_ID",
    )
