"""Settings for the Google Sheets provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class GoogleSheetsSettings(ProviderSettings):
    """Configuration options for Google Sheets access."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_SHEETS_ACCESS_TOKEN",
            "GOOGLE_SHEETS_TOKEN",
            "GOOGLE_TOKEN",
            "GOOGLE_ACCESS_TOKEN",
        ),
    )
    authorization_scheme: str | None = Field(
        default="Bearer",
        validation_alias="GOOGLE_SHEETS_AUTHORIZATION_SCHEME",
    )
    base_url: str = Field(
        default="https://sheets.googleapis.com/v4/spreadsheets",
        validation_alias="GOOGLE_SHEETS_BASE_URL",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="GOOGLE_SHEETS_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="GOOGLE_SHEETS_USER_AGENT",
    )
    default_spreadsheet_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_SHEETS_DEFAULT_SPREADSHEET_ID",
            "GOOGLE_SHEETS_SPREADSHEET_ID",
        ),
    )
