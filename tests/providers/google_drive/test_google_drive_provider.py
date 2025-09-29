"""Tests for the Google Drive provider."""

from __future__ import annotations

import json
from typing import Any, Mapping

import pytest

from integrations.providers.google_drive.google_drive_provider import (
    GoogleDriveProvider,
)
from integrations.providers.google_drive.google_drive_settings import (
    GoogleDriveSettings,
)


class StubResponse:
    def __init__(
        self,
        payload: Any | None,
        *,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = dict(headers or {"Content-Type": "application/json"})
        if payload is None:
            self.content = b""
        elif isinstance(payload, (bytes, bytearray)):
            self.content = bytes(payload)
        else:
            self.content = json.dumps(payload).encode("utf-8")
        self.text = self.content.decode("utf-8", errors="ignore")

    def json(self) -> Any:
        if isinstance(self._payload, (bytes, bytearray)):
            raise ValueError("No JSON payload")
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class RecordingRequest:
    def __init__(
        self, responses: Mapping[tuple[str, str], list[StubResponse] | StubResponse]
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
        try:
            queue = self._responses[(method_key, slug)]
        except KeyError as exc:  # pragma: no cover - defensive guard
            raise AssertionError(f"Unexpected request: {method_key} {slug}") from exc
        if not queue:  # pragma: no cover - defensive guard
            raise AssertionError(f"No responses left for {method_key} {slug}")
        return queue.pop(0)


@pytest.fixture
def settings() -> GoogleDriveSettings:
    return GoogleDriveSettings(token="ya29.drive-token", user_agent="sdk-test")


def test_httpx_headers(settings: GoogleDriveSettings) -> None:
    provider = GoogleDriveProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"].startswith("Bearer ya29.drive-token")
    assert headers["Accept"] == "application/json"
    assert headers["User-Agent"] == "sdk-test"


@pytest.mark.asyncio
async def test_create_file_from_text_uses_multipart_upload(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest({("POST", "/files"): StubResponse({"id": "file123"})})
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.create_file_from_text(
        "Notes",
        "hello",
        parents=["folder1"],
    )

    assert result["id"] == "file123"
    method, slug, kwargs = recorder.calls[0]
    assert method == "POST" and slug == "/files"
    assert kwargs["params"]["uploadType"] == "multipart"
    metadata_part = kwargs["files"]["metadata"]
    assert json.loads(metadata_part[1])["parents"] == ["folder1"]
    assert kwargs["base_url"] == settings.upload_base_url


@pytest.mark.asyncio
async def test_find_or_create_folder_returns_existing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest(
        {("GET", "/files"): StubResponse({"files": [{"id": "abc", "name": "Reports"}]})}
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.find_or_create_folder("Reports")

    assert result["created"] is False
    assert result["folder"]["id"] == "abc"
    assert len(recorder.calls) == 1


@pytest.mark.asyncio
async def test_find_or_create_folder_creates_when_missing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest(
        {
            ("GET", "/files"): [StubResponse({"files": []})],
            ("POST", "/files"): StubResponse({"id": "new-folder"}),
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.find_or_create_folder("Reports", parents=["root"])

    assert result["created"] is True
    assert result["folder"]["id"] == "new-folder"
    _, post_call = recorder.calls
    assert post_call[2]["json"]["mimeType"] == "application/vnd.google-apps.folder"


@pytest.mark.asyncio
async def test_upload_document_sets_google_doc_mime(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest({("POST", "/files"): StubResponse({"id": "doc123"})})
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.upload_document("Report", content="Hello")

    assert result["id"] == "doc123"
    _, _, kwargs = recorder.calls[0]
    metadata = json.loads(kwargs["files"]["metadata"][1])
    assert metadata["mimeType"] == "application/vnd.google-apps.document"
    assert kwargs["base_url"] == settings.upload_base_url


@pytest.mark.asyncio
async def test_find_or_create_document_creates_when_missing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest(
        {
            ("GET", "/files"): [StubResponse({"files": []})],
            ("POST", "/files"): StubResponse({"id": "doc789"}),
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.find_or_create_document("Proposal")

    assert result["created"] is True
    assert result["document"]["id"] == "doc789"
    _, post_call = recorder.calls
    if "files" in post_call[2]:
        metadata = json.loads(post_call[2]["files"]["metadata"][1])
    else:
        metadata = post_call[2]["json"]
    assert metadata["mimeType"] == "application/vnd.google-apps.document"


@pytest.mark.asyncio
async def test_create_document_from_template_wraps_copy(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest(
        {("POST", "/files/template123/copy"): StubResponse({"id": "copy123"})}
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.create_document_from_template("template123", name="Copy")

    assert result["document"]["id"] == "copy123"
    method, slug, kwargs = recorder.calls[0]
    assert method == "POST"
    assert slug == "/files/template123/copy"
    assert kwargs["json"]["name"] == "Copy"


@pytest.mark.asyncio
async def test_replace_file_uses_media_upload(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest(
        {("PATCH", "/files/file123"): StubResponse({"id": "file123"})}
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.replace_file("file123", b"data", mime_type="text/plain")

    assert result["id"] == "file123"
    _, _, kwargs = recorder.calls[0]
    assert kwargs["params"]["uploadType"] == "media"
    assert kwargs["data"] == b"data"
    assert kwargs["headers"]["Content-Type"] == "text/plain"
    assert kwargs["base_url"] == settings.upload_base_url


@pytest.mark.asyncio
async def test_upload_file_uses_download_when_source_url(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleDriveSettings,
) -> None:
    provider = GoogleDriveProvider(settings=settings)
    recorder = RecordingRequest({("POST", "/files"): StubResponse({"id": "file789"})})
    monkeypatch.setattr(provider, "request", recorder)

    async def fake_download(url: str) -> tuple[bytes, str | None]:
        assert url == "https://example.com/report.pdf"
        return b"pdf-bytes", "application/pdf"

    monkeypatch.setattr(provider, "download_external", fake_download)

    result = await provider.upload_file(
        "Report.pdf",
        source_url="https://example.com/report.pdf",
        supports_all_drives=False,
    )

    assert result["id"] == "file789"
    _, _, kwargs = recorder.calls[0]
    assert kwargs["params"]["supportsAllDrives"] is False
    metadata = json.loads(kwargs["files"]["metadata"][1])
    assert metadata["mimeType"] == "application/pdf"
    assert kwargs["base_url"] == settings.upload_base_url
