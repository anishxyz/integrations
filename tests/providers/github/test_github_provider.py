"""Tests for the Github provider behaviour using mocked HTTP clients."""

from __future__ import annotations

import base64
from typing import Any, Dict, Mapping, Tuple

import pytest

from integrations import Integrations
from integrations.providers.github.github_provider import GithubProvider
from integrations.providers.github.github_settings import GithubSettings


class StubResponse:
    def __init__(
        self,
        payload: Any = None,
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


Key = Tuple[str, str, Tuple[Tuple[str, Any], ...]]


class StubAsyncClient:
    def __init__(
        self,
        *,
        responses: Dict[Key, StubResponse | list[StubResponse]],
        calls: list[dict],
    ) -> None:
        self._responses: Dict[Key, list[StubResponse]] = {}
        for key, value in responses.items():
            method, path, params = key
            normalized_key = (method.upper(), path, params)
            if isinstance(value, list):
                self._responses[normalized_key] = list(value)
            else:
                self._responses[normalized_key] = [value]
        self._calls = calls
        self.closed = False

    async def __aenter__(self) -> "StubAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.closed = True

    def _next_response(
        self, method: str, path: str, params: Tuple[Tuple[str, Any], ...]
    ) -> StubResponse:
        key = (method.upper(), path, params)
        try:
            bucket = self._responses[key]
        except KeyError as exc:  # pragma: no cover - defensive
            raise AssertionError(f"Unexpected request: {method} {path}") from exc
        if not bucket:
            raise AssertionError(f"No responses left for {method} {path}")
        return bucket.pop(0)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Dict[str, Any] | None = None,
        json: Any = None,
        data: Any = None,
        headers: Dict[str, Any] | None = None,
        **_: Any,
    ) -> StubResponse:
        params_tuple = tuple(sorted((params or {}).items()))
        method_upper = method.upper()
        self._calls.append(
            {
                "method": method_upper,
                "path": path,
                "params": params,
                "json": json,
                "data": data,
                "headers": headers,
            }
        )
        return self._next_response(method_upper, path, params_tuple)


@pytest.fixture
def settings() -> GithubSettings:
    return GithubSettings(token="token-123", user_agent="sdk", timeout=5)


def test_settings_allow_missing_token() -> None:
    settings = GithubSettings()
    assert settings.token is None
    assert settings.authorization_scheme == "Bearer"


def test_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "env-token")
    monkeypatch.setenv("GITHUB_USER_AGENT", "env-agent")

    settings = GithubSettings()

    assert settings.token == "env-token"
    assert settings.user_agent == "env-agent"


