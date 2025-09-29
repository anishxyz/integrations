"""Settings for the Github provider."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from ...core import ProviderSettings


class GithubSettings(ProviderSettings):
    """Configuration for the Github provider."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)

    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GITHUB_TOKEN",
            "GITHUB_PAT",
            "GITHUB_OAUTH_TOKEN",
            "GITHUB_APP_TOKEN",
        ),
    )
    authorization_scheme: str = Field(
        default="Bearer",
        validation_alias="GITHUB_TOKEN_TYPE",
    )
    base_url: str = Field(
        default="https://api.github.com",
        validation_alias="GITHUB_BASE_URL",
    )
    user_agent: str = Field(
        default="integrations-sdk", validation_alias="GITHUB_USER_AGENT"
    )
    timeout: float | None = Field(default=10.0, validation_alias="GITHUB_TIMEOUT")
