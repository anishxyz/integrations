"""Settings for the Gmail provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class GmailSettings(ProviderSettings):
    """Configuration for authenticating and calling the Gmail API."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GMAIL_TOKEN",
            "GMAIL_ACCESS_TOKEN",
            "GOOGLE_TOKEN",
            "GOOGLE_ACCESS_TOKEN",
        ),
    )
    authorization_scheme: str = Field(
        default="Bearer",
        validation_alias="GMAIL_TOKEN_TYPE",
    )
    base_url: str = Field(
        default="https://gmail.googleapis.com/gmail/v1",
        validation_alias="GMAIL_BASE_URL",
    )
    user_id: str = Field(default="me", validation_alias="GMAIL_USER_ID")
    timeout: float | None = Field(default=10.0, validation_alias="GMAIL_TIMEOUT")
