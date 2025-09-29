"""Action for leaving Slack channels."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class LeaveChannel(BaseAction):
    """Leave a Slack conversation."""

    async def __call__(self, channel_id: str) -> Any:
        response = await self.provider.request(
            "POST",
            "/conversations.leave",
            json={"channel": channel_id},
        )
        return self.provider.process_httpx_response(response)
