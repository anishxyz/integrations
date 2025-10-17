"""Google auth provider registration."""

from ...auth.auth_provider_key import AuthProviderKey
from ...auth.auth_registry import register_auth_provider
from .google_auth_provider import (
    GoogleAppCredentials,
    GoogleAuthProvider,
    GoogleUserCredentials,
)

register_auth_provider(AuthProviderKey.GOOGLE, GoogleAuthProvider)

__all__ = ["GoogleAuthProvider", "GoogleAppCredentials", "GoogleUserCredentials"]
