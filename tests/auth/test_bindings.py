from __future__ import annotations

import pytest

from integrations.auth import AuthManager
from integrations.auth.auth_provider import AuthProvider
from integrations.auth.bindings import AuthBinding
from integrations.auth.credentials import AppCredentials, UserCredentials
from integrations.core import ProviderSettings
from integrations.auth.auth_provider_key import AuthProviderKey


class DummySettings(ProviderSettings):
    token: str


class DummyAppCredentials(AppCredentials):
    token: str | None = None


class DummyUserCredentials(UserCredentials):
    token: str


class DummyBinding(AuthBinding):
    async def to_settings(
        self,
        *,
        manager: AuthManager,
        provider: str,
        subject: str,
        app_credentials: DummyAppCredentials,
        user_credentials: DummyUserCredentials | None,
    ) -> DummySettings:
        if user_credentials is not None:
            return DummySettings(token=user_credentials.token)
        if app_credentials.token:
            return DummySettings(token=app_credentials.token)
        return DummySettings(token="default")


class DummyAuthProvider(AuthProvider[DummyAppCredentials, DummyUserCredentials]):
    app_credentials_class = DummyAppCredentials
    user_credentials_class = DummyUserCredentials

    def default_bindings(self):  # type: ignore[override]
        return {AuthProviderKey.GITHUB: DummyBinding()}


@pytest.mark.asyncio
async def test_auth_provider_binding_mapping() -> None:
    provider = DummyAuthProvider(app_credentials=DummyAppCredentials(token="app"))
    binding = provider.bindings()[AuthProviderKey.GITHUB]

    manager = AuthManager(auto_configure=False)
    user = DummyUserCredentials(token="user")
    settings = await binding.to_settings(
        manager=manager,
        provider=AuthProviderKey.GITHUB.value,
        subject="subject",
        app_credentials=provider.app_credentials,
        user_credentials=user,
    )

    assert isinstance(settings, DummySettings)
    assert settings.token == "user"


@pytest.mark.asyncio
async def test_auth_provider_binding_fallback_to_app_credentials() -> None:
    provider = DummyAuthProvider(app_credentials=DummyAppCredentials(token="app"))
    binding = provider.bindings()[AuthProviderKey.GITHUB]
    manager = AuthManager(auto_configure=False)

    settings = await binding.to_settings(
        manager=manager,
        provider=AuthProviderKey.GITHUB.value,
        subject="subject",
        app_credentials=provider.app_credentials,
        user_credentials=None,
    )

    assert settings.token == "app"
