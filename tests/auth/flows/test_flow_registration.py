from __future__ import annotations

import asyncio
from typing import Any

import pytest

from integrations.auth import (
    AppCredentials,
    AuthProvider,
    BaseAuthFlow,
    UserCredentials,
    flow,
)


class DummyAppCredentials(AppCredentials):
    client_id: str = "dummy"


class DummyUserCredentials(UserCredentials):
    token: str


class DummyFlow(BaseAuthFlow):
    kind = "dummy"

    def __init__(self) -> None:
        self.authorize_calls: list[dict[str, Any]] = []
        self.exchange_calls: list[dict[str, Any]] = []
        self.refresh_calls: list[dict[str, Any]] = []

    async def authorize(self, **kwargs: Any) -> dict[str, Any]:
        self.authorize_calls.append(kwargs)
        return {"ok": True, **kwargs}

    async def exchange(self, *, subject: Any, **kwargs: Any) -> DummyUserCredentials:
        payload = {"subject": subject, **kwargs}
        self.exchange_calls.append(payload)
        return DummyUserCredentials(token="issued", **payload)

    async def refresh(
        self,
        *,
        subject: Any | None = None,
        credentials: DummyUserCredentials | None = None,
        **kwargs: Any,
    ) -> DummyUserCredentials:
        payload = {"subject": subject, "credentials": credentials, **kwargs}
        self.refresh_calls.append(payload)
        return DummyUserCredentials(token="refreshed", **payload)


class DummyAuthProvider(AuthProvider[DummyAppCredentials, DummyUserCredentials]):
    app_credentials_class = DummyAppCredentials

    dummy_flow: DummyFlow = flow(lambda provider: DummyFlow())


@pytest.mark.asyncio
async def test_flow_descriptor_instantiates_once_per_provider() -> None:
    provider = DummyAuthProvider()
    other = DummyAuthProvider()

    first_flow = provider.dummy_flow
    second_flow = provider.dummy_flow
    other_flow = other.dummy_flow

    assert first_flow is second_flow
    assert first_flow is not other_flow

    flows = provider.flows()
    assert "dummy_flow" in flows
    assert flows["dummy_flow"] is first_flow

    # sanity check async methods behave
    await asyncio.gather(
        provider.dummy_flow.authorize(state="123"),
        provider.dummy_flow.exchange(subject="user", code="abc"),
        provider.dummy_flow.refresh(subject="user"),
    )

    assert provider.dummy_flow.authorize_calls[-1] == {"state": "123"}
    assert provider.dummy_flow.exchange_calls[-1]["subject"] == "user"
    assert provider.dummy_flow.refresh_calls[-1]["subject"] == "user"


def test_app_credentials_coercion() -> None:
    provider = DummyAuthProvider(app_credentials={"client_id": "coerced"})
    assert isinstance(provider.app_credentials, DummyAppCredentials)
    assert provider.app_credentials.client_id == "coerced"
