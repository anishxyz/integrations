from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Mapping as TypingMapping

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from integrations.auth.flows import OAuth2AppCredentials, OAuth2Token

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"


class GithubAppCredentials(OAuth2AppCredentials):
    """GitHub-specific defaults for OAuth2 flows."""

    authorization_url: str | None = Field(
        default=GITHUB_AUTHORIZE_URL,
        validation_alias=AliasChoices(
            "GITHUB_AUTHORIZATION_URL", "GITHUB_AUTHORIZE_URL"
        ),
    )
    token_url: str | None = Field(
        default=GITHUB_TOKEN_URL, validation_alias=AliasChoices("GITHUB_TOKEN_URL")
    )
    client_id: str | None = Field(default=None, validation_alias="GITHUB_CLIENT_ID")
    client_secret: str | None = Field(
        default=None, validation_alias="GITHUB_CLIENT_SECRET"
    )
    redirect_uri: str | None = Field(
        default=None, validation_alias="GITHUB_REDIRECT_URI"
    )
    token: str | None = Field(
        default=None, validation_alias=AliasChoices("GITHUB_TOKEN", "GITHUB_API_TOKEN")
    )
    default_scope: Sequence[str] | str | None = Field(default=None)
    client_kwargs: TypingMapping[str, Any] | None = None
    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class GithubUserCredentials(OAuth2Token):
    """User credentials for GitHub auth (OAuth2 or PAT)."""

    access_token: str | None = None
    token_type: str | None = "Bearer"
    refresh_token: str | None = None
    scope: tuple[str, ...] | None = None
    expires_in: int | None = None
    expires_at: float | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
