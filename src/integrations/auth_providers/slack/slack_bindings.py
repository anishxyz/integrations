"""Bindings for Slack auth."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from integrations.auth.storage import SubjectLike
from integrations.providers.slack.slack_settings import SlackSettings

from .slack_credentials import SlackAppCredentials, SlackUserCredentials

if TYPE_CHECKING:  # pragma: no cover
    from integrations.auth.auth_manager import AuthManager


class SlackBinding:
    """Convert Slack auth credentials into provider settings."""

    async def to_settings(
        self,
        *,
        manager: "AuthManager",
        provider: str,
        subject: SubjectLike,
        app_credentials: SlackAppCredentials,
        user_credentials: SlackUserCredentials | Mapping[str, Any] | None,
    ) -> SlackSettings:
        token: str | None = None

        if isinstance(user_credentials, SlackUserCredentials):
            token = user_credentials.access_token
        elif isinstance(user_credentials, Mapping):
            token_value = user_credentials.get("access_token")
            if isinstance(token_value, str):
                token = token_value

        if not token:
            token = app_credentials.bot_token or app_credentials.user_token

        if not token:
            raise ValueError(
                "Slack credentials missing access token; store the OAuth access token or"
                " configure a bot token."
            )

        payload: dict[str, Any] = {"token": token}

        for field in ("base_url", "timeout", "user_agent"):
            value = self._extract(field, app_credentials, user_credentials)
            if value is not None:
                payload[field] = value

        return SlackSettings(**payload)

    def _extract(
        self,
        field: str,
        app_credentials: SlackAppCredentials,
        user_credentials: SlackUserCredentials | Mapping[str, Any] | None,
    ) -> Any:
        if isinstance(user_credentials, SlackUserCredentials):
            value = getattr(user_credentials, field, None)
            if value is not None:
                return value
        elif isinstance(user_credentials, Mapping):
            value = user_credentials.get(field)
            if value is not None:
                return value
        return getattr(app_credentials, field, None)


__all__ = ["SlackBinding"]
