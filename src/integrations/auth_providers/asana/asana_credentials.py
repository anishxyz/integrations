"""Asana-specific credential models."""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from integrations.auth.flows import OAuth2AppCredentials, OAuth2Token

ASANA_AUTHORIZATION_URL = "https://app.asana.com/-/oauth_authorize"
ASANA_TOKEN_URL = "https://app.asana.com/-/oauth_token"


class AsanaAppCredentials(OAuth2AppCredentials):
    """Static credentials for the Asana auth provider."""

    authorization_url: str | None = Field(
        default=ASANA_AUTHORIZATION_URL,
        validation_alias=AliasChoices(
            "ASANA_AUTHORIZATION_URL",
            "ASANA_AUTHORIZE_URL",
        ),
    )
    token_url: str | None = Field(
        default=ASANA_TOKEN_URL,
        validation_alias=AliasChoices("ASANA_TOKEN_URL", "ASANA_ACCESS_TOKEN_URL"),
    )
    client_id: str | None = Field(default=None, validation_alias="ASANA_CLIENT_ID")
    client_secret: str | None = Field(
        default=None, validation_alias="ASANA_CLIENT_SECRET"
    )
    redirect_uri: str | None = Field(
        default=None, validation_alias="ASANA_REDIRECT_URI"
    )
    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "ASANA_ACCESS_TOKEN",
            "ASANA_PERSONAL_ACCESS_TOKEN",
            "ASANA_TOKEN",
        ),
    )
    default_scope: Sequence[str] | str | None = Field(default=None)
    workspace_gid: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "ASANA_WORKSPACE_GID",
            "ASANA_WORKSPACE",
        ),
    )

    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class AsanaUserCredentials(OAuth2Token):
    """Persisted user token payload for Asana."""

    workspace_gid: str | None = None


__all__ = ["AsanaAppCredentials", "AsanaUserCredentials"]
