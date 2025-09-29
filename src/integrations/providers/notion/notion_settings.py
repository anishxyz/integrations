"""Settings for the Notion provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class NotionSettings(ProviderSettings):
    """Configuration for the Notion provider."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "NOTION_TOKEN",
            "NOTION_INTEGRATION_TOKEN",
        ),
    )
    version: str = Field(
        default="2022-06-28",
        validation_alias=AliasChoices(
            "NOTION_VERSION",
            "NOTION_API_VERSION",
        ),
    )
    base_url: str = Field(
        default="https://api.notion.com/v1",
        validation_alias="NOTION_BASE_URL",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="NOTION_TIMEOUT",
    )
    user_agent: str | None = Field(
        default="integrations-sdk",
        validation_alias="NOTION_USER_AGENT",
    )
