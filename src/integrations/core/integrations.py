"""Simple dependency container for managing integration providers."""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Any, Dict, Iterator, Mapping, Optional

from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic_settings import SettingsError

from .provider import BaseProvider, ProviderSettings
from .provider_key import ProviderIdentifier, ProviderKey, provider_key
from .registry import available_providers, get_provider

if TYPE_CHECKING:
    from ..providers import (
        AsanaProvider,
        GithubProvider,
        GmailProvider,
        GoogleCalendarProvider,
        GoogleDocsProvider,
        GoogleDriveProvider,
        GoogleSheetsProvider,
        HubspotProvider,
        NotionProvider,
        SlackProvider,
    )

ProviderInstance = BaseProvider[Any]
ProviderConfig = ProviderInstance | ProviderSettings | Mapping[str, Any]


class ProviderOverrideConfig(BaseModel):
    """Integrations override configuration options."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: ProviderConfig
    merge: bool = True


def provider_override(
    config: ProviderConfig,
    *,
    merge: bool = True,
) -> ProviderOverrideConfig:
    """Create an override configuration with an optional merge flag."""

    return ProviderOverrideConfig(config=config, merge=merge)


class Integrations:
    """Registry of providers that allows attribute access and overrides."""

    asana: "AsanaProvider"
    github: "GithubProvider"
    gmail: "GmailProvider"
    hubspot: "HubspotProvider"
    notion: "NotionProvider"
    slack: "SlackProvider"
    google_calendar: "GoogleCalendarProvider"
    google_docs: "GoogleDocsProvider"
    google_drive: "GoogleDriveProvider"
    google_sheets: "GoogleSheetsProvider"

    def __init__(
        self,
        *,
        auto_configure: bool = True,
        **providers: ProviderConfig,
    ) -> None:
        self._providers: Dict[str, ProviderInstance] = {}
        for name, config in providers.items():
            self._providers[name] = self._instantiate_provider(name, config)
        if auto_configure:
            self._auto_configure_missing_providers()

    def __getattr__(self, name: str) -> ProviderInstance:
        try:
            return self._providers[name]
        except KeyError as exc:  # pragma: no cover - defensive only
            raise AttributeError(f"Provider '{name}' is not registered") from exc

    def __getitem__(self, name: ProviderIdentifier) -> ProviderInstance:
        return self._providers[provider_key(name)]

    def __contains__(self, name: object) -> bool:
        if not isinstance(name, (ProviderKey, str)):
            return False
        return provider_key(name) in self._providers

    def __iter__(self) -> Iterator[str]:
        return iter(self._providers)

    def register(self, name: ProviderIdentifier, provider: ProviderConfig) -> None:
        """Register or replace a provider under ``name``."""
        key = provider_key(name)
        self._providers[key] = self._instantiate_provider(key, provider)

    def get(
        self,
        name: ProviderIdentifier,
        default: ProviderInstance | None = None,
    ) -> ProviderInstance | None:
        return self._providers.get(provider_key(name), default)

    def overrides(
        self,
        *,
        merge: bool | None = None,
        **overrides: ProviderConfig | ProviderOverrideConfig,
    ) -> AbstractAsyncContextManager["Integrations"]:
        """Return an async-aware context manager that temporarily overrides providers."""

        default_merge = True if merge is None else bool(merge)
        return _IntegrationsOverride(self, overrides, default_merge=default_merge)

    def _instantiate_provider(
        self,
        name: str,
        value: ProviderConfig,
        *,
        current: Optional[ProviderInstance] = None,
        merge: bool = False,
    ) -> ProviderInstance:
        if isinstance(value, BaseProvider):
            return value

        try:
            provider_cls = get_provider(name)
        except KeyError as exc:  # pragma: no cover - defensive only
            raise ValueError(f"No provider registered as '{name}'.") from exc

        if merge and current is not None:
            merged_settings = self._merge_settings(current, value)
            return provider_cls(settings=merged_settings)

        if isinstance(value, ProviderSettings):
            return provider_cls(settings=value)
        if isinstance(value, Mapping):
            return provider_cls(**dict(value))
        raise TypeError(
            f"Unsupported configuration for provider '{name}'. "
            "Expected Provider instance, ProviderSettings, or mapping of settings data."
        )

    @staticmethod
    def _merge_settings(
        current: ProviderInstance,
        update: ProviderConfig,
    ) -> ProviderSettings:
        base_settings = current.settings
        if isinstance(update, ProviderSettings):
            update_data = update.model_dump(exclude_unset=True)
        elif isinstance(update, Mapping):
            update_data = dict(update)
        else:
            raise TypeError(
                "Cannot merge provider instance overrides; pass merge=False to replace."
            )

        return base_settings.model_copy(update=update_data)

    def _auto_configure_missing_providers(self) -> None:
        for name, provider_cls in available_providers().items():
            if name in self._providers:
                continue

            try:
                provider = provider_cls()
            except (ValidationError, SettingsError):
                continue

            self._providers[name] = provider


class _IntegrationsOverride(AbstractAsyncContextManager[Integrations]):
    """Async-aware context manager that swaps providers while active."""

    def __init__(
        self,
        container: Integrations,
        overrides: Dict[str, ProviderConfig | ProviderOverrideConfig],
        *,
        default_merge: bool,
    ) -> None:
        self._container = container
        self._overrides = overrides
        self._default_merge = default_merge
        self._previous: Dict[str, ProviderInstance] = {}
        self._missing: set[str] = set()

    async def __aenter__(self) -> Integrations:
        self._apply()
        return self._container

    async def __aexit__(self, *_: Any) -> None:
        self._restore()

    def __enter__(self) -> Integrations:
        self._apply()
        return self._container

    def __exit__(self, *_: Any) -> None:
        self._restore()

    def _apply(self) -> None:
        for name, override in self._overrides.items():
            if isinstance(override, ProviderOverrideConfig):
                config = override.config
                merge_flag = override.merge
            else:
                config = override
                merge_flag = self._default_merge

            current = self._container._providers.get(name)
            provider = self._container._instantiate_provider(
                name,
                config,
                current=current if merge_flag else None,
                merge=merge_flag,
            )

            if name in self._container._providers:
                self._previous[name] = self._container._providers[name]
            else:
                self._missing.add(name)
            self._container._providers[name] = provider

    def _restore(self) -> None:
        for name in self._overrides:
            if name in self._missing:
                self._container._providers.pop(name, None)
            else:
                self._container._providers[name] = self._previous[name]
        self._previous.clear()
        self._missing.clear()
