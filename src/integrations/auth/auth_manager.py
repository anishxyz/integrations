from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Dict

from pydantic import ValidationError
from pydantic_settings import SettingsError

from .auth_provider_key import (
    AuthProviderIdentifier,
    AuthProviderKey,
    auth_provider_key,
)
from .auth_registry import (
    available_auth_providers,
    get_auth_provider,
)
from .auth_provider import AuthProvider
from .credentials import AppCredentials, UserCredentials
from .storage import (
    CredentialStore,
    InMemoryCredentialStore,
    SubjectLike,
    StoredData,
)
from integrations.core.integrations import Integrations
from integrations.core.provider_key import (
    ProviderIdentifier as ContainerProviderIdentifier,
    provider_key as container_provider_key,
)

if TYPE_CHECKING:
    from integrations.auth_providers.asana import AsanaAuthProvider
    from integrations.auth_providers.github import GithubAuthProvider
    from integrations.auth_providers.google import GoogleAuthProvider
    from integrations.auth_providers.hubspot import HubspotAuthProvider
    from integrations.auth_providers.notion import NotionAuthProvider
    from integrations.auth_providers.slack import SlackAuthProvider

ProviderInstance = AuthProvider[Any, Any]
ProviderAuthConfig = ProviderInstance | AppCredentials | Mapping[str, Any]


