"""Action for sending messages to Slack channels."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class SendChannelMessage(BaseAction):
    """Send a message to a Slack channel."""

    async def __call__(
        self,
        channel_id: str,
        text: str,
        *,
        thread_ts: str | None = None,
        blocks: list[dict[str, Any]] | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> Any:
        payload: dict[str, Any] = {
            "channel": channel_id,
            "text": text,
        }
        if thread_ts is not None:
            payload["thread_ts"] = thread_ts
        if blocks is not None:
            payload["blocks"] = blocks
        if attachments is not None:
            payload["attachments"] = attachments

        response = await self.provider.request(
            "POST",
            "/chat.postMessage",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
