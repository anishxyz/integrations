"""Settings for the Google Drive provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class GoogleDriveSettings(ProviderSettings):
    """Configuration model for Google Drive access."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_DRIVE_ACCESS_TOKEN",
            "GOOGLE_DRIVE_TOKEN",
            "GOOGLE_TOKEN",
            "GOOGLE_ACCESS_TOKEN",
        ),
    )
    authorization_scheme: str | None = Field(
        default="Bearer",
        validation_alias="GOOGLE_DRIVE_AUTHORIZATION_SCHEME",
    )
    base_url: str = Field(
        default="https://www.googleapis.com/drive/v3",
        validation_alias="GOOGLE_DRIVE_BASE_URL",
    )
    upload_base_url: str = Field(
        default="https://www.googleapis.com/upload/drive/v3",
        validation_alias="GOOGLE_DRIVE_UPLOAD_BASE_URL",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="GOOGLE_DRIVE_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="GOOGLE_DRIVE_USER_AGENT",
    )
    default_drive_id: str | None = Field(
        default=None,
        validation_alias="GOOGLE_DRIVE_DEFAULT_DRIVE_ID",
    )
    default_parent_id: str | None = Field(
        default=None,
        validation_alias="GOOGLE_DRIVE_DEFAULT_PARENT_ID",
    )
