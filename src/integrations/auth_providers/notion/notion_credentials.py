"""Notion credential models."""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from integrations.auth.flows import OAuth2AppCredentials, OAuth2Token

NOTION_AUTHORIZATION_URL = "https://api.notion.com/v1/oauth/authorize"
NOTION_TOKEN_URL = "https://api.notion.com/v1/oauth/token"


class NotionAppCredentials(OAuth2AppCredentials):
    """Static configuration for Notion auth."""

    authorization_url: str | None = Field(
        default=NOTION_AUTHORIZATION_URL,
        validation_alias=AliasChoices(
            "NOTION_AUTHORIZATION_URL",
            "NOTION_AUTHORIZE_URL",
        ),
    )
    token_url: str | None = Field(
        default=NOTION_TOKEN_URL,
        validation_alias=AliasChoices("NOTION_TOKEN_URL", "NOTION_ACCESS_TOKEN_URL"),
    )
    client_id: str | None = Field(default=None, validation_alias="NOTION_CLIENT_ID")
    client_secret: str | None = Field(
        default=None,
        validation_alias="NOTION_CLIENT_SECRET",
    )
    redirect_uri: str | None = Field(
        default=None, validation_alias="NOTION_REDIRECT_URI"
    )
    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("NOTION_TOKEN", "NOTION_INTEGRATION_TOKEN"),
    )
    default_scope: Sequence[str] | str | None = Field(default=None)
    version: str | None = Field(
        default=None,
        validation_alias=AliasChoices("NOTION_VERSION", "NOTION_API_VERSION"),
    )

    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class NotionUserCredentials(OAuth2Token):
    """User credentials for Notion OAuth."""

    workspace_id: str | None = None
    workspace_name: str | None = None
    workspace_icon: str | None = None


__all__ = ["NotionAppCredentials", "NotionUserCredentials"]
