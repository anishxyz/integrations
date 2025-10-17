"""Auth provider for Asana."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from integrations.auth.auth_provider import AuthProvider
from integrations.auth.auth_provider_key import AuthProviderKey
from integrations.auth.flows import OAuth2Flow
from integrations.auth.registration import flow

from .asana_bindings import AsanaBinding
from .asana_credentials import AsanaAppCredentials, AsanaUserCredentials


class AsanaAuthProvider(AuthProvider[AsanaAppCredentials, AsanaUserCredentials]):
    """Auth entry point for Asana integrations."""

    app_credentials_class = AsanaAppCredentials
    user_credentials_class = AsanaUserCredentials

    oauth2: OAuth2Flow[AsanaAppCredentials, AsanaUserCredentials] = flow(
        lambda provider: provider._build_oauth2_flow()
    )

    def default_bindings(self) -> Mapping[AuthProviderKey, AsanaBinding]:
        return {AuthProviderKey.ASANA: AsanaBinding()}

    def _build_oauth2_flow(
        self,
    ) -> OAuth2Flow[AsanaAppCredentials, AsanaUserCredentials]:
        credentials = self.app_credentials
        default_scope = self._normalize_scope(
            getattr(credentials, "default_scope", None)
        )
        client_kwargs = getattr(credentials, "client_kwargs", None)

        if client_kwargs is not None and not isinstance(client_kwargs, Mapping):
            raise TypeError("client_kwargs must be a mapping when provided.")

        return OAuth2Flow(
            credentials,
            default_scope=default_scope,
            client_kwargs=dict(client_kwargs or {}),
            token_class=AsanaUserCredentials,
        )

    def _normalize_scope(
        self, scope: Sequence[str] | str | None
    ) -> tuple[str, ...] | None:
        if scope is None:
            return None
        if isinstance(scope, str):
            parts = [
                item.strip()
                for item in scope.split(self.app_credentials.scope_separator)
            ]
            return tuple(filter(None, parts))
        if isinstance(scope, Sequence):
            return tuple(scope)
        raise TypeError("default_scope must be a sequence or string when provided.")


__all__ = ["AsanaAuthProvider"]
