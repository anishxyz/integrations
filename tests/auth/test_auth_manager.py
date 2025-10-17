from __future__ import annotations

import pytest

from integrations.auth import AuthManager
from integrations.auth_providers.github import (
    GithubAppCredentials,
    GithubAuthProvider,
)

from .fixtures import DummyOAuthClient


def test_manager_auto_configures_github_with_credentials() -> None:
    manager = AuthManager(
        github={
            "client_id": "client",
            "client_secret": "secret",
            "redirect_uri": "https://example.com/callback",
        }
    )

    github = manager.get_provider("github")
    assert isinstance(github, GithubAuthProvider)
    assert github.app_credentials.client_id == "client"

    assert isinstance(manager.github, GithubAuthProvider)
    assert "github" in manager
    assert "github" in list(manager)


def test_manager_register_override() -> None:
    credentials = GithubAppCredentials(
        client_id="override",
        client_secret="secret",
        redirect_uri="https://example.com/callback",
        authorization_url="https://example.com/authorize",
        token_url="https://example.com/token",
    )
    custom = GithubAuthProvider(app_credentials=credentials)

    manager = AuthManager(auto_configure=False)
    manager.register("github", custom)

    provider = manager.providers()["github"]
    assert provider is custom
    assert manager.github is custom


def test_manager_skips_missing_credentials() -> None:
    manager = AuthManager(auto_configure=True)
    provider = manager.get_provider("github")
    assert isinstance(provider, GithubAuthProvider)


@pytest.mark.asyncio
async def test_e2e_oauth2_flow(monkeypatch: pytest.MonkeyPatch) -> None:
    created_clients: list[DummyOAuthClient] = []

    def factory(**kwargs: object) -> DummyOAuthClient:
        client = DummyOAuthClient(**kwargs)
        created_clients.append(client)
        return client

    monkeypatch.setattr("integrations.auth.flows.oauth2.AsyncOAuth2Client", factory)

    manager = AuthManager(
        github={
            "client_id": "client",
            "client_secret": "secret",
            "redirect_uri": "https://example.com/callback",
        }
    )

    flow = manager.github.oauth2

    authorization = await flow.authorize(state="state")
    assert authorization["state"] == "state"

    token = await flow.exchange(subject="user", code="code")
    assert token.access_token == "token"

    refreshed = await flow.refresh(credentials=token)
    assert refreshed.access_token == "new-token"

    assert len(created_clients) == 3
