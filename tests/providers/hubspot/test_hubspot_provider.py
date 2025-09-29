"""Tests for the HubSpot provider."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Dict, Tuple

import pytest

from integrations import Container
from integrations.providers.hubspot.hubspot_provider import HubspotProvider
from integrations.providers.hubspot.hubspot_settings import HubspotSettings


class StubResponse:
    def __init__(
        self,
        payload: Any,
        *,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers = dict(headers or {"Content-Type": "application/json"})

    def json(self) -> Any:
        return self._payload

    @property
    def content(self) -> bytes:
        if self._payload is None:
            return b""
        if isinstance(self._payload, (bytes, bytearray)):
            return bytes(self._payload)
        if isinstance(self._payload, str):
            return self._payload.encode()
        return b"payload"

    @property
    def text(self) -> str:
        payload = self._payload
        if payload is None:
            return ""
        if isinstance(payload, (bytes, bytearray)):
            return bytes(payload).decode()
        return str(payload)

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class StubAsyncClient:
    def __init__(
        self,
        responses: Dict[Tuple[str, str], list[StubResponse] | StubResponse],
    ) -> None:
        self._responses: Dict[Tuple[str, str], list[StubResponse]] = {}
        for key, value in responses.items():
            if isinstance(value, list):
                self._responses[key] = list(value)
            else:
                self._responses[key] = [value]
        self.calls: list[
            tuple[
                str,
                str,
                Dict[str, Any] | None,
                Dict[str, Any] | None,
                Dict[str, Any] | None,
                Dict[str, Any] | None,
            ]
        ] = []
        self.closed = False

    async def __aenter__(self) -> "StubAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.closed = True

    def _next_response(self, method: str, path: str) -> StubResponse:
        key = (method.upper(), path)
        try:
            responses = self._responses[key]
        except KeyError as exc:  # pragma: no cover - defensive
            raise AssertionError(f"Unexpected request: {method} {path}") from exc
        if not responses:
            raise AssertionError(f"No responses left for {method} {path}")
        return responses.pop(0)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        files: Dict[str, Any] | None = None,
        headers: Dict[str, Any] | None = None,
    ) -> StubResponse:
        method = method.upper()
        self.calls.append((method, path, params, json, data, files))
        return self._next_response(method, path)


@pytest.fixture
def settings() -> HubspotSettings:
    return HubspotSettings(access_token="secret", user_agent="sdk", timeout=5)


def test_settings_env_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HUBSPOT_ACCESS_TOKEN", "env-token")
    monkeypatch.setenv("HUBSPOT_USER_AGENT", "env-agent")

    settings = HubspotSettings()

    assert settings.access_token == "env-token"
    assert settings.user_agent == "env-agent"


def test_httpx_headers(settings: HubspotSettings) -> None:
    provider = HubspotProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "Bearer secret"
    assert headers["User-Agent"] == "sdk"


@pytest.mark.asyncio
async def test_create_contact(
    monkeypatch: pytest.MonkeyPatch, settings: HubspotSettings
) -> None:
    provider = HubspotProvider(settings=settings)
    payload = {"id": "123"}
    stub_client = StubAsyncClient(
        responses={
            ("POST", "/crm/v3/objects/contacts"): StubResponse(payload),
        }
    )

    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    result = await provider.create_contact(properties={"email": "a@example.com"})

    assert result == payload
    method, path, params, json_body, data, files = stub_client.calls[0]
    assert method == "POST"
    assert path == "/crm/v3/objects/contacts"
    assert json_body == {"properties": {"email": "a@example.com"}}
    assert params is None
    assert data is None
    assert files is None
    assert stub_client.closed is True


@pytest.mark.asyncio
async def test_upload_file(
    monkeypatch: pytest.MonkeyPatch, settings: HubspotSettings
) -> None:
    provider = HubspotProvider(settings=settings)
    stub_client = StubAsyncClient(
        responses={
            ("POST", "/files/v3/files"): StubResponse({"id": "file"}),
        }
    )

    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    result = await provider.upload_file(
        file_name="example.txt",
        file_bytes=b"hello",
        content_type="text/plain",
        options={"folderPath": "uploads"},
    )

    assert result == {"id": "file"}
    _, path, params, json_body, data, files = stub_client.calls[0]
    assert path == "/files/v3/files"
    assert json_body is None
    assert data == {"options": '{"folderPath": "uploads"}'}
    assert files is not None
    assert files["file"][0] == "example.txt"


@pytest.mark.asyncio
async def test_find_or_create_contact_existing(
    monkeypatch: pytest.MonkeyPatch, settings: HubspotSettings
) -> None:
    provider = HubspotProvider(settings=settings)
    stub_client = StubAsyncClient(
        responses={
            ("POST", "/crm/v3/objects/contacts/search"): StubResponse(
                {"results": [{"id": "existing"}]}
            ),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    result = await provider.find_or_create_contact(
        create_properties={"email": "a@example.com"},
        search_filters=[
            {"propertyName": "email", "operator": "EQ", "value": "a@example.com"}
        ],
    )

    assert result == {"id": "existing"}
    assert len(stub_client.calls) == 1
    method, path, *_ = stub_client.calls[0]
    assert method == "POST"
    assert path.endswith("/search")


@pytest.mark.asyncio
async def test_find_or_create_contact_creates(
    monkeypatch: pytest.MonkeyPatch, settings: HubspotSettings
) -> None:
    provider = HubspotProvider(settings=settings)
    stub_client = StubAsyncClient(
        responses={
            ("POST", "/crm/v3/objects/contacts/search"): StubResponse({"results": []}),
            ("POST", "/crm/v3/objects/contacts"): StubResponse({"id": "new"}),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    result = await provider.find_or_create_contact(
        create_properties={"email": "new@example.com"},
        search_filters=[
            {"propertyName": "email", "operator": "EQ", "value": "new@example.com"}
        ],
    )

    assert result == {"id": "new"}
    assert len(stub_client.calls) == 2
    create_call = stub_client.calls[1]
    assert create_call[1] == "/crm/v3/objects/contacts"
    assert create_call[3] == {"properties": {"email": "new@example.com"}}


@pytest.mark.asyncio
async def test_raw_request_action(
    monkeypatch: pytest.MonkeyPatch, settings: HubspotSettings
) -> None:
    provider = HubspotProvider(settings=settings)
    stub_client = StubAsyncClient(
        responses={
            ("DELETE", "/custom/path"): StubResponse(
                None, headers={"Content-Type": "text/plain"}
            ),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    result = await provider.raw_request(
        "delete",
        "/custom/path",
        params={"a": 1},
        json={"b": 2},
    )

    assert result == {}
    method, path, params, json_body, data, files = stub_client.calls[0]
    assert method == "DELETE"
    assert path == "/custom/path"
    assert params == {"a": 1}
    assert json_body == {"b": 2}
    assert data is None
    assert files is None


@pytest.mark.asyncio
async def test_container_end_to_end(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = HubspotSettings(access_token="token")
    container = Container(hubspot=settings)

    stub_client = StubAsyncClient(
        responses={
            ("POST", "/crm/v3/objects/contacts"): StubResponse({"id": "42"}),
        }
    )
    monkeypatch.setattr(container.hubspot, "httpx_client", lambda **_: stub_client)

    result = await container.hubspot.create_contact(
        properties={"email": "user@example.com"}
    )

    assert result["id"] == "42"
    assert stub_client.closed is True
