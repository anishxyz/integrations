"""Settings for the Slack provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class SlackSettings(ProviderSettings):
    """Configuration for the Slack provider."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "SLACK_BOT_TOKEN",
            "SLACK_TOKEN",
            "SLACK_USER_TOKEN",
        ),
    )
    base_url: str = Field(
        default="https://slack.com/api",
        validation_alias="SLACK_BASE_URL",
    )
    user_agent: str = Field(
        default="integrations-sdk",
        validation_alias="SLACK_USER_AGENT",
    )
    timeout: float | None = Field(
        default=10.0,
        validation_alias="SLACK_TIMEOUT",
    )
