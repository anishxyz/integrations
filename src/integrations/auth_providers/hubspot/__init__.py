"""HubSpot auth provider registration."""

from ...auth.auth_provider_key import AuthProviderKey
from ...auth.auth_registry import register_auth_provider
from .hubspot_auth_provider import (
    HubspotAppCredentials,
    HubspotAuthProvider,
    HubspotUserCredentials,
)

register_auth_provider(AuthProviderKey.HUBSPOT, HubspotAuthProvider)

__all__ = [
    "HubspotAuthProvider",
    "HubspotAppCredentials",
    "HubspotUserCredentials",
]
