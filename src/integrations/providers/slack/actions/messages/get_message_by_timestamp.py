"""Action for retrieving a Slack message by timestamp."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class GetMessageByTimestamp(BaseAction):
    """Fetch a Slack message by its timestamp."""

    async def __call__(
        self,
        channel_id: str,
        message_ts: str,
    ) -> Any:
        params = {
            "channel": channel_id,
            "latest": message_ts,
            "inclusive": True,
            "limit": 1,
        }
        response = await self.provider.request(
            "GET",
            "/conversations.history",
            params=params,
        )
        payload = self.provider.process_httpx_response(response)
        messages = payload.get("messages", []) if isinstance(payload, dict) else []
        return messages[0] if messages else None
