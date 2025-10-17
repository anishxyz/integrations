from __future__ import annotations

import pytest

from integrations.auth import AuthManager
from integrations.auth_providers.github import GithubUserCredentials
from integrations.auth.storage import InMemoryCredentialStore
from integrations.auth.auth_provider_key import AuthProviderKey


@pytest.mark.asyncio
async def test_session_uses_stored_github_credentials() -> None:
    store = InMemoryCredentialStore()
    manager = AuthManager(credential_store=store, github={"token": "fallback"})

    await manager.store_credentials(
        "github",
        "user-1",
        GithubUserCredentials(access_token="stored-token", token_type="Bearer"),
    )

    async with manager.session(subject="user-1") as integrations:
        github = integrations.github
        assert github.settings.token == "stored-token"
        assert github.settings.authorization_scheme == "Bearer"


@pytest.mark.asyncio
async def test_session_falls_back_to_app_token() -> None:
    manager = AuthManager(github={"token": "app-token"})

    async with manager.session(subject="user-2") as integrations:
        assert integrations.github.settings.token == "app-token"


@pytest.mark.asyncio
async def test_session_respects_provider_filter() -> None:
    manager = AuthManager(github={"token": "app-token"})

    async with manager.session(
        subject="user-3", providers=[AuthProviderKey.GITHUB]
    ) as integrations:
        assert integrations.github.settings.token == "app-token"


@pytest.mark.asyncio
async def test_session_accepts_manual_credentials() -> None:
    manager = AuthManager(github={"token": "app-token"})

    async with manager.session(
        subject="user-4",
        with_credentials={
            AuthProviderKey.GITHUB: GithubUserCredentials(
                access_token="manual", token_type="token-type"
            )
        },
        auto_load_credentials=False,
    ) as integrations:
        assert integrations.github.settings.token == "manual"
        assert integrations.github.settings.authorization_scheme == "token-type"
