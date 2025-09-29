"""Action for setting Slack profile status."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class SetProfileStatus(BaseAction):
    """Set the calling user's Slack profile status."""

    async def __call__(
        self,
        status_text: str,
        *,
        status_emoji: str | None = None,
        status_expiration: int | None = None,
    ) -> Any:
        profile: dict[str, Any] = {
            "status_text": status_text,
            "status_emoji": status_emoji or "",
        }
        if status_expiration is not None:
            profile["status_expiration"] = status_expiration

        response = await self.provider.request(
            "POST",
            "/users.profile.set",
            json={"profile": profile},
        )
        return self.provider.process_httpx_response(response)
