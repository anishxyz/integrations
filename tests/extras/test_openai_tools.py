"""Optional OpenAI Agents integration tests."""

from __future__ import annotations

import builtins
import json
import sys

import pytest

from agents.tool_context import ToolContext

from integrations import (
    BaseAction,
    BaseProvider,
    Integrations,
    ProviderSettings,
    action,
)
from integrations.providers.github.github_settings import GithubSettings


@pytest.mark.asyncio
async def test_actions_convert_to_openai_tools(monkeypatch: pytest.MonkeyPatch) -> None:
    container = Integrations(github=GithubSettings(token="token", user_agent="ua"))

    payload = [{"name": "repo"}]
    responses = {
        ("GET", "/user/repos", (("per_page", 5),)): StubResponse(payload),
    }

    clients: list[StubAsyncClient] = []

    def fake_client(**_):
        client = StubAsyncClient(responses=responses)
        clients.append(client)
        return client

    monkeypatch.setattr(container.github, "httpx_client", fake_client)

    tool = container.github.list_repositories.as_tool(platform="openai")
    ctx = ToolContext(context=None, tool_name=tool.name, tool_call_id="call-1")
    result = await tool.on_invoke_tool(ctx, json.dumps({"per_page": 5}))

    assert result == payload
    assert clients and clients[0].closed is True

    with pytest.raises(NotImplementedError):
        container.github.list_repositories.as_tool(platform="made-up")


def test_as_tool_requires_agents(monkeypatch: pytest.MonkeyPatch) -> None:
    cached_agents = {
        name: sys.modules.pop(name)
        for name in list(sys.modules)
        if name == "agents" or name.startswith("agents.")
    }

    original_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "agents" or name.startswith("agents."):
            raise ModuleNotFoundError("No module named 'agents'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    class DummySettings(ProviderSettings):
        token: str = "token"

    class DummyAction(BaseAction):
        async def __call__(self) -> str:
            return "ok"

    class DummyProvider(BaseProvider[DummySettings]):
        settings_class = DummySettings
        ping = action(DummyAction)

    provider = DummyProvider(settings=DummySettings())
    ping_action = provider.ping

    with pytest.raises(RuntimeError, match="The 'agents' package is required"):
        ping_action.as_tool()

    sys.modules.update(cached_agents)


class StubResponse:
    def __init__(self, payload, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP error: {self.status_code}")


class StubAsyncClient:
    def __init__(self, *, responses):
        self._responses = {}
        for key, value in responses.items():
            method, path, params = key
            normalized = (method.upper(), path, params)
            self._responses[normalized] = value
        self.closed = False

    async def __aenter__(self) -> "StubAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.closed = True

    async def request(self, method: str, path: str, *, params=None, **_):
        key = (method.upper(), path, tuple(sorted((params or {}).items())))
        try:
            return self._responses[key]
        except KeyError as exc:  # pragma: no cover - defensive
            raise AssertionError(f"Unexpected request: {method} {path}") from exc
