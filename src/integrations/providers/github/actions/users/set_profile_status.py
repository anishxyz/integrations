"""Action for updating the authenticated user's profile status."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class SetProfileStatus(BaseAction):
    """Set the profile status for the authenticated user."""

    provider: "GithubProvider"

    async def __call__(
        self,
        *,
        emoji: str | None = None,
        message: str | None = None,
        expires_at: str | None = None,
        limited_availability: bool | None = None,
        organization_id: int | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {}

        if emoji is not None:
            payload["emoji"] = emoji
        if message is not None:
            payload["message"] = message
        if expires_at is not None:
            payload["expires_at"] = expires_at
        if limited_availability is not None:
            payload["limited_availability"] = limited_availability
        if organization_id is not None:
            payload["organization_id"] = organization_id

        response = await self.provider.request(
            "PUT",
            "/user/status",
            json=payload or None,
        )
        return self.provider.process_httpx_response(response)
