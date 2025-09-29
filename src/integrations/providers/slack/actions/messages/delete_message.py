"""Action for deleting Slack messages."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class DeleteMessage(BaseAction):
    """Delete a message from a Slack conversation."""

    async def __call__(self, channel_id: str, message_ts: str) -> Any:
        response = await self.provider.request(
            "POST",
            "/chat.delete",
            json={"channel": channel_id, "ts": message_ts},
        )
        return self.provider.process_httpx_response(response)
