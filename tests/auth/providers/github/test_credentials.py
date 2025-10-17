from __future__ import annotations

import pytest

from integrations.auth import AuthManager
from integrations.auth_providers.github.github_credentials import GithubAppCredentials


def test_github_app_credentials_env_aliases(monkeypatch: pytest.MonkeyPatch) -> None:
    auth_url = "https://example.com/authorize"
    token_url = "https://example.com/token"
    client_id = "env-client-id"
    client_secret = "env-client-secret"
    monkeypatch.setenv("GITHUB_AUTHORIZATION_URL", auth_url)
    monkeypatch.setenv("GITHUB_TOKEN_URL", token_url)
    monkeypatch.setenv("GITHUB_CLIENT_ID", client_id)
    monkeypatch.setenv("GITHUB_CLIENT_SECRET", client_secret)

    credentials = GithubAppCredentials()

    assert credentials.authorization_url == auth_url
    assert credentials.token_url == token_url
    assert credentials.client_id == client_id
    assert credentials.client_secret == client_secret

    manager = AuthManager()
    provider = manager.get_provider("github")

    assert provider.app_credentials.authorization_url == auth_url
    assert provider.app_credentials.token_url == token_url
    assert provider.app_credentials.client_id == client_id
    assert provider.app_credentials.client_secret == client_secret
