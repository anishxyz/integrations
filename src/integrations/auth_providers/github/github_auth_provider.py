from __future__ import annotations

from collections.abc import Mapping, Sequence

from integrations.auth.auth_provider import AuthProvider
from integrations.auth.auth_provider_key import AuthProviderKey
from integrations.auth.flows import OAuth2Flow
from integrations.auth.registration import flow
from .github_bindings import GithubBinding
from .github_credentials import GithubAppCredentials, GithubUserCredentials


class GithubAuthProvider(AuthProvider[GithubAppCredentials, GithubUserCredentials]):
    """Auth entry point for GitHub integrations."""

    app_credentials_class = GithubAppCredentials
    user_credentials_class = GithubUserCredentials
    oauth2: OAuth2Flow[GithubAppCredentials, GithubUserCredentials] = flow(
        lambda provider: provider._build_oauth2_flow()
    )

    def default_bindings(self) -> Mapping[AuthProviderKey, GithubBinding]:
        return {AuthProviderKey.GITHUB: GithubBinding()}

    def _build_oauth2_flow(
        self,
    ) -> OAuth2Flow[GithubAppCredentials, GithubUserCredentials]:
        credentials = self.app_credentials
        default_scope = self._normalize_scope(
            getattr(credentials, "default_scope", None),
            credentials.scope_separator,
        )
        client_kwargs = getattr(credentials, "client_kwargs", None)

        if client_kwargs is not None and not isinstance(client_kwargs, Mapping):
            raise TypeError("client_kwargs must be a mapping when provided.")

        client_options = dict(client_kwargs) if client_kwargs is not None else None

        return OAuth2Flow(
            credentials,
            default_scope=default_scope,
            client_kwargs=client_options,
            token_class=GithubUserCredentials,
        )

    def _normalize_scope(
        self, scope: Sequence[str] | str | None, separator: str
    ) -> tuple[str, ...] | None:
        if scope is None:
            return None
        if isinstance(scope, str):
            parts = [item.strip() for item in scope.split(separator)]
            return tuple(filter(None, parts))
        if isinstance(scope, Sequence):
            return tuple(scope)
        raise TypeError("default_scope must be a sequence or string when provided.")
