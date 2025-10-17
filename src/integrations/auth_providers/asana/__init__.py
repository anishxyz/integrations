"""Asana auth provider registration."""

from ...auth.auth_provider_key import AuthProviderKey
from ...auth.auth_registry import register_auth_provider
from .asana_auth_provider import (
    AsanaAppCredentials,
    AsanaAuthProvider,
    AsanaUserCredentials,
)

register_auth_provider(AuthProviderKey.ASANA, AsanaAuthProvider)

__all__ = ["AsanaAuthProvider", "AsanaAppCredentials", "AsanaUserCredentials"]
