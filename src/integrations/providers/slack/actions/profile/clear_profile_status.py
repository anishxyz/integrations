"""Action for clearing Slack profile status."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...slack_provider import SlackProvider


class ClearProfileStatus(BaseAction):
    """Clear the calling user's Slack profile status."""

    provider: "SlackProvider"

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
