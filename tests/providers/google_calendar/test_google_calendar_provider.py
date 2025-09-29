"""Tests for the Google Calendar provider."""

from __future__ import annotations

import json
from typing import Any, Mapping

import pytest

from integrations.providers.google_calendar.actions.google_calendar_base_action import (
    GoogleCalendarBaseAction,
)
from integrations.providers.google_calendar.google_calendar_provider import (
    GoogleCalendarProvider,
)
from integrations.providers.google_calendar.google_calendar_settings import (
    GoogleCalendarSettings,
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
        self._json_payload = payload
        self.headers = dict(headers or {"Content-Type": "application/json"})
        if payload is None:
            self.content = b""
        else:
            self.content = json.dumps(payload).encode("utf-8")
        self.text = self.content.decode("utf-8", errors="ignore")

    def json(self) -> Any:
        if self._json_payload is None:
            raise ValueError("No JSON payload available")
        return self._json_payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class RecordingRequest:
    def __init__(
        self, responses: Mapping[tuple[str, str], StubResponse | list[StubResponse]]
    ) -> None:
        self._responses: dict[tuple[str, str], list[StubResponse]] = {}
        for key, value in responses.items():
            if isinstance(value, list):
                self._responses[key] = list(value)
            else:
                self._responses[key] = [value]
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    async def __call__(self, method: str, path: str, **kwargs: Any) -> StubResponse:
        method_key = method.upper()
        recorded_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.calls.append((method_key, path, recorded_kwargs))
        responses = self._responses[(method_key, path)]
        if not responses:
            raise AssertionError(f"No responses left for {method_key} {path}")
        return responses.pop(0)


@pytest.fixture
def settings() -> GoogleCalendarSettings:
    return GoogleCalendarSettings(
        token="ya29.calendar-token",
        user_agent="integrations-sdk-tests",
        default_calendar_id="team@calendar",
    )


def test_httpx_headers(settings: GoogleCalendarSettings) -> None:
    provider = GoogleCalendarProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"].startswith("Bearer ya29.calendar-token")
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert headers["User-Agent"] == "integrations-sdk-tests"


def test_resolve_calendar_id(settings: GoogleCalendarSettings) -> None:
    provider = GoogleCalendarProvider(settings=settings)
    helper = GoogleCalendarBaseAction(provider)
    assert helper.resolve_calendar_id(None) == "team@calendar"
    assert helper.resolve_calendar_id("custom@calendar") == "custom@calendar"

    primary_provider = GoogleCalendarProvider(
        settings=GoogleCalendarSettings(token="token")
    )
    primary_helper = GoogleCalendarBaseAction(primary_provider)
    assert primary_helper.resolve_calendar_id(None) == "primary"


@pytest.mark.asyncio
async def test_add_attendees_to_event_merges(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = GoogleCalendarProvider(settings=GoogleCalendarSettings(token="token"))
    recorder = RecordingRequest(
        {
            ("GET", "/calendars/primary/events/evt-123"): StubResponse(
                {
                    "attendees": [
                        {"email": "owner@example.com", "responseStatus": "accepted"}
                    ]
                }
            ),
            ("PATCH", "/calendars/primary/events/evt-123"): StubResponse(
                {"id": "evt-123"}
            ),
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.add_attendees_to_event(
        "evt-123",
        [
            "new@example.com",
            {"email": "owner@example.com", "displayName": "Owner"},
        ],
        send_updates="all",
    )

    assert result["added_count"] == 1
    assert result["added_attendees"] == [{"email": "new@example.com"}]
    get_call, patch_call = recorder.calls
    assert get_call[0] == "GET"
    assert patch_call[2]["params"] == {"sendUpdates": "all"}
    attendees = patch_call[2]["json"]["attendees"]
    assert {att["email"] for att in attendees} == {
        "owner@example.com",
        "new@example.com",
    }


@pytest.mark.asyncio
async def test_find_or_create_event_returns_existing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = GoogleCalendarProvider(settings=GoogleCalendarSettings(token="token"))
    recorder = RecordingRequest(
        {
            ("GET", "/calendars/primary/events"): StubResponse(
                {"items": [{"id": "evt-789", "summary": "Standup"}]}
            )
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.find_or_create_event(search_query="Standup")

    assert result["created"] is False
    assert result["event"]["id"] == "evt-789"
    method, path, kwargs = recorder.calls[0]
    assert method == "GET"
    assert path == "/calendars/primary/events"
    assert kwargs["params"]["maxResults"] == 1
    assert kwargs["params"]["singleEvents"] is True


@pytest.mark.asyncio
async def test_find_or_create_event_creates_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = GoogleCalendarProvider(settings=GoogleCalendarSettings(token="token"))
    recorder = RecordingRequest(
        {
            ("GET", "/calendars/custom@calendar/events"): StubResponse({"items": []}),
            ("POST", "/calendars/custom@calendar/events"): StubResponse(
                {"id": "evt-456"}
            ),
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result = await provider.find_or_create_event(
        calendar_id="custom@calendar",
        summary="Kickoff",
        start={"dateTime": "2024-01-01T10:00:00Z"},
        end={"dateTime": "2024-01-01T11:00:00Z"},
        send_updates="all",
        conference_data_version=1,
        supports_attachments=True,
    )

    assert result["created"] is True
    assert result["event"]["id"] == "evt-456"
    _, post_call = recorder.calls
    assert post_call[0] == "POST"
    assert post_call[1] == "/calendars/custom@calendar/events"
    assert post_call[2]["params"] == {
        "sendUpdates": "all",
        "conferenceDataVersion": 1,
        "supportsAttachments": True,
    }
    assert post_call[2]["json"]["summary"] == "Kickoff"


@pytest.mark.asyncio
async def test_raw_request_action(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = GoogleCalendarProvider(settings=GoogleCalendarSettings(token="token"))
    recorder = RecordingRequest(
        {
            ("GET", "/calendars/primary/events"): [
                StubResponse({"ok": True}),
                StubResponse({"ok": True}),
            ]
        }
    )
    monkeypatch.setattr(provider, "request", recorder)

    result_upper = await provider.raw_request("GET", "/calendars/primary/events")
    assert result_upper == {"ok": True}

    result_lower = await provider.raw_request("get", "/calendars/primary/events")
    assert result_lower == {"ok": True}
