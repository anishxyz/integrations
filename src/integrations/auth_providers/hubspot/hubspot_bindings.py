"""Bindings for HubSpot auth."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from integrations.auth.storage import SubjectLike
from integrations.providers.hubspot.hubspot_settings import HubspotSettings

from .hubspot_credentials import HubspotAppCredentials, HubspotUserCredentials

if TYPE_CHECKING:  # pragma: no cover
    from integrations.auth.auth_manager import AuthManager


class HubspotBinding:
    """Convert HubSpot auth credentials to provider settings."""

    async def to_settings(
        self,
        *,
        manager: "AuthManager",
        provider: str,
        subject: SubjectLike,
        app_credentials: HubspotAppCredentials,
        user_credentials: HubspotUserCredentials | Mapping[str, Any] | None,
    ) -> HubspotSettings:
        token: str | None = None

        if isinstance(user_credentials, HubspotUserCredentials):
            token = user_credentials.access_token
        elif isinstance(user_credentials, Mapping):
            token_value = user_credentials.get("access_token")
            if isinstance(token_value, str):
                token = token_value

        if not token:
            token = app_credentials.token

        if not token:
            raise ValueError(
                "HubSpot credentials missing access token; supply a user OAuth token or"
                " configure a private app token."
            )

        payload: dict[str, Any] = {"access_token": token}

        base_url = getattr(app_credentials, "base_url", None)
        if isinstance(user_credentials, Mapping):
            user_base_url = user_credentials.get("base_url")
        else:
            user_base_url = getattr(user_credentials, "base_url", None)
        resolved_base_url = user_base_url or base_url
        if isinstance(resolved_base_url, str):
            payload["base_url"] = resolved_base_url

        timeout = getattr(app_credentials, "timeout", None)
        if isinstance(user_credentials, Mapping):
            user_timeout = user_credentials.get("timeout")
        else:
            user_timeout = getattr(user_credentials, "timeout", None)
        resolved_timeout = user_timeout or timeout
        if isinstance(resolved_timeout, (int, float)):
            payload["timeout"] = float(resolved_timeout)

        user_agent = getattr(app_credentials, "user_agent", None)
        if isinstance(user_credentials, Mapping):
            user_user_agent = user_credentials.get("user_agent")
        else:
            user_user_agent = getattr(user_credentials, "user_agent", None)
        resolved_user_agent = user_user_agent or user_agent
        if isinstance(resolved_user_agent, str):
            payload["user_agent"] = resolved_user_agent

        return HubspotSettings(**payload)


__all__ = ["HubspotBinding"]
