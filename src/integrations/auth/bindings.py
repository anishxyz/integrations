from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, TYPE_CHECKING

from .storage import SubjectLike
from ..core.provider import ProviderSettings

if TYPE_CHECKING:  # pragma: no cover
    from .auth_manager import AuthManager
    from .credentials import AppCredentials, UserCredentials


class AuthBinding(Protocol):
    """Converts auth credentials into provider settings."""

    async def to_settings(
        self,
        *,
        manager: AuthManager,
        provider: str,
        subject: SubjectLike,
        app_credentials: AppCredentials,
        user_credentials: UserCredentials | Mapping[str, Any] | None,
    ) -> ProviderSettings: ...


__all__ = ["AuthBinding"]
