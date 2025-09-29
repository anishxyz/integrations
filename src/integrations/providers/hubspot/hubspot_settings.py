"""Settings for the HubSpot provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class HubspotSettings(ProviderSettings):
    """Configuration for the HubSpot provider."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    access_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "HUBSPOT_ACCESS_TOKEN",
            "HUBSPOT_TOKEN",
            "HUBSPOT_PRIVATE_APP_TOKEN",
        ),
    )
    base_url: str = Field(
        default="https://api.hubapi.com",
        validation_alias="HUBSPOT_BASE_URL",
    )
    timeout: float | None = Field(
        default=15.0,
        validation_alias="HUBSPOT_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="HUBSPOT_USER_AGENT",
    )
