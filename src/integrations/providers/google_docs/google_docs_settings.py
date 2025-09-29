"""Settings for the Google Docs provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class GoogleDocsSettings(ProviderSettings):
    """Configuration options for accessing the Google Docs API."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_DOCS_ACCESS_TOKEN",
            "GOOGLE_DOCS_TOKEN",
            "GOOGLE_TOKEN",
            "GOOGLE_ACCESS_TOKEN",
        ),
    )
    authorization_scheme: str | None = Field(
        default="Bearer",
        validation_alias="GOOGLE_DOCS_AUTHORIZATION_SCHEME",
    )
    base_url: str = Field(
        default="https://docs.googleapis.com/v1",
        validation_alias="GOOGLE_DOCS_BASE_URL",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="GOOGLE_DOCS_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="GOOGLE_DOCS_USER_AGENT",
    )
