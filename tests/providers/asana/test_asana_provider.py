from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Tuple

import pytest

from integrations.providers.asana.asana_provider import AsanaProvider
from integrations.providers.asana.asana_settings import AsanaSettings


class StubResponse:
    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers: dict[str, str] = {"Content-Type": "application/json"}

    def json(self) -> Any:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class StubAsyncClient:
    def __init__(
        self,
        responses: Mapping[Tuple[str, str], Iterable[StubResponse] | StubResponse],
    ) -> None:
        self._responses: Dict[Tuple[str, str], list[StubResponse]] = {}
        for key, value in responses.items():
            if isinstance(value, StubResponse):
                self._responses[key] = [value]
            else:
                self._responses[key] = list(value)
        self.calls: list[dict[str, Any]] = []
        self.closed = False

    async def __aenter__(self) -> "StubAsyncClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        self.closed = True

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
        files: Mapping[str, Any] | None = None,
        headers: Mapping[str, Any] | None = None,
    ) -> StubResponse:
        key = (method, path)
        try:
            responses = self._responses[key]
        except KeyError as exc:  # pragma: no cover - guard for unexpected calls
            raise AssertionError(f"Unexpected request: {method} {path}") from exc
        if not responses:
            raise AssertionError(f"No responses left for {method} {path}")
        response = responses.pop(0)
        self.calls.append(
            {
                "method": method,
                "path": path,
                "params": params,
                "json": json,
                "data": data,
                "files": files,
                "headers": headers,
            }
        )
        return response


@pytest.fixture
def settings() -> AsanaSettings:
    return AsanaSettings(token="asana-token", workspace_gid="123", user_agent="sdk")


def test_httpx_headers(settings: AsanaSettings) -> None:
    provider = AsanaProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "Bearer asana-token"
    assert headers["User-Agent"] == "sdk"
    assert headers["Accept"] == "application/json"


@pytest.mark.asyncio
async def test_create_task_uses_workspace_default(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("POST", "/tasks"): StubResponse({"data": {"gid": "task"}}),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    result = await provider.create_task(name="Test Task")

    assert result == {"gid": "task"}
    assert stub.calls[0]["json"] == {"data": {"name": "Test Task", "workspace": "123"}}
    assert stub.closed is True


@pytest.mark.asyncio
async def test_find_or_create_project_returns_existing(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("GET", "/projects"): StubResponse(
                {"data": [{"gid": "111", "name": "Marketing"}]}
            )
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    project = await provider.find_or_create_project(name="Marketing")

    assert project["gid"] == "111"
    assert stub.calls == [
        {
            "method": "GET",
            "path": "/projects",
            "params": {"workspace": "123", "archived": False},
            "json": None,
            "data": None,
            "files": None,
            "headers": None,
        }
    ]


@pytest.mark.asyncio
async def test_find_or_create_project_creates_when_missing(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("GET", "/projects"): StubResponse({"data": []}),
            ("POST", "/projects"): StubResponse(
                {"data": {"gid": "222", "name": "Roadmap"}}
            ),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    project = await provider.find_or_create_project(name="Roadmap", public=True)

    assert project == {"gid": "222", "name": "Roadmap"}
    assert stub.calls[1]["json"]["data"]["public"] is True


@pytest.mark.asyncio
async def test_raw_request_passthrough(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("PATCH", "/custom"): StubResponse({"data": {"ok": True}}),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    response = await provider.raw_request(
        "patch",
        "/custom",
        params={"foo": "bar"},
        headers={"X-Test": "1"},
    )

    assert response == {"ok": True}
    call = stub.calls[0]
    assert call["method"] == "PATCH"
    assert call["params"] == {"foo": "bar"}
    assert call["headers"] == {"X-Test": "1"}


@pytest.mark.asyncio
async def test_raw_request_defaults(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("GET", "/custom"): StubResponse({"data": {"ok": True}}),
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    payload = await provider.raw_request("get", "/custom")

    assert payload == {"ok": True}
    assert stub.calls[0]["method"] == "GET"


@pytest.mark.asyncio
async def test_find_tasks_in_workspace_handles_pagination(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("GET", "/tasks"): [
                StubResponse(
                    {
                        "data": [{"gid": "t1"}],
                        "next_page": {"offset": "abc"},
                    }
                ),
                StubResponse({"data": [{"gid": "t2"}]}),
            ]
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    tasks = await provider.find_tasks_in_workspace(fetch_all=True)

    assert tasks == [{"gid": "t1"}, {"gid": "t2"}]
    assert stub.calls[1]["params"]["offset"] == "abc"


@pytest.mark.asyncio
async def test_attach_file_uses_multipart_upload(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("POST", "/tasks/1/attachments"): StubResponse({"data": {"gid": "att"}})
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    attachment = await provider.attach_file(
        task_gid="1",
        file_name="note.txt",
        file_content=b"hello",
        content_type="text/plain",
    )

    assert attachment == {"gid": "att"}
    call = stub.calls[0]
    assert call["data"] == {"parent": "1"}
    assert call["files"]["file"][0] == "note.txt"
    assert call["files"]["file"][2] == "text/plain"


@pytest.mark.asyncio
async def test_find_user_by_email(
    monkeypatch: pytest.MonkeyPatch, settings: AsanaSettings
) -> None:
    provider = AsanaProvider(settings=settings)
    stub = StubAsyncClient(
        responses={
            ("GET", "/users"): StubResponse(
                {"data": [{"gid": "user", "email": "person@example.com"}]}
            )
        }
    )
    monkeypatch.setattr(provider, "httpx_client", lambda **_: stub)

    user = await provider.find_user(email="person@example.com")

    assert user["gid"] == "user"
    assert stub.calls[0]["params"]["workspace"] == "123"
