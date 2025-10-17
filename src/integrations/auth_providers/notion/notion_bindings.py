"""Bindings for Notion auth."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from integrations.auth.storage import SubjectLike
from integrations.providers.notion.notion_settings import NotionSettings

from .notion_credentials import NotionAppCredentials, NotionUserCredentials

if TYPE_CHECKING:  # pragma: no cover
    from integrations.auth.auth_manager import AuthManager


class NotionBinding:
    """Convert Notion auth credentials into provider settings."""

    async def to_settings(
        self,
        *,
        manager: "AuthManager",
        provider: str,
        subject: SubjectLike,
        app_credentials: NotionAppCredentials,
        user_credentials: NotionUserCredentials | Mapping[str, Any] | None,
    ) -> NotionSettings:
        token: str | None = None

        if isinstance(user_credentials, NotionUserCredentials):
            token = user_credentials.access_token
        elif isinstance(user_credentials, Mapping):
            token_value = user_credentials.get("access_token")
            if isinstance(token_value, str):
                token = token_value

        if not token:
            token = app_credentials.token

        if not token:
            raise ValueError(
                "Notion credentials missing access token; provide an integration token or"
                " persist the OAuth access token."
            )

        payload: dict[str, Any] = {"token": token}

        version = self._extract_value("version", app_credentials, user_credentials)
        if isinstance(version, str):
            payload["version"] = version

        user_agent = self._extract_value(
            "user_agent", app_credentials, user_credentials
        )
        if isinstance(user_agent, str):
            payload["user_agent"] = user_agent

        timeout = self._extract_value("timeout", app_credentials, user_credentials)
        if isinstance(timeout, (int, float)):
            payload["timeout"] = float(timeout)

        base_url = self._extract_value("base_url", app_credentials, user_credentials)
        if isinstance(base_url, str):
            payload["base_url"] = base_url

        return NotionSettings(**payload)

    def _extract_value(
        self,
        field: str,
        app_credentials: NotionAppCredentials,
        user_credentials: NotionUserCredentials | Mapping[str, Any] | None,
    ) -> Any:
        if isinstance(user_credentials, NotionUserCredentials):
            value = getattr(user_credentials, field, None)
            if value is not None:
                return value
        elif isinstance(user_credentials, Mapping):
            value = user_credentials.get(field)
            if value is not None:
                return value
        return getattr(app_credentials, field, None)


__all__ = ["NotionBinding"]