class AuthManager:
    """Orchestrates auth providers and credential wiring."""

    asana: "AsanaAuthProvider"
    github: "GithubAuthProvider"
    google: "GoogleAuthProvider"
    hubspot: "HubspotAuthProvider"
    notion: "NotionAuthProvider"
    slack: "SlackAuthProvider"

    def __init__(
        self,
        *,
        auto_configure: bool = True,
        credential_store: CredentialStore | None = None,
        **providers: ProviderAuthConfig,
    ) -> None:
        self._providers: Dict[str, ProviderInstance] = {}
        self._explicit_providers: set[str] = set()
        self._credential_store: CredentialStore = (
            credential_store
            if credential_store is not None
            else InMemoryCredentialStore()
        )

        for name, config in providers.items():
            self.register(name, config)

        if auto_configure:
            self._auto_configure_missing_providers()

    def __getattr__(self, name: str) -> ProviderInstance:
        key = self._normalize_name(name)
        try:
            return self._providers[key]
        except KeyError as exc:  # pragma: no cover - defensive only
            raise AttributeError(f"Auth provider '{name}' is not registered") from exc

    def __contains__(self, name: object) -> bool:
        if not isinstance(name, str):
            return False
        normalized = self._normalize_name(name)
        return normalized in self._providers

    def __iter__(self) -> Iterator[str]:
        return iter(self._providers)

    def providers(self) -> Mapping[str, ProviderInstance]:
        """Return instantiated auth providers keyed by name."""
        return dict(self._providers)

    @property
    def credential_store(self) -> CredentialStore:
        """Return the configured credential store."""
        return self._credential_store

    def get_provider(self, name: str) -> ProviderInstance:
        """Fetch a specific auth provider by identifier."""
        key = self._normalize_name(name)
        try:
            return self._providers[key]
        except KeyError as exc:
            raise KeyError(f"Auth provider '{name}' is not registered") from exc

    def register(self, name: str, config: ProviderAuthConfig) -> None:
        """Register or replace a provider under ``name``."""
        key = self._normalize_name(name)
        provider = self._instantiate_provider(key, config)
        self._providers[key] = provider
        self._explicit_providers.add(key)

    def _instantiate_provider(
        self,
        name: str,
        value: ProviderAuthConfig,
    ) -> ProviderInstance:
        if isinstance(value, AuthProvider):
            return value

        provider_cls = self._lookup_provider_class(name)

        if isinstance(value, AppCredentials):
            return provider_cls(app_credentials=value)
        if isinstance(value, Mapping):
            return provider_cls(app_credentials=value)

        raise TypeError(
            f"Unsupported configuration for auth provider '{name}'. "
            "Expected AuthProvider instance, AppCredentials, or mapping."
        )

    async def load_credentials(
        self, provider: str, subject: SubjectLike
    ) -> UserCredentials | None:
        """Fetch and coerce credentials for ``subject`` from the store."""
        key = self._normalize_name(provider)
        raw = await self._credential_store.get(key, subject)
        if raw is None:
            return None
        auth_provider = self.get_provider(key)
        coerced = auth_provider.parse_user_credentials(raw)
        if coerced is None:
            return None
        return coerced

    async def store_credentials(
        self,
        provider: str,
        subject: SubjectLike,
        credentials: UserCredentials | StoredData,
    ) -> None:
        """Persist credentials for ``subject`` to the store."""
        data = self._serialize_credentials(credentials)
        key = self._normalize_name(provider)
        await self._credential_store.set(key, subject, data)

    async def delete_credentials(self, provider: str, subject: SubjectLike) -> None:
        """Remove credentials for ``subject`` from the store."""
        key = self._normalize_name(provider)
        await self._credential_store.delete(key, subject)

    @asynccontextmanager
    async def session(
        self,
        *,
        subject: SubjectLike,
        providers: Iterable[AuthProviderIdentifier] | None = None,
        overrides: Mapping[ContainerProviderIdentifier, Any] | None = None,
        with_credentials: Mapping[
            AuthProviderIdentifier, UserCredentials | Mapping[str, Any]
        ]
        | None = None,
        auto_load_credentials: bool = True,
    ) -> Integrations:
        """Yield an ``Integrations`` container configured with stored credentials."""

        provider_filter: set[AuthProviderKey] | None = None
        if providers is not None:
            provider_filter = {
                self._coerce_auth_provider_key(identifier) for identifier in providers
            }

        config: Dict[str, Any] = {}

        provided_credentials: dict[
            AuthProviderKey, UserCredentials | Mapping[str, Any]
        ] = {
            self._coerce_auth_provider_key(identifier): value
            for identifier, value in (with_credentials or {}).items()
        }

        for name, auth_provider in self._providers.items():
            is_explicit = name in self._explicit_providers
            bindings = auth_provider.bindings()
            if not bindings:
                continue

            try:
                self._coerce_auth_provider_key(name)
            except ValueError:
                continue

            store_key = self._normalize_name(name)

            for container_key, binding in bindings.items():
                if provider_filter and container_key not in provider_filter:
                    continue

                manual_source = provided_credentials.get(container_key)
                user_credentials = auth_provider.parse_user_credentials(manual_source)
                manual_supplied = manual_source is not None
                stored_raw: StoredData | None = None

                if user_credentials is None and auto_load_credentials:
                    stored_raw = await self._credential_store.get(store_key, subject)
                    user_credentials = auth_provider.parse_user_credentials(stored_raw)

                try:
                    settings = await binding.to_settings(
                        manager=self,
                        provider=container_key.value,
                        subject=subject,
                        app_credentials=auth_provider.app_credentials,
                        user_credentials=user_credentials,
                    )
                except ValueError:
                    if (
                        not is_explicit
                        and user_credentials is None
                        and not manual_supplied
                        and stored_raw is None
                        and (
                            provider_filter is None
                            or container_key not in provider_filter
                        )
                    ):
                        continue
                    raise

                config[container_key.value] = settings

        if overrides:
            for identifier, value in overrides.items():
                config[container_provider_key(identifier)] = value

        integrations = Integrations(auto_configure=True, **config)
        try:
            yield integrations
        finally:
            pass

    def _auto_configure_missing_providers(self) -> None:
        for name, provider_cls in available_auth_providers().items():
            if name in self._providers:
                continue

            try:
                provider = provider_cls()
            except (ValidationError, SettingsError, TypeError):
                continue

            self._providers[name] = provider

    @staticmethod
    def _serialize_credentials(
        credentials: UserCredentials | StoredData,
    ) -> Dict[str, Any]:
        if isinstance(credentials, UserCredentials):
            return credentials.model_dump(mode="json")
        if isinstance(credentials, Mapping):
            return dict(credentials)
        raise TypeError(
            "credentials must be a UserCredentials instance or mapping of credential data."
        )

    @staticmethod
    def _lookup_provider_class(
        name: str,
    ) -> type[AuthProvider[Any, Any]]:
        return get_auth_provider(name)

    @staticmethod
    def _coerce_auth_provider_key(
        identifier: AuthProviderIdentifier | str,
    ) -> AuthProviderKey:
        if isinstance(identifier, AuthProviderKey):
            return identifier
        key_value = auth_provider_key(identifier)
        try:
            return AuthProviderKey(key_value)
        except ValueError as exc:  # pragma: no cover - defensive only
            raise ValueError(
                f"Auth provider '{identifier}' is not supported by the AuthManager."
            ) from exc

    @staticmethod
    def _normalize_name(name: str) -> str:
        return name.replace("-", "_").lower()
