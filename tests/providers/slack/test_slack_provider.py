"""Tests for the Slack provider."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

import httpx
import pytest

from integrations import Integrations
from integrations.providers.slack.slack_provider import SlackProvider
from integrations.providers.slack.slack_settings import SlackSettings


class StubResponse:
    def __init__(
        self,
        payload: Any,
        status_code: int = 200,
        *,
        headers: Mapping[str, str] | None = None,
        text: str | None = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers = dict(headers or {"content-type": "application/json"})
        self._text = text

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
        if self._text is not None:
            return self._text
        if isinstance(self._payload, str):
            return self._payload
        if isinstance(self._payload, (bytes, bytearray)):
            return bytes(self._payload).decode()
        return ""

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class StubAsyncClient:
    def __init__(
        self, responses: Dict[Tuple[str, str], list[StubResponse] | StubResponse]
    ) -> None:
        self._responses: Dict[Tuple[str, str], list[StubResponse]] = {}
        for key, value in responses.items():
            method, path = key
            normalized = (method.upper(), path)
            if isinstance(value, list):
                self._responses[normalized] = list(value)
            else:
                self._responses[normalized] = [value]
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
        except KeyError as exc:
            raise AssertionError(f"Unexpected request: {method} {path}") from exc
        if not responses:
            raise AssertionError(f"No responses left for {method} {path}")
        return responses.pop(0)

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        headers: Dict[str, Any] | None = None,
        **_: Any,
    ) -> StubResponse:
        method_upper = method.upper()
        self.calls.append((method_upper, url, params, json, data, headers))
        return self._next_response(method_upper, url)


@pytest.fixture
def settings() -> SlackSettings:
    return SlackSettings(token="xoxb-token", user_agent="sdk", timeout=5)


def test_settings_env_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SLACK_BOT_TOKEN", "env-token")
    monkeypatch.setenv("SLACK_USER_AGENT", "env-agent")

    settings = SlackSettings()

    assert settings.token == "env-token"
    assert settings.user_agent == "env-agent"


def test_httpx_headers(settings: SlackSettings) -> None:
    provider = SlackProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "Bearer xoxb-token"
    assert headers["User-Agent"] == "sdk"
    assert headers["Content-Type"].startswith("application/json")


@pytest.mark.asyncio
async def test_raw_request_delegates_to_provider(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response = StubResponse({"ok": True, "value": 1})

    async def fake_request(method: str, slug: str, **kwargs: Any) -> StubResponse:
        captured.update({"method": method, "slug": slug, "kwargs": kwargs})
        return stub_response

    monkeypatch.setattr(provider, "request", fake_request)

    result = await provider.raw_request("POST", "/chat.postMessage", json={"a": 1})

    assert result == {"ok": True, "value": 1}
    assert captured["method"] == "POST"
    assert captured["slug"] == "/chat.postMessage"
    assert captured["kwargs"]["json"] == {"a": 1}


def test_process_httpx_response_raises_on_error(settings: SlackSettings) -> None:
    provider = SlackProvider(settings=settings)
    request = httpx.Request("GET", "https://slack.com/api/test")
    response = httpx.Response(
        200,
        json={"ok": False, "error": "invalid_auth"},
        request=request,
    )

    with pytest.raises(ValueError, match="invalid_auth"):
        provider.process_httpx_response(response)


@pytest.mark.asyncio
async def test_send_channel_message(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    payload = {"ok": True, "ts": "123.456"}
    stub_client = StubAsyncClient(
        responses={
            ("POST", "/chat.postMessage"): [StubResponse(payload)],
        }
    )

    def fake_client(**_):
        return stub_client

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    response = await provider.send_channel_message(channel_id="C123", text="hello")

    assert response == payload
    method, url, params, json_body, data, headers = stub_client.calls[0]
    assert method == "POST"
    assert url == "/chat.postMessage"
    assert params is None
    assert json_body == {"channel": "C123", "text": "hello"}
    assert data is None
    assert headers is None
    assert stub_client.closed is True


@pytest.mark.asyncio
async def test_send_direct_message(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    responses = {
        ("POST", "/conversations.open"): [
            StubResponse({"ok": True, "channel": {"id": "D123"}})
        ],
        ("POST", "/chat.postMessage"): [
            StubResponse({"ok": True, "message": {"text": "hi"}})
        ],
    }
    stub_client = StubAsyncClient(responses=responses)

    def fake_client(**_):
        return stub_client

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.send_direct_message(user_id="U123", text="hi")

    assert result == {"ok": True, "message": {"text": "hi"}}
    open_call = stub_client.calls[0]
    message_call = stub_client.calls[1]
    assert open_call[0] == "POST"
    assert open_call[1] == "/conversations.open"
    assert open_call[3] == {"users": "U123"}
    assert message_call[0] == "POST"
    assert message_call[1] == "/chat.postMessage"
    assert message_call[3]["channel"] == "D123"


@pytest.mark.asyncio
async def test_get_message_by_timestamp(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    responses = {
        ("GET", "/conversations.history"): [
            StubResponse({"ok": True, "messages": [{"ts": "111.222", "text": "hello"}]})
        ],
    }
    stub_client = StubAsyncClient(responses=responses)

    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    message = await provider.get_message_by_timestamp(
        channel_id="C1", message_ts="111.222"
    )

    assert message == {"ts": "111.222", "text": "hello"}
    method, path, params, json_body, data, headers = stub_client.calls[0]
    assert method == "GET"
    assert path == "/conversations.history"
    assert params["inclusive"] is True
    assert json_body is None
    assert data is None
    assert headers is None


@pytest.mark.asyncio
async def test_retrieve_thread_messages(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    responses = {
        ("GET", "/conversations.replies"): [
            StubResponse({"ok": True, "messages": [{"ts": "1"}, {"ts": "2"}]})
        ],
    }
    stub_client = StubAsyncClient(responses=responses)

    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    messages = await provider.retrieve_thread_messages(
        channel_id="C1", thread_ts="1", limit=50
    )

    assert [msg["ts"] for msg in messages] == ["1", "2"]
    method, path, params, json_body, data, headers = stub_client.calls[0]
    assert method == "GET"
    assert path == "/conversations.replies"
    assert params["limit"] == 50
    assert json_body is None
    assert data is None
    assert headers is None


@pytest.mark.asyncio
async def test_set_profile_status(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    responses = {
        ("POST", "/users.profile.set"): [
            StubResponse({"ok": True, "profile": {"status_text": "Busy"}})
        ],
    }
    stub_client = StubAsyncClient(responses=responses)

    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    profile = await provider.set_profile_status(
        status_text="Busy", status_emoji=":hammer:", status_expiration=0
    )

    assert profile["profile"]["status_text"] == "Busy"
    method, path, params, json_body, data, headers = stub_client.calls[0]
    assert method == "POST"
    assert path == "/users.profile.set"
    assert params is None
    assert json_body["profile"]["status_emoji"] == ":hammer:"
    assert data is None
    assert headers is None


@pytest.mark.asyncio
async def test_find_conversation_members(
    monkeypatch: pytest.MonkeyPatch, settings: SlackSettings
) -> None:
    provider = SlackProvider(settings=settings)
    responses = {
        ("GET", "/conversations.members"): [
            StubResponse({"ok": True, "members": ["U1", "U2"]})
        ],
    }
    stub_client = StubAsyncClient(responses=responses)

    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub_client)

    result = await provider.find_conversation_members(channel_id="C1", limit=2)

    assert result["members"] == ["U1", "U2"]
    method, path, params, json_body, data, headers = stub_client.calls[0]
    assert method == "GET"
    assert path == "/conversations.members"
    assert params["limit"] == 2
    assert json_body is None
    assert data is None
    assert headers is None


@pytest.mark.asyncio
async def test_integrations_end_to_end(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SlackSettings(token="xoxb-override", user_agent="sdk")
    container = Integrations(slack=settings)

    responses = {
        ("POST", "/chat.postMessage"): [StubResponse({"ok": True, "ts": "1.0"})],
    }
    stub_client = StubAsyncClient(responses=responses)

    monkeypatch.setattr(container.slack, "httpx_client", lambda **_: stub_client)

    payload = await container.slack.send_channel_message(channel_id="C1", text="Hello")

    assert payload["ts"] == "1.0"
    assert stub_client.closed is True
