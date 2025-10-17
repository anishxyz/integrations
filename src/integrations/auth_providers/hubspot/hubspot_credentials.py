"""HubSpot credential models."""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict

from integrations.auth.flows import OAuth2AppCredentials, OAuth2Token

HUBSPOT_AUTHORIZATION_URL = "https://app.hubspot.com/oauth/authorize"
HUBSPOT_TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"


class HubspotAppCredentials(OAuth2AppCredentials):
    """Configuration for HubSpot OAuth flows or private app tokens."""

    authorization_url: str | None = Field(
        default=HUBSPOT_AUTHORIZATION_URL,
        validation_alias=AliasChoices(
            "HUBSPOT_AUTHORIZATION_URL",
            "HUBSPOT_AUTHORIZE_URL",
        ),
    )
    token_url: str | None = Field(
        default=HUBSPOT_TOKEN_URL,
        validation_alias=AliasChoices("HUBSPOT_TOKEN_URL", "HUBSPOT_ACCESS_TOKEN_URL"),
    )
    client_id: str | None = Field(default=None, validation_alias="HUBSPOT_CLIENT_ID")
    client_secret: str | None = Field(
        default=None,
        validation_alias="HUBSPOT_CLIENT_SECRET",
    )
    redirect_uri: str | None = Field(
        default=None, validation_alias="HUBSPOT_REDIRECT_URI"
    )
    token: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "HUBSPOT_ACCESS_TOKEN",
            "HUBSPOT_TOKEN",
            "HUBSPOT_PRIVATE_APP_TOKEN",
        ),
    )
    default_scope: Sequence[str] | str | None = Field(default=None)

    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class HubspotUserCredentials(OAuth2Token):
    """User credential payload for HubSpot OAuth."""

    expires_in: int | None = None


__all__ = ["HubspotAppCredentials", "HubspotUserCredentials"]
