from __future__ import annotations

from abc import ABC
from collections.abc import Mapping
from typing import Any, Dict, Generic, Mapping as TypingMapping, TypeVar, cast

from .auth_provider_key import (
    AuthProviderIdentifier,
    AuthProviderKey,
    normalize_auth_provider_key,
)
from .credentials import AppCredentials, UserCredentials
from .flows.base_auth_flow import BaseAuthFlow
from .registration import FlowFactory, declared_flow_names
from .bindings import AuthBinding

FlowT = TypeVar("FlowT", bound=BaseAuthFlow)
AppCredentialsT = TypeVar("AppCredentialsT", bound=AppCredentials)
UserCredentialsT = TypeVar("UserCredentialsT", bound=UserCredentials)


class AuthProvider(ABC, Generic[AppCredentialsT, UserCredentialsT]):
    """Shared contract for provider-specific auth orchestration."""

    app_credentials_class: type[AppCredentialsT] = cast(
        type[AppCredentialsT], AppCredentials
    )
    user_credentials_class: type[UserCredentialsT] = cast(
        type[UserCredentialsT], UserCredentials
    )

    def __init__(
        self,
        app_credentials: AppCredentialsT | TypingMapping[str, Any] | None = None,
        **app_data: Any,
    ) -> None:
        if app_credentials is not None and app_data:
            raise ValueError(
                "Provide either an app_credentials instance or keyword data, not both."
            )

        if app_credentials is None:
            source: TypingMapping[str, Any]
            if app_data:
                source = app_data
            else:
                source = {}
            coerced = self._coerce_app_credentials(source)
        else:
            coerced = self._coerce_app_credentials(app_credentials)

        self._app_credentials: AppCredentialsT = coerced

        self._flows: Dict[str, BaseAuthFlow] = {}
        self._bindings: Dict[AuthProviderKey, AuthBinding] = {
            normalize_auth_provider_key(name): binding
            for name, binding in self.default_bindings().items()
        }

    def _coerce_app_credentials(
        self, data: AppCredentialsT | TypingMapping[str, Any]
    ) -> AppCredentialsT:
        if isinstance(data, self.app_credentials_class):
            return data
        if isinstance(data, Mapping):
            return self.app_credentials_class(**data)
        raise TypeError(
            "app_credentials must be an instance of app_credentials_class or a mapping"
        )

    @property
    def app_credentials(self) -> AppCredentialsT:
        """Return the provider app credentials as configured."""
        return self._app_credentials

    def flows(self) -> Mapping[str, BaseAuthFlow]:
        """Return instantiated auth flows keyed by attribute name."""
        for name in declared_flow_names(self):
            getattr(self, name, None)
        return dict(self._flows)

    def bindings(self) -> Mapping[AuthProviderKey, AuthBinding]:
        """Return registered bindings keyed by provider identifier."""
        return dict(self._bindings)

    def default_bindings(self) -> Mapping[AuthProviderIdentifier, AuthBinding]:
        """Return default bindings for the auth provider."""
        return {}

    def register_binding(
        self, provider: AuthProviderIdentifier, binding: AuthBinding
    ) -> None:
        """Register or replace the binding for ``provider``."""
        key = normalize_auth_provider_key(provider)
        self._bindings[key] = binding

    def _get_or_create_flow(self, name: str, factory: FlowFactory[FlowT]) -> FlowT:
        try:
            return cast(FlowT, self._flows[name])
        except KeyError:
            flow = factory(self)
            self._flows[name] = flow
            return cast(FlowT, flow)

    def parse_user_credentials(
        self, data: UserCredentialsT | Mapping[str, Any] | None
    ) -> UserCredentialsT | None:
        if data is None:
            return None
        if isinstance(data, self.user_credentials_class):
            return data
        if isinstance(data, Mapping):
            return self.user_credentials_class.model_validate(data)
        raise TypeError(
            "user_credentials must be an instance of user_credentials_class or mapping"
        )
