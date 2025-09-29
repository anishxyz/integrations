"""Action for clearing Slack profile status."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class ClearProfileStatus(BaseAction):
    """Clear the calling user's Slack profile status."""

    async def __call__(self) -> Any:
        profile = {
            "status_text": "",
            "status_emoji": "",
            "status_expiration": 0,
        }
        response = await self.provider.request(
            "POST",
            "/users.profile.set",
            json={"profile": profile},
        )
        return self.provider.process_httpx_response(response)
