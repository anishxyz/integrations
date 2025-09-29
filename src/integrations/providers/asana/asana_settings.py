"""Settings for the Asana provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class AsanaSettings(ProviderSettings):
    """Configuration model for Asana API access."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "ASANA_ACCESS_TOKEN",
            "ASANA_PERSONAL_ACCESS_TOKEN",
            "ASANA_TOKEN",
        ),
    )
    workspace_gid: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "ASANA_WORKSPACE_GID",
            "ASANA_WORKSPACE",
        ),
    )
    base_url: str = Field(
        default="https://app.asana.com/api/1.0",
        validation_alias="ASANA_BASE_URL",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="ASANA_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="ASANA_USER_AGENT",
    )
