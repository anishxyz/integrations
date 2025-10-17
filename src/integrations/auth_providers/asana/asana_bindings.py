"""Bindings for the Asana auth provider."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from integrations.auth.storage import SubjectLike
from integrations.providers.asana.asana_settings import AsanaSettings

from .asana_credentials import AsanaAppCredentials, AsanaUserCredentials

if TYPE_CHECKING:  # pragma: no cover
    from integrations.auth.auth_manager import AuthManager


class AsanaBinding:
    """Map Asana auth credentials into provider settings."""

    async def to_settings(
        self,
        *,
        manager: "AuthManager",
        provider: str,
        subject: SubjectLike,
        app_credentials: AsanaAppCredentials,
        user_credentials: AsanaUserCredentials | Mapping[str, object] | None,
    ) -> AsanaSettings:
        token: str | None = None
        workspace_gid: str | None = app_credentials.workspace_gid

        if isinstance(user_credentials, AsanaUserCredentials):
            token = user_credentials.access_token
            workspace_gid = user_credentials.workspace_gid or workspace_gid
        elif isinstance(user_credentials, Mapping):
            token_value = user_credentials.get("access_token")
            if isinstance(token_value, str):
                token = token_value

            workspace_value = user_credentials.get("workspace_gid")
            if isinstance(workspace_value, str):
                workspace_gid = workspace_value

        if not token:
            token = app_credentials.token

        if not token:
            raise ValueError(
                "Asana credentials missing access token; supply a user token or configure"
                " an app token."
            )

        return AsanaSettings(token=token, workspace_gid=workspace_gid)


__all__ = ["AsanaBinding"]
