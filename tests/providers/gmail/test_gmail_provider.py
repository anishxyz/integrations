"""Tests for the Gmail provider using mocked HTTP clients."""

from __future__ import annotations

from typing import Any

import pytest

from integrations.providers.gmail.gmail_provider import GmailProvider
from integrations.providers.gmail.gmail_settings import GmailSettings


class StubResponse:
    def __init__(self, payload, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code
        self.headers = {"Content-Type": "application/json"}

    def json(self):
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class RecordingRequest:
    def __init__(self, responses):
        self._responses = responses
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def __call__(self, method: str, slug: str, **kwargs):
        method_key = method.upper() if isinstance(method, str) else method
        record_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.calls.append((method_key, slug, record_kwargs))
        return self._responses[(method_key, slug)]


@pytest.fixture
def settings() -> GmailSettings:
    return GmailSettings(token="token-123", timeout=5, user_id="me")


def test_settings_allow_missing_token() -> None:
    settings = GmailSettings()
    assert settings.token is None
    assert settings.user_id == "me"


def test_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GMAIL_TOKEN", "env-token")
    monkeypatch.setenv("GMAIL_USER_ID", "user@example.com")

    settings = GmailSettings()

    assert settings.token == "env-token"
    assert settings.user_id == "user@example.com"


def test_httpx_headers(settings: GmailSettings) -> None:
    provider = GmailProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "Bearer token-123"
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_send_email(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {
        ("POST", "/users/me/messages/send"): StubResponse({"id": "123"}),
    }
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.send_email(raw="raw-message")

    assert result == {"id": "123"}
    method, path, kwargs = recorder.calls[0]
    assert method == "POST"
    assert path == "/users/me/messages/send"
    assert "params" not in kwargs
    assert kwargs["json"] == {"raw": "raw-message"}


@pytest.mark.asyncio
async def test_send_email_using_alias(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {
        ("POST", "/users/me/messages/send"): StubResponse({"id": "456"}),
    }
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.send_email_using_alias(raw="raw", alias="alias@example.com")

    assert result == {"id": "456"}
    _, _, kwargs = recorder.calls[0]
    assert kwargs["params"] == {"sendAsEmail": "alias@example.com"}
    assert kwargs["json"] == {"raw": "raw"}


@pytest.mark.asyncio
async def test_create_draft(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {
        ("POST", "/users/me/drafts"): StubResponse({"id": "draft"}),
    }
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.create_draft(raw="draft-raw", thread_id="thread-1")

    assert result == {"id": "draft"}
    _, _, kwargs = recorder.calls[0]
    assert "params" not in kwargs
    assert kwargs["json"] == {
        "message": {"raw": "draft-raw", "threadId": "thread-1"},
    }


@pytest.mark.asyncio
async def test_label_actions(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {
        ("POST", "/users/me/messages/msg-1/modify"): StubResponse({"id": "msg-1"}),
    }
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    await provider.add_label_to_email(message_id="msg-1", label_ids=["LBL"])
    await provider.remove_label_from_email(message_id="msg-1", label_ids=["LBL"])

    add_call, remove_call = recorder.calls
    assert add_call[2]["json"] == {"addLabelIds": ["LBL"]}
    assert remove_call[2]["json"] == {"removeLabelIds": ["LBL"]}


@pytest.mark.asyncio
async def test_move_and_star_actions(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {
        ("POST", "/users/me/messages/msg-2/modify"): StubResponse({"id": "msg-2"}),
    }
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    await provider.move_email(
        message_id="msg-2",
        add_label_ids=["LBL_DEST"],
        remove_label_ids=["LBL_SRC"],
    )
    await provider.star_email(message_id="msg-2")
    await provider.unstar_email(message_id="msg-2")
    await provider.archive_email(message_id="msg-2")

    move_call, star_call, unstar_call, archive_call = recorder.calls
    assert move_call[2]["json"] == {
        "addLabelIds": ["LBL_DEST"],
        "removeLabelIds": ["LBL_SRC"],
    }
    assert star_call[2]["json"] == {"addLabelIds": ["STARRED"]}
    assert unstar_call[2]["json"] == {"removeLabelIds": ["STARRED"]}
    assert archive_call[2]["json"] == {"removeLabelIds": ["INBOX"]}


@pytest.mark.asyncio
async def test_trash_and_untrash(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {
        ("POST", "/users/me/messages/msg-3/trash"): StubResponse({"id": "msg-3"}),
        ("POST", "/users/me/messages/msg-3/untrash"): StubResponse({"id": "msg-3"}),
    }
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    trashed = await provider.trash_email(message_id="msg-3")
    restored = await provider.untrash_email(message_id="msg-3")

    assert trashed == {"id": "msg-3"}
    assert restored == {"id": "msg-3"}
    trash_call, untrash_call = recorder.calls
    assert trash_call[1] == "/users/me/messages/msg-3/trash"
    assert untrash_call[1] == "/users/me/messages/msg-3/untrash"


@pytest.mark.asyncio
async def test_raw_request_action(
    monkeypatch: pytest.MonkeyPatch, settings: GmailSettings
) -> None:
    provider = GmailProvider(settings=settings)
    responses = {("GET", "/custom"): StubResponse({"ok": True})}
    recorder = RecordingRequest(responses)
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.raw_request("get", "/custom")

    assert result == {"ok": True}
    method, slug, kwargs = recorder.calls[0]
    assert method == "GET"
    assert slug == "/custom"
    assert "json" not in kwargs
