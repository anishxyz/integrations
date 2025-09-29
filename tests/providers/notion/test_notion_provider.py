"""Tests for the Notion provider using mocked HTTP interactions."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

import pytest

from integrations.providers.notion.notion_provider import NotionProvider
from integrations.providers.notion.notion_settings import NotionSettings


class StubResponse:
    def __init__(
        self,
        payload: Any = None,
        *,
        status_code: int = 200,
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
    def text(self) -> str:
        if self._text is not None:
            return self._text
        if isinstance(self._payload, str):
            return self._payload
        return ""

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


Key = Tuple[str, str, Tuple[Tuple[str, Any], ...]]


class StubAsyncClient:
    def __init__(self, *, responses: Dict[Key, StubResponse], calls: list[dict]):
        self._responses = responses
        self._calls = calls
        self.closed = False

    async def __aenter__(self) -> "StubAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.closed = True

    async def request(self, method: str, url: str, **kwargs: Any) -> StubResponse:
        key = (
            method.upper(),
            url,
            tuple(sorted((kwargs.get("params") or {}).items())),
        )
        self._calls.append(
            {
                "method": method.upper(),
                "url": url,
                "params": kwargs.get("params"),
                "json": kwargs.get("json"),
                "data": kwargs.get("data"),
                "headers": kwargs.get("headers"),
            }
        )
        try:
            return self._responses[key]
        except KeyError as exc:  # pragma: no cover - defensive guard
            raise AssertionError(f"Unexpected request: {key}") from exc


@pytest.fixture
def settings() -> NotionSettings:
    return NotionSettings(token="secret", timeout=5.0, user_agent="sdk")


def test_settings_defaults() -> None:
    settings = NotionSettings()
    assert settings.token is None
    assert settings.version == "2022-06-28"
    assert settings.base_url == "https://api.notion.com/v1"
    assert settings.timeout == 10.0
    assert settings.user_agent == "integrations-sdk"


def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_INTEGRATION_TOKEN", "env-token")
    monkeypatch.setenv("NOTION_VERSION", "2023-01-01")
    monkeypatch.setenv("NOTION_BASE_URL", "https://example.notion.com/v1")
    monkeypatch.setenv("NOTION_TIMEOUT", "12.5")
    monkeypatch.setenv("NOTION_USER_AGENT", "env-sdk")

    settings = NotionSettings()

    assert settings.token == "env-token"
    assert settings.version == "2023-01-01"
    assert settings.base_url == "https://example.notion.com/v1"
    assert settings.timeout == 12.5
    assert settings.user_agent == "env-sdk"


def test_httpx_headers(settings: NotionSettings) -> None:
    provider = NotionProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "Bearer secret"
    assert headers["Notion-Version"] == settings.version
    assert headers["Content-Type"] == "application/json"
    assert headers["User-Agent"] == "sdk"


def test_httpx_headers_missing_token() -> None:
    provider = NotionProvider(settings=NotionSettings(token=None))
    with pytest.raises(ValueError, match="Notion token is required"):
        provider.httpx_headers()


def test_process_response_handles_204(settings: NotionSettings) -> None:
    provider = NotionProvider(settings=settings)
    response = StubResponse(
        status_code=204, headers={"content-type": "application/json"}
    )
    assert provider.parse_httpx_response(response, empty_value={}) == {}


def test_process_response_returns_json(settings: NotionSettings) -> None:
    provider = NotionProvider(settings=settings)
    payload = {"id": "123"}
    response = StubResponse(payload)
    assert provider.parse_httpx_response(response, empty_value={}) == payload


def test_process_response_returns_text(settings: NotionSettings) -> None:
    provider = NotionProvider(settings=settings)
    response = StubResponse(
        "ok",
        headers={"content-type": "text/plain"},
    )
    assert provider.parse_httpx_response(response, empty_value={}) == "ok"


@pytest.mark.asyncio
async def test_request_uses_httpx_client(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    payload = {"result": True}
    responses = {
        ("GET", "databases/db-1", ()): StubResponse(payload),
    }
    calls: list[dict] = []
    client_kwargs: list[dict] = []
    clients: list[StubAsyncClient] = []

    def fake_async_client(**kwargs: Any) -> StubAsyncClient:
        client_kwargs.append(kwargs)
        stub = StubAsyncClient(responses=responses, calls=calls)
        clients.append(stub)
        return stub

    monkeypatch.setattr(
        "integrations.core.mixins.httpx.httpx.AsyncClient",
        fake_async_client,
    )

    response = await provider.request("GET", "databases/db-1")
    result = provider.process_httpx_response(response)

    assert result == payload
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "databases/db-1"
    assert calls[0]["json"] is None
    assert client_kwargs[0]["base_url"] == "https://api.notion.com/v1"
    assert client_kwargs[0]["timeout"] == 5.0
    assert "Authorization" in client_kwargs[0]["headers"]
    assert clients[0].closed is True


@pytest.mark.asyncio
async def test_raw_request_delegates_to_provider(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}

    class DummyResponse:
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

    stub_response: Any = DummyResponse()

    async def fake_request(method: str, slug: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "slug": slug, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"ok": True}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.raw_request(
        "POST",
        "pages",
        params={"page_size": 5},
        json={"title": "Doc"},
    )

    assert result == {"ok": True}
    assert captured["method"] == "POST"
    assert captured["slug"] == "pages"
    assert captured["kwargs"]["params"] == {"page_size": 5}
    assert captured["kwargs"]["json"] == {"title": "Doc"}


@pytest.mark.asyncio
async def test_raw_request_accepts_full_url(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}

    class DummyResponse:
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

    stub_response: Any = DummyResponse()

    async def fake_request(method: str, slug: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "slug": slug, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"status": "ok"}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.raw_request(
        "PATCH",
        "https://api.notion.com/v1/pages/abc",
        headers={"X-Test": "1"},
        data={"key": "value"},
    )

    assert result == {"status": "ok"}
    assert captured["method"] == "PATCH"
    assert captured["slug"] == "https://api.notion.com/v1/pages/abc"
    assert captured["kwargs"]["headers"] == {"X-Test": "1"}
    assert captured["kwargs"]["data"] == {"key": "value"}


@pytest.mark.asyncio
async def test_archive_database_item(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"archived": True}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.archive_database_item("page-1")

    assert result == {"archived": True}
    assert captured["method"] == "PATCH"
    assert captured["url"] == "pages/page-1"
    assert captured["kwargs"]["json"] == {"archived": True}


@pytest.mark.asyncio
async def test_create_database_item(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"id": "item"}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.create_database_item(
        "db-1",
        {"Name": {"title": "Doc"}},
        children=[{"type": "paragraph"}],
        icon={"type": "emoji", "emoji": "doc-emoji"},
        cover={"type": "external", "external": {"url": "https://example"}},
    )

    assert result == {"id": "item"}
    json_payload = captured["kwargs"]["json"]
    assert json_payload["parent"] == {"database_id": "db-1"}
    assert json_payload["properties"] == {"Name": {"title": "Doc"}}
    assert json_payload["children"] == [{"type": "paragraph"}]
    assert json_payload["icon"] == {"type": "emoji", "emoji": "doc-emoji"}
    assert json_payload["cover"] == {
        "type": "external",
        "external": {"url": "https://example"},
    }


@pytest.mark.asyncio
async def test_update_database_item(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"id": "page"}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.update_database_item(
        "page-1",
        properties={"Status": {"select": {"name": "Done"}}},
        archived=False,
        icon={"type": "emoji", "emoji": "check-emoji"},
        cover={"type": "external", "external": {"url": "https://cover"}},
    )

    assert result == {"id": "page"}
    assert captured["method"] == "PATCH"
    assert captured["url"] == "pages/page-1"
    assert captured["kwargs"]["json"] == {
        "properties": {"Status": {"select": {"name": "Done"}}},
        "archived": False,
        "icon": {"type": "emoji", "emoji": "check-emoji"},
        "cover": {"type": "external", "external": {"url": "https://cover"}},
    }


@pytest.mark.asyncio
async def test_add_content_to_page(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"appended": True}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.add_content_to_page(
        "block-1",
        [{"type": "paragraph"}],
        after="child-1",
    )

    assert result == {"appended": True}
    assert captured["url"] == "blocks/block-1/children"
    assert captured["kwargs"]["json"] == {
        "children": [{"type": "paragraph"}],
        "after": "child-1",
    }


@pytest.mark.asyncio
async def test_create_page(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"id": "page"}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.create_page(
        {"type": "database_id", "database_id": "db-1"},
        properties={"Title": {"title": "Doc"}},
        children=[{"type": "heading_1"}],
        icon={"type": "emoji", "emoji": "doc-emoji"},
        cover={"type": "external", "external": {"url": "https://cover"}},
    )

    assert result == {"id": "page"}
    assert captured["method"] == "POST"
    assert captured["url"] == "pages"
    assert captured["kwargs"]["json"] == {
        "parent": {"type": "database_id", "database_id": "db-1"},
        "properties": {"Title": {"title": "Doc"}},
        "children": [{"type": "heading_1"}],
        "icon": {"type": "emoji", "emoji": "doc-emoji"},
        "cover": {"type": "external", "external": {"url": "https://cover"}},
    }


@pytest.mark.asyncio
async def test_move_page(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"moved": True}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.move_page("page-1", {"workspace": True})

    assert result == {"moved": True}
    assert captured["method"] == "PATCH"
    assert captured["url"] == "pages/page-1"
    assert captured["kwargs"]["json"] == {"parent": {"workspace": True}}


@pytest.mark.asyncio
async def test_retrieve_helpers(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    calls: list[dict] = []

    async def fake_request(method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        calls.append({"method": method, "url": url})
        return {"data": url}

    def fake_process(response: Any, **_: Any) -> Any:
        return response

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    page = await provider.retrieve_page("page-1")
    database = await provider.retrieve_database("db-1")
    restored = await provider.restore_database_item("page-1")

    assert page == {"data": "pages/page-1"}
    assert database == {"data": "databases/db-1"}
    assert restored == {"data": "pages/page-1"}
    assert calls[0]["url"] == "pages/page-1"
    assert calls[1]["url"] == "databases/db-1"
    assert calls[2]["url"] == "pages/page-1"


@pytest.mark.asyncio
async def test_add_comment(
    monkeypatch: pytest.MonkeyPatch, settings: NotionSettings
) -> None:
    provider = NotionProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response: Any = object()

    async def fake_request(method: str, url: str, **kwargs: Any) -> Any:
        captured.update({"method": method, "url": url, "kwargs": kwargs})
        return stub_response

    def fake_process(response: Any, **_: Any) -> dict[str, Any]:
        assert response is stub_response
        return {"id": "comment"}

    monkeypatch.setattr(provider, "request", fake_request)
    monkeypatch.setattr(provider, "process_httpx_response", fake_process)

    result = await provider.add_comment(
        parent={"page_id": "page-1"},
        rich_text=[{"type": "text", "text": {"content": "Hello"}}],
    )

    assert result == {"id": "comment"}
    assert captured["method"] == "POST"
    assert captured["url"] == "comments"
    assert captured["kwargs"]["json"] == {
        "parent": {"page_id": "page-1"},
        "rich_text": [{"type": "text", "text": {"content": "Hello"}}],
    }