def test_settings_from_env_falls_back_to_pat(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GITHUB_PAT", "env-token")

    settings = GithubSettings()

    assert settings.token == "env-token"


def test_httpx_headers(settings: GithubSettings) -> None:
    provider = GithubProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "Bearer token-123"
    assert headers["User-Agent"] == "sdk"
    assert headers["X-GitHub-Api-Version"] == "2022-11-28"


def test_httpx_headers_with_custom_scheme() -> None:
    settings = GithubSettings(
        token="installation-token",
        authorization_scheme="token",
    )
    provider = GithubProvider(settings=settings)
    headers = provider.httpx_headers()
    assert headers["Authorization"] == "token installation-token"


@pytest.mark.asyncio
async def test_raw_request_delegates_to_provider(
    monkeypatch: pytest.MonkeyPatch, settings: GithubSettings
) -> None:
    provider = GithubProvider(settings=settings)
    captured: dict[str, Any] = {}
    stub_response = StubResponse(
        {"ok": True}, headers={"content-type": "application/json"}
    )

    async def fake_request(method: str, path: str, **kwargs: Any) -> StubResponse:
        captured.update({"method": method, "path": path, "kwargs": kwargs})
        return stub_response

    monkeypatch.setattr(provider, "request", fake_request)

    result = await provider.raw_request("GET", "/user", params={"a": 1})

    assert result == {"ok": True}
    assert captured["method"] == "GET"
    assert captured["path"] == "/user"
    assert captured["kwargs"]["params"] == {"a": 1}


@pytest.mark.asyncio
async def test_list_repositories_uses_client_and_returns_payload(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    payload = [{"name": "repo"}]
    responses = {
        ("GET", "/user/repos", ()): StubResponse(payload),
    }
    calls: list[dict] = []
    client_kwargs: list[dict] = []
    clients: list[StubAsyncClient] = []

    def fake_client(**kwargs):
        stub = StubAsyncClient(responses=responses, calls=calls)
        client_kwargs.append(kwargs)
        clients.append(stub)
        return stub

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.list_repositories()

    assert result == payload
    assert client_kwargs[0].get("timeout") is None
    assert calls[0]["method"] == "GET"
    assert calls[0]["path"] == "/user/repos"
    assert clients[0].closed is True


@pytest.mark.asyncio
async def test_list_codespaces(
    monkeypatch: pytest.MonkeyPatch, settings: GithubSettings
) -> None:
    provider = GithubProvider(settings=settings)
    payload = {"total_count": 1, "codespaces": []}
    responses = {
        ("GET", "/user/codespaces", (("per_page", 30),)): StubResponse(payload),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.list_codespaces(per_page=30)

    assert result == payload
    assert calls[0]["path"] == "/user/codespaces"
    assert calls[0]["params"] == {"per_page": 30}


@pytest.mark.asyncio
async def test_list_repository_codespaces(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    payload = {"total_count": 2, "codespaces": [{"name": "one"}, {"name": "two"}]}
    responses = {
        (
            "GET",
            "/repos/octo/proj/codespaces",
            (("page", 2),),
        ): StubResponse(payload),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.list_repository_codespaces("octo", "proj", page=2)

    assert result == payload
    assert calls[0]["path"] == "/repos/octo/proj/codespaces"
    assert calls[0]["params"] == {"page": 2}


@pytest.mark.asyncio
async def test_get_authenticated_user(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    payload = {"login": "octocat"}
    responses = {
        ("GET", "/user", ()): StubResponse(payload),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    user = await provider.get_authenticated_user()
    assert user == payload
    assert calls[0]["method"] == "GET"
    assert calls[0]["path"] == "/user"


@pytest.mark.asyncio
async def test_create_or_update_file_encodes_content(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    responses = {
        (
            "PUT",
            "/repos/octo/proj/contents/README.md",
            (),
        ): StubResponse({"content": {"sha": "abc123"}}),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.create_or_update_file(
        "octo",
        "proj",
        "README.md",
        message="docs",
        content="hello world",
    )

    assert result["content"]["sha"] == "abc123"
    encoded = calls[0]["json"]["content"]
    assert base64.b64decode(encoded).decode() == "hello world"


@pytest.mark.asyncio
async def test_create_codespace(
    monkeypatch: pytest.MonkeyPatch, settings: GithubSettings
) -> None:
    provider = GithubProvider(settings=settings)
    responses = {
        (
            "POST",
            "/repos/octo/proj/codespaces",
            (),
        ): StubResponse({"name": "my-space"}),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.create_codespace(
        "octo",
        "proj",
        ref="main",
        machine="standardLinux32gb",
    )

    assert result["name"] == "my-space"
    assert calls[0]["json"] == {"ref": "main", "machine": "standardLinux32gb"}


@pytest.mark.asyncio
async def test_codespace_lifecycle_actions(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    responses = {
        ("GET", "/user/codespaces/my-space", ()): StubResponse({"name": "my-space"}),
        ("POST", "/user/codespaces/my-space/start", ()): StubResponse(
            {"state": "Starting"}
        ),
        ("POST", "/user/codespaces/my-space/stop", ()): StubResponse(
            {"state": "Stopped"}
        ),
        ("DELETE", "/user/codespaces/my-space", ()): StubResponse(status_code=202),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    details = await provider.get_codespace("my-space")
    started = await provider.start_codespace("my-space")
    stopped = await provider.stop_codespace("my-space")
    deleted = await provider.delete_codespace("my-space")

    assert details["name"] == "my-space"
    assert started["state"] == "Starting"
    assert stopped["state"] == "Stopped"
    assert deleted is None
    assert [call["method"] for call in calls] == ["GET", "POST", "POST", "DELETE"]


@pytest.mark.asyncio
async def test_create_pull_request_with_merge(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    responses = {
        ("POST", "/repos/octo/proj/pulls", ()): StubResponse({"number": 7}),
        ("PUT", "/repos/octo/proj/pulls/7/merge", ()): StubResponse({"merged": True}),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    result = await provider.create_pull_request(
        "octo",
        "proj",
        title="Add feature",
        head="octo:feature",
        base="main",
        merge=True,
        merge_method="squash",
    )

    assert result["pull_request"]["number"] == 7
    assert result["merge"]["merged"] is True
    assert calls[0]["method"] == "POST"
    assert calls[1]["method"] == "PUT"
    assert calls[1]["json"]["merge_method"] == "squash"


@pytest.mark.asyncio
async def test_find_or_create_issue_prefers_existing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    search_query = '"Bug"'
    responses = {
        (
            "GET",
            "/search/issues",
            (
                ("per_page", 1),
                ("q", f"repo:octo/proj in:title state:open {search_query}"),
            ),
        ): StubResponse({"total_count": 1, "items": [{"number": 12}]}),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    issue = await provider.find_or_create_issue("octo", "proj", "Bug")
    assert issue["number"] == 12
    assert len(calls) == 1
    assert calls[0]["path"] == "/search/issues"


@pytest.mark.asyncio
async def test_find_or_create_issue_creates_when_missing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    responses = {
        (
            "GET",
            "/search/issues",
            (("per_page", 1), ("q", 'repo:octo/proj in:title state:open "Bug"')),
        ): StubResponse({"total_count": 0, "items": []}),
        (
            "POST",
            "/repos/octo/proj/issues",
            (),
        ): StubResponse({"number": 33}),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    issue = await provider.find_or_create_issue("octo", "proj", "Bug")
    assert issue["number"] == 33
    assert calls[1]["path"] == "/repos/octo/proj/issues"


@pytest.mark.asyncio
async def test_check_org_membership_handles_missing(
    monkeypatch: pytest.MonkeyPatch,
    settings: GithubSettings,
) -> None:
    provider = GithubProvider(settings=settings)
    responses = {
        ("GET", "/orgs/my-org/memberships/octocat", ()): StubResponse(status_code=404),
    }
    calls: list[dict] = []

    def fake_client(**_):
        return StubAsyncClient(responses=responses, calls=calls)

    monkeypatch.setattr(provider, "httpx_client", fake_client)

    membership = await provider.check_organization_membership("my-org", "octocat")
    assert membership is None
    assert calls[0]["path"] == "/orgs/my-org/memberships/octocat"


@pytest.mark.asyncio
async def test_container_end_to_end(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = GithubSettings(token="token-xyz", user_agent="sdk")
    container = Integrations(github=settings)

    responses = {
        ("GET", "/user", ()): StubResponse({"login": "octocat"}),
        ("GET", "/user/repos", (("per_page", 5),)): StubResponse(
            [
                {"name": "repo-1"},
                {"name": "repo-2"},
            ]
        ),
    }
    calls: list[dict] = []
    clients: list[StubAsyncClient] = []

    def stub_client(**_):
        client = StubAsyncClient(responses=responses, calls=calls)
        clients.append(client)
        return client

    monkeypatch.setattr(container.github, "httpx_client", stub_client)

    repos = await container.github.list_repositories(per_page=5)
    user = await container.github.get_authenticated_user()

    assert [repo["name"] for repo in repos] == ["repo-1", "repo-2"]
    assert user["login"] == "octocat"
    assert all(client.closed for client in clients)
