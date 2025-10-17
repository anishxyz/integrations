"""Bindings that project Google credentials into provider settings."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from integrations.auth.storage import SubjectLike
from integrations.providers.gmail.gmail_settings import GmailSettings
from integrations.providers.google_calendar.google_calendar_settings import (
    GoogleCalendarSettings,
)
from integrations.providers.google_docs.google_docs_settings import GoogleDocsSettings
from integrations.providers.google_drive.google_drive_settings import (
    GoogleDriveSettings,
)
from integrations.providers.google_sheets.google_sheets_settings import (
    GoogleSheetsSettings,
)

from .google_credentials import GoogleAppCredentials, GoogleUserCredentials

if TYPE_CHECKING:  # pragma: no cover
    from integrations.auth.auth_manager import AuthManager


SettingsT = TypeVar("SettingsT")


class GoogleBinding(Generic[SettingsT]):
    """Base helper that converts OAuth tokens into provider settings."""

    def __init__(
        self,
        settings_cls: type[SettingsT],
        *,
        token_field: str = "token",
        scheme_field: str | None = "authorization_scheme",
        extra_fields: Sequence[str] = (),
    ) -> None:
        self._settings_cls = settings_cls
        self._token_field = token_field
        self._scheme_field = scheme_field
        self._extra_fields = tuple(extra_fields)

    async def to_settings(
        self,
        *,
        manager: "AuthManager",
        provider: str,
        subject: SubjectLike,
        app_credentials: GoogleAppCredentials,
        user_credentials: GoogleUserCredentials | Mapping[str, Any] | None,
    ) -> SettingsT:
        token: str | None = None
        scheme: str | None = "Bearer"

        if isinstance(user_credentials, GoogleUserCredentials):
            token = user_credentials.access_token
            scheme = user_credentials.token_type or scheme
        elif isinstance(user_credentials, Mapping):
            token_value = user_credentials.get("access_token")
            if isinstance(token_value, str):
                token = token_value
            token_type_value = user_credentials.get("token_type")
            if isinstance(token_type_value, str):
                scheme = token_type_value or scheme

        if not token:
            if isinstance(app_credentials.token, str) and app_credentials.token:
                token = app_credentials.token
            else:
                token_value = getattr(app_credentials, "access_token", None)
                if isinstance(token_value, str) and token_value:
                    token = token_value

        if not token:
            raise ValueError(
                "Google credentials missing access token; run the OAuth flow or provide"
                " a service account token via app credentials."
            )

        payload: dict[str, Any] = {self._token_field: token}

        if self._scheme_field:
            payload[self._scheme_field] = scheme or "Bearer"

        for field in self._extra_fields:
            value = self._resolve_extra(field, app_credentials, user_credentials)
            if value is not None:
                payload[field] = value

        return self._settings_cls(**payload)

    def _resolve_extra(
        self,
        field: str,
        app_credentials: GoogleAppCredentials,
        user_credentials: GoogleUserCredentials | Mapping[str, Any] | None,
    ) -> Any:
        if isinstance(user_credentials, GoogleUserCredentials):
            value = getattr(user_credentials, field, None)
            if value is not None:
                return value
        elif isinstance(user_credentials, Mapping):
            value = user_credentials.get(field)
            if value is not None:
                return value

        value = getattr(app_credentials, field, None)
        if value is not None:
            return value
        return None


class GmailBinding(GoogleBinding[GmailSettings]):
    def __init__(self) -> None:
        super().__init__(
            GmailSettings,
            extra_fields=(
                "user_id",
                "base_url",
                "timeout",
            ),
        )


class GoogleCalendarBinding(GoogleBinding[GoogleCalendarSettings]):
    def __init__(self) -> None:
        super().__init__(
            GoogleCalendarSettings,
            extra_fields=(
                "base_url",
                "timeout",
                "user_agent",
                "default_calendar_id",
            ),
        )


class GoogleDocsBinding(GoogleBinding[GoogleDocsSettings]):
    def __init__(self) -> None:
        super().__init__(
            GoogleDocsSettings,
            extra_fields=(
                "base_url",
                "timeout",
                "user_agent",
            ),
        )


class GoogleDriveBinding(GoogleBinding[GoogleDriveSettings]):
    def __init__(self) -> None:
        super().__init__(
            GoogleDriveSettings,
            extra_fields=(
                "base_url",
                "upload_base_url",
                "timeout",
                "user_agent",
                "default_drive_id",
                "default_parent_id",
            ),
        )


class GoogleSheetsBinding(GoogleBinding[GoogleSheetsSettings]):
    def __init__(self) -> None:
        super().__init__(
            GoogleSheetsSettings,
            extra_fields=(
                "base_url",
                "timeout",
                "user_agent",
                "default_spreadsheet_id",
            ),
        )


__all__ = [
    "GmailBinding",
    "GoogleCalendarBinding",
    "GoogleDocsBinding",
    "GoogleDriveBinding",
    "GoogleSheetsBinding",
]
