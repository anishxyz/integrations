"""GitHub auth provider registration."""

from ...auth.auth_provider_key import AuthProviderKey
from ...auth.auth_registry import register_auth_provider
from .github_auth_provider import (
    GithubAppCredentials,
    GithubAuthProvider,
    GithubUserCredentials,
)

register_auth_provider(AuthProviderKey.GITHUB, GithubAuthProvider)

__all__ = ["GithubAuthProvider", "GithubAppCredentials", "GithubUserCredentials"]
