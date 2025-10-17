from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from integrations.auth.storage import SubjectLike
from integrations.providers.github.github_settings import GithubSettings
from .github_credentials import GithubAppCredentials, GithubUserCredentials

if TYPE_CHECKING:  # pragma: no cover
    from integrations.auth.auth_manager import AuthManager


class GithubBinding:
    """Default binding that maps GitHub auth credentials into provider settings."""

    async def to_settings(
        self,
        *,
        manager: "AuthManager",
        provider: str,
        subject: SubjectLike,
        app_credentials: GithubAppCredentials,
        user_credentials: GithubUserCredentials | Mapping[str, str] | None,
    ) -> GithubSettings:
        token: str | None = None
        scheme: str | None = "Bearer"

        if isinstance(user_credentials, GithubUserCredentials):
            token = user_credentials.access_token
            scheme = user_credentials.token_type or scheme
        elif isinstance(user_credentials, Mapping):
            token = user_credentials.get("access_token")  # type: ignore[assignment]
            scheme = user_credentials.get("token_type", scheme)

        if not token:
            token = app_credentials.token
            if not token:
                raise ValueError(
                    "GitHub credentials missing token; store OAuth token or configure an app token."
                )

        return GithubSettings(token=token, authorization_scheme=scheme or "Bearer")


__all__ = ["GithubBinding"]
