from __future__ import annotations

import pytest

from integrations.auth import AuthManager
from integrations.auth.storage import InMemoryCredentialStore
from integrations.auth_providers.github import GithubUserCredentials


@pytest.mark.asyncio
async def test_in_memory_store_roundtrip() -> None:
    store = InMemoryCredentialStore()
    data = {"access_token": "abc", "token_type": "bearer"}

    await store.set("github", "user-1", data)
    fetched = await store.get("github", "user-1")
    assert fetched == data

    await store.delete("github", "user-1")
    assert await store.get("github", "user-1") is None


@pytest.mark.asyncio
async def test_in_memory_store_handles_mapping_subject() -> None:
    store = InMemoryCredentialStore()
    subject = {"user_id": "123", "org": "acme"}
    data = {"access_token": "token"}

    await store.set("github", subject, data)
    fetched = await store.get("github", subject)
    assert fetched == data

    await store.delete("github", subject)
    assert await store.get("github", subject) is None


@pytest.mark.asyncio
async def test_auth_manager_store_and_load_credentials() -> None:
    manager = AuthManager(
        github={
            "client_id": "client",
            "client_secret": "secret",
            "redirect_uri": "https://example.com/callback",
        }
    )

    credentials = GithubUserCredentials(access_token="token", token_type="bearer")

    await manager.store_credentials("github", "user-xyz", credentials)
    stored = await manager.load_credentials("github", "user-xyz")

    assert isinstance(stored, GithubUserCredentials)
    assert stored.access_token == "token"
    assert stored.token_type == "bearer"

    await manager.delete_credentials("github", "user-xyz")
    assert await manager.load_credentials("github", "user-xyz") is None
