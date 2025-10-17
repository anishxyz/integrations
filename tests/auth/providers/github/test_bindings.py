from __future__ import annotations

import pytest

from integrations.auth import AuthManager
from integrations.auth_providers.github import (
    GithubAppCredentials,
    GithubAuthProvider,
    GithubUserCredentials,
)
from integrations.auth.auth_provider_key import AuthProviderKey
from integrations.providers.github.github_settings import GithubSettings


@pytest.mark.asyncio
async def test_github_binding_prefers_user_credentials() -> None:
    provider = GithubAuthProvider(
        app_credentials=GithubAppCredentials(client_id="client", token="fallback")
    )
    binding = provider.bindings()[AuthProviderKey.GITHUB]

    manager = AuthManager(auto_configure=False)
    user_creds = GithubUserCredentials(
        access_token="user-token", token_type="token-type"
    )

    settings = await binding.to_settings(
        manager=manager,
        provider=AuthProviderKey.GITHUB,
        subject="user-123",
        app_credentials=provider.app_credentials,
        user_credentials=user_creds,
    )

    assert isinstance(settings, GithubSettings)
    assert settings.token == "user-token"
    assert settings.authorization_scheme == "token-type"


@pytest.mark.asyncio
async def test_github_binding_falls_back_to_app_token() -> None:
    provider = GithubAuthProvider(
        app_credentials=GithubAppCredentials(token="app-token")
    )
    binding = provider.bindings()[AuthProviderKey.GITHUB]
    manager = AuthManager(auto_configure=False)

    settings = await binding.to_settings(
        manager=manager,
        provider=AuthProviderKey.GITHUB,
        subject="user-123",
        app_credentials=provider.app_credentials,
        user_credentials=None,
    )

    assert isinstance(settings, GithubSettings)
    assert settings.token == "app-token"
    assert settings.authorization_scheme == "Bearer"
