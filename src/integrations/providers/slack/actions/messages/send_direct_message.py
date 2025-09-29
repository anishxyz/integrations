"""Action for sending direct messages on Slack."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class SendDirectMessage(BaseAction):
    """Send a direct message to a Slack user."""

    async def __call__(
        self,
        user_id: str,
        text: str,
        *,
        blocks: list[dict[str, Any]] | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> Any:
        open_response = await self.provider.request(
            "POST",
            "/conversations.open",
            json={"users": user_id},
        )
        open_payload = self.provider.process_httpx_response(open_response)
        channel = (
            open_payload.get("channel", {}) if isinstance(open_payload, dict) else {}
        )
        channel_id = channel.get("id")
        if not channel_id:
            raise ValueError(
                "Slack API did not return a channel id for DM conversation"
            )

        payload: dict[str, Any] = {
            "channel": channel_id,
            "text": text,
        }
        if blocks is not None:
            payload["blocks"] = blocks
        if attachments is not None:
            payload["attachments"] = attachments

        message_response = await self.provider.request(
            "POST",
            "/chat.postMessage",
            json=payload,
        )

        return self.provider.process_httpx_response(message_response)
