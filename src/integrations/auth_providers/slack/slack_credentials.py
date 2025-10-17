"""Slack credential models."""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from integrations.auth.flows import OAuth2AppCredentials, OAuth2Token

SLACK_AUTHORIZATION_URL = "https://slack.com/oauth/v2/authorize"
SLACK_TOKEN_URL = "https://slack.com/api/oauth.v2.access"


class SlackAppCredentials(OAuth2AppCredentials):
    """Static configuration for Slack OAuth or token-based auth."""

    authorization_url: str | None = Field(
        default=SLACK_AUTHORIZATION_URL,
        validation_alias=AliasChoices(
            "SLACK_AUTHORIZATION_URL",
            "SLACK_AUTHORIZE_URL",
        ),
    )
    token_url: str | None = Field(
        default=SLACK_TOKEN_URL,
        validation_alias=AliasChoices("SLACK_TOKEN_URL", "SLACK_ACCESS_TOKEN_URL"),
    )
    client_id: str | None = Field(default=None, validation_alias="SLACK_CLIENT_ID")
    client_secret: str | None = Field(
        default=None,
        validation_alias="SLACK_CLIENT_SECRET",
    )
    redirect_uri: str | None = Field(
        default=None, validation_alias="SLACK_REDIRECT_URI"
    )
    bot_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SLACK_BOT_TOKEN", "SLACK_TOKEN"),
    )
    user_token: str | None = Field(
        default=None,
        validation_alias="SLACK_USER_TOKEN",
    )
    default_scope: Sequence[str] | str | None = Field(default=None)

    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class SlackUserCredentials(OAuth2Token):
    """User credential payload produced by Slack OAuth."""

    bot_user_id: str | None = None
    team_id: str | None = None
    team_name: str | None = None
    authed_user_id: str | None = None
    access_token: str


__all__ = ["SlackAppCredentials", "SlackUserCredentials"]
