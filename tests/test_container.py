"""Tests for the Container class covering common usage flows."""

from __future__ import annotations

import pytest

from integrations import (
    BaseAction,
    BaseProvider,
    Container,
    ProviderSettings,
    action,
    register_provider,
)
from pydantic_settings import SettingsConfigDict


class DummySettings(ProviderSettings):
    model_config = SettingsConfigDict(
        env_prefix="DUMMY_", extra="allow", populate_by_name=True
    )

    name: str
    nickname: str | None = None


class IdentAction(BaseAction):
    async def __call__(self) -> str:
        return self.provider.settings.name


class DummyProvider(BaseProvider[DummySettings]):
    settings_class = DummySettings
    ident = action(IdentAction)


register_provider("dummy", DummyProvider)


@pytest.fixture
def container() -> Container:
    return Container(dummy=DummySettings(name="default-dummy", nickname="base"))


@pytest.mark.asyncio
async def test_container_provides_attribute_access(container: Container) -> None:
    dummy = container.dummy
    assert isinstance(dummy, DummyProvider)
    assert dummy.settings.nickname == "base"
    assert await dummy.ident() == "default-dummy"


def test_container_accepts_mapping_configuration() -> None:
    container = Container(dummy={"name": "mapped", "nickname": "map"})
    assert container.dummy.settings.nickname == "map"


def test_container_falls_back_to_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DUMMY_NAME", "env-dummy")
    monkeypatch.setenv("DUMMY_NICKNAME", "env-nick")

    container = Container(dummy={})

    assert container.dummy.settings.name == "env-dummy"
    assert container.dummy.settings.nickname == "env-nick"


def test_environment_defaults_yield_to_explicit_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DUMMY_NAME", "env-dummy")

    container = Container(dummy={"name": "explicit"})

    assert container.dummy.settings.name == "explicit"


def test_environment_and_manual_values_can_mix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DUMMY_NICKNAME", "env-nick")

    container = Container(dummy={"name": "manual"})

    assert container.dummy.settings.name == "manual"
    assert container.dummy.settings.nickname == "env-nick"


@pytest.mark.asyncio
async def test_container_override_sync_context(container: Container) -> None:
    with container.overrides(dummy={"name": "override"}):
        dummy = container.dummy
        assert await dummy.ident() == "override"
        assert dummy.settings.nickname == "base"

    assert await container.dummy.ident() == "default-dummy"


@pytest.mark.asyncio
async def test_container_override_async_context(container: Container) -> None:
    async with container.overrides(dummy={"name": "async-override"}):
        dummy = container.dummy
        assert await dummy.ident() == "async-override"
        assert dummy.settings.nickname == "base"

    assert await container.dummy.ident() == "default-dummy"


@pytest.mark.asyncio
async def test_container_override_replacement(container: Container) -> None:
    with container.overrides(merge=False, dummy={"name": "replacement"}):
        dummy = container.dummy
        assert await dummy.ident() == "replacement"
        assert dummy.settings.nickname is None

    assert await container.dummy.ident() == "default-dummy"
