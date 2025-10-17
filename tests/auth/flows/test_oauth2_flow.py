from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pytest

from integrations.auth import OAuth2AppCredentials, OAuth2Flow, OAuth2Token
from ..fixtures import DummyOAuthClient


@pytest.mark.asyncio
async def test_oauth2_flow_lifecycle(monkeypatch: pytest.MonkeyPatch) -> None:
    created_clients: list[DummyOAuthClient] = []

    def factory(**kwargs: Any) -> DummyOAuthClient:
        client = DummyOAuthClient(**kwargs)
        created_clients.append(client)
        return client

    monkeypatch.setattr(
        "integrations.auth.flows.oauth2.AsyncOAuth2Client",
        factory,
    )

    app_credentials = OAuth2AppCredentials(
        authorization_url="https://example.com/authorize",
        token_url="https://example.com/token",
        client_id="client-id",
        client_secret="client-secret",
        redirect_uri="https://example.com/callback",
        include_client_id=True,
    )

    flow = OAuth2Flow(
        app_credentials,
        default_scope=("repo", "user"),
        client_kwargs={"timeout": 10},
    )

    authorization = await flow.authorize(
        state="state-123", client_kwargs={"follow_redirects": True}
    )
    assert authorization["authorization_url"].startswith(
        "https://example.com/authorize"
    )
    assert authorization["state"] == "state-123"

    authorize_client = created_clients[0]
    assert authorize_client.kwargs["scope"] == "repo user"
    assert authorize_client.kwargs["client_id"] == "client-id"
    assert authorize_client.kwargs["client_secret"] == "client-secret"
    assert authorize_client.kwargs["timeout"] == 10
    assert authorize_client.kwargs["follow_redirects"] is True

    token = await flow.exchange(
        subject="subject-1",
        code="code-123",
        scope=("read",),
        client_kwargs={"timeout": 5},
    )
    assert isinstance(token, OAuth2Token)
    assert token.access_token == "token"
    assert token.scope == ("repo", "user")
    assert token.refresh_token == "refresh"

    exchange_client = created_clients[1]
    assert exchange_client.kwargs["scope"] == "read"
    assert exchange_client.fetch_calls[0]["code"] == "code-123"
    assert exchange_client.fetch_calls[0]["include_client_id"] is True

    refreshed = await flow.refresh(credentials=token)
    assert refreshed.access_token == "new-token"
    assert refreshed.scope == ("repo", "user")

    refresh_client = created_clients[2]
    assert refresh_client.kwargs["token"]["access_token"] == "token"
    assert refresh_client.refresh_calls[0]["refresh_token"] == "refresh"


@pytest.mark.parametrize(
    "scope_input, expected",
    [
        ("repo read", ("repo", "read")),
        (("repo", "read"), ("repo", "read")),
        (None, None),
    ],
)
def test_oauth2_token_roundtrip(
    scope_input: Sequence[str] | str | None, expected: tuple[str, ...] | None
) -> None:
    data: dict[str, Any] = {
        "access_token": "token",
        "token_type": "bearer",
        "scope": scope_input,
    }
    token = OAuth2Token.from_dict(data, scope_separator=" ")
    assert token.scope == expected
    assert token.raw["access_token"] == "token"

    serialized = token.to_dict(scope_separator=" ")
    if expected is None:
        assert "scope" not in serialized or serialized["scope"] in (None, "")
    else:
        assert serialized["scope"] == " ".join(expected)
