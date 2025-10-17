"""Shared auth provider for Google Workspace integrations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from integrations.auth.auth_provider import AuthProvider
from integrations.auth.auth_provider_key import AuthProviderKey
from integrations.auth.flows import OAuth2Flow
from integrations.auth.registration import flow

from .google_bindings import (
    GmailBinding,
    GoogleCalendarBinding,
    GoogleDocsBinding,
    GoogleDriveBinding,
    GoogleSheetsBinding,
)
from .google_credentials import GoogleAppCredentials, GoogleUserCredentials


class GoogleAuthProvider(AuthProvider[GoogleAppCredentials, GoogleUserCredentials]):
    """Auth entry point shared by the Google Workspace providers."""

    app_credentials_class = GoogleAppCredentials
    user_credentials_class = GoogleUserCredentials

    oauth2: OAuth2Flow[GoogleAppCredentials, GoogleUserCredentials] = flow(
        lambda provider: provider._build_oauth2_flow()
    )

    def default_bindings(
        self,
    ) -> Mapping[AuthProviderKey, object]:
        return {
            AuthProviderKey.GMAIL: GmailBinding(),
            AuthProviderKey.GOOGLE_CALENDAR: GoogleCalendarBinding(),
            AuthProviderKey.GOOGLE_DOCS: GoogleDocsBinding(),
            AuthProviderKey.GOOGLE_DRIVE: GoogleDriveBinding(),
            AuthProviderKey.GOOGLE_SHEETS: GoogleSheetsBinding(),
        }

    def _build_oauth2_flow(
        self,
    ) -> OAuth2Flow[GoogleAppCredentials, GoogleUserCredentials]:
        credentials = self.app_credentials
        default_scope = self._normalize_scope(
            getattr(credentials, "default_scope", None),
            credentials.scope_separator,
        )
        client_kwargs = getattr(credentials, "client_kwargs", None)

        if client_kwargs is not None and not isinstance(client_kwargs, Mapping):
            raise TypeError("client_kwargs must be a mapping when provided.")

        options = dict(client_kwargs or {})

        return OAuth2Flow(
            credentials,
            default_scope=default_scope,
            client_kwargs=options or None,
            token_class=GoogleUserCredentials,
        )

    def _normalize_scope(
        self,
        scope: Sequence[str] | str | None,
        separator: str,
    ) -> tuple[str, ...] | None:
        if scope is None:
            return None
        if isinstance(scope, str):
            parts = [item.strip() for item in scope.split(separator)]
            return tuple(filter(None, parts))
        if isinstance(scope, Sequence):
            return tuple(scope)
        raise TypeError("default_scope must be a sequence or string when provided.")


__all__ = ["GoogleAuthProvider"]
