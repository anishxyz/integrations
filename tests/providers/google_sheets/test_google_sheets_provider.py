"""Tests for the Google Sheets provider."""

from __future__ import annotations

import json
from typing import Any, Mapping

import pytest

from integrations.providers.google_sheets.google_sheets_provider import (
    GoogleSheetsProvider,
)
from integrations.providers.google_sheets.google_sheets_settings import (
    GoogleSheetsSettings,
)


class StubResponse:
    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers = {"Content-Type": "application/json"}
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
        try:
            queue = self._responses[(method_key, slug)]
        except KeyError as exc:  # pragma: no cover - defensive guard
            raise AssertionError(f"Unexpected request: {method_key} {slug}") from exc
        if not queue:
            raise AssertionError(f"No responses left for {method_key} {slug}")
        return queue.pop(0)


@pytest.fixture
def settings() -> GoogleSheetsSettings:
    return GoogleSheetsSettings(token="ya29.token", user_agent="sdk")


def test_httpx_headers(settings: GoogleSheetsSettings) -> None:
    provider = GoogleSheetsProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"].startswith("Bearer ya29.token")
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert headers["User-Agent"] == "sdk"


@pytest.mark.asyncio
async def test_create_spreadsheet_row_appends_values(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleSheetsSettings,
) -> None:
    provider = GoogleSheetsProvider(settings=settings)
    recorder = RecordingRequest(
        {
            (
                "POST",
                "/spreadsheet123/values/Sheet1!A1:B1:append",
            ): StubResponse({"updates": {"updatedRows": 1}})
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.create_spreadsheet_row(
        "spreadsheet123",
        "Sheet1!A1:B1",
        row=["a", "b"],
        value_input_option="RAW",
    )

    assert result["updates"]["updatedRows"] == 1
    _, _, kwargs = recorder.calls[0]
    assert kwargs["params"] == {"valueInputOption": "RAW"}
    assert kwargs["json"] == {"values": [["a", "b"]]}


@pytest.mark.asyncio
async def test_lookup_spreadsheet_rows_returns_objects(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleSheetsSettings,
) -> None:
    provider = GoogleSheetsProvider(settings=settings)
    recorder = RecordingRequest(
        {
            (
                "GET",
                "/spreadsheet123/values/Sheet1!A1:C4",
            ): StubResponse(
                {
                    "range": "Sheet1!A1:C4",
                    "values": [
                        ["Name", "Status", "Count"],
                        ["Widget", "Ready", "5"],
                        ["Cog", "Ready", "2"],
                        ["Widget", "Backlog", "1"],
                    ],
                }
            )
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.lookup_spreadsheet_rows(
        "spreadsheet123",
        "Sheet1!A1:C4",
        lookup_column="Name",
        lookup_value="Widget",
    )

    assert len(result["matches"]) == 2
    assert result["matched_row_numbers"] == [2, 4]


@pytest.mark.asyncio
async def test_find_or_create_row_creates_when_missing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GoogleSheetsSettings,
) -> None:
    provider = GoogleSheetsProvider(settings=settings)
    recorder = RecordingRequest(
        {
            (
                "GET",
                "/spreadsheet123/values/Sheet1!A1:C3",
            ): StubResponse(
                {"range": "Sheet1!A1:C3", "values": [["Name"], ["Gadget"]]}
            ),
            (
                "POST",
                "/spreadsheet123/values/Sheet1!A1:C3:append",
            ): StubResponse({"updates": {"updatedRows": 1}}),
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.find_or_create_row(
        "spreadsheet123",
        "Sheet1!A1:C3",
        lookup_column="Name",
        lookup_value="Widget",
        row=["Widget"],
        value_input_option="RAW",
    )

    assert result["created"] is True
    assert result["row"] == {"Name": "Widget"}
    assert recorder.calls[1][2]["params"] == {"valueInputOption": "RAW"}


@pytest.mark.asyncio
async def test_raw_request_action(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = GoogleSheetsProvider(settings=GoogleSheetsSettings(token="token"))
    recorder = RecordingRequest({("GET", "/custom"): StubResponse({"ok": True})})
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.raw_request(
        "GET",
        "/custom",
        params={"alt": "json"},
    )

    assert result == {"ok": True}
    method, slug, kwargs = recorder.calls[0]
    assert method == "GET"
    assert slug == "/custom"
    assert kwargs["params"] == {"alt": "json"}
