"""Google Workspace credential models."""

from __future__ import annotations

from collections.abc import Mapping as TypingMapping, Sequence
from typing import Any

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from integrations.auth.flows import OAuth2AppCredentials, OAuth2Token

GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


class GoogleAppCredentials(OAuth2AppCredentials):
    """OAuth2 configuration shared across Google providers."""

    authorization_url: str | None = Field(
        default=GOOGLE_AUTHORIZATION_URL,
        validation_alias=AliasChoices(
            "GOOGLE_AUTHORIZATION_URL",
            "GOOGLE_AUTHORIZE_URL",
        ),
    )
    token_url: str | None = Field(
        default=GOOGLE_TOKEN_URL,
        validation_alias=AliasChoices("GOOGLE_TOKEN_URL", "GOOGLE_ACCESS_TOKEN_URL"),
    )
    client_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_CLIENT_ID",
            "GOOGLE_OAUTH_CLIENT_ID",
        ),
    )
    client_secret: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_CLIENT_SECRET",
            "GOOGLE_OAUTH_CLIENT_SECRET",
        ),
    )
    redirect_uri: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_REDIRECT_URI",
            "GOOGLE_OAUTH_REDIRECT_URI",
        ),
    )
    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_TOKEN",
            "GOOGLE_ACCESS_TOKEN",
        ),
    )
    refresh_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_REFRESH_TOKEN",
            "GOOGLE_OAUTH_REFRESH_TOKEN",
        ),
    )
    default_scope: Sequence[str] | str | None = Field(default=None)
    client_kwargs: TypingMapping[str, Any] | None = None

    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class GoogleUserCredentials(OAuth2Token):
    """User credentials produced by Google OAuth flows."""

    refresh_token: str | None = None


__all__ = ["GoogleAppCredentials", "GoogleUserCredentials"]
