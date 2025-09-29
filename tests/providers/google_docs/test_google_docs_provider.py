"""Tests for the Google Docs provider."""

from __future__ import annotations

import json
from typing import Any, Mapping

import pytest

from integrations.providers.google_docs.google_docs_provider import (
    GoogleDocsProvider,
)
from integrations.providers.google_docs.google_docs_settings import (
    GoogleDocsSettings,
)


class StubResponse:
    def __init__(
        self,
        payload: Any,
        *,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = dict(headers or {"Content-Type": "application/json"})
        self.content = (
            json.dumps(payload).encode("utf-8") if payload is not None else b""
        )
        self.text = self.content.decode("utf-8", errors="ignore")

    def json(self) -> Any:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class RecordingRequest:
    def __init__(
        self, responses: Mapping[tuple[str, str], StubResponse | list[StubResponse]]
    ):
        self._responses: dict[tuple[str, str], list[StubResponse]] = {}
        for key, value in responses.items():
            if isinstance(value, list):
                self._responses[key] = list(value)
            else:
                self._responses[key] = [value]
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def __call__(self, method: str, slug: str, **kwargs: Any) -> StubResponse:
        method_key = method.upper()
        recorded_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.calls.append((method_key, slug, recorded_kwargs))
        responses = self._responses[(method_key, slug)]
        if not responses:
            raise AssertionError(f"No responses left for {method_key} {slug}")
        return responses.pop(0)


@pytest.fixture
def settings() -> GoogleDocsSettings:
    return GoogleDocsSettings(token="ya29.docs-token", user_agent="sdk-docs")


def test_httpx_headers(settings: GoogleDocsSettings) -> None:
    provider = GoogleDocsProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"].startswith("Bearer ya29.docs-token")
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert headers["User-Agent"] == "sdk-docs"


@pytest.mark.asyncio
async def test_append_text_to_document_issues_batch_update(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDocsSettings,
) -> None:
    provider = GoogleDocsProvider(settings=settings)
    recorder = RecordingRequest(
        {("POST", "/documents/doc123:batchUpdate"): StubResponse({"replies": [{}]})}
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.append_text_to_document(
        "doc123",
        "Hello",
        append_newline=True,
    )

    assert "replies" in result
    method, slug, kwargs = recorder.calls[0]
    assert method == "POST"
    assert slug == "/documents/doc123:batchUpdate"
    requests = kwargs["json"]["requests"]
    assert requests[0]["insertText"]["text"] == "Hello\n"
    assert requests[0]["insertText"]["endOfSegmentLocation"] == {}


@pytest.mark.asyncio
async def test_create_document_from_text_creates_and_inserts(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDocsSettings,
) -> None:
    provider = GoogleDocsProvider(settings=settings)
    recorder = RecordingRequest(
        {
            ("POST", "/documents"): StubResponse(
                {"documentId": "doc456", "title": "Generated"}
            ),
            ("POST", "/documents/doc456:batchUpdate"): StubResponse(
                {"replies": [{"insertText": {"location": {"index": 1}}}]}
            ),
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.create_document_from_text(
        "Initial text",
        title="Generated",
        append_newline=False,
    )

    assert result["documentId"] == "doc456"
    assert result["document"]["title"] == "Generated"
    update = result.get("update")
    assert isinstance(update, dict)
    assert update["replies"][0]["insertText"]["location"]["index"] == 1

    create_call, update_call = recorder.calls
    assert create_call[0] == "POST"
    assert create_call[1] == "/documents"
    assert create_call[2]["json"] == {"title": "Generated"}
    assert update_call[1] == "/documents/doc456:batchUpdate"


@pytest.mark.asyncio
async def test_raw_request_action(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = GoogleDocsProvider(settings=GoogleDocsSettings(token="token"))
    recorder = RecordingRequest({("GET", "/custom/path"): StubResponse({"ok": True})})
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.raw_request(
        "GET",
        "/custom/path",
        base_url="https://docs.googleapis.com/custom",
    )

    assert result == {"ok": True}
    method, slug, kwargs = recorder.calls[0]
    assert method == "GET"
    assert slug == "/custom/path"
    assert kwargs["base_url"] == "https://docs.googleapis.com/custom"
