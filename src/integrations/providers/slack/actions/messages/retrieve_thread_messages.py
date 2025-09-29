"""Action for retrieving Slack thread messages."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class RetrieveThreadMessages(BaseAction):
    """Retrieve messages that belong to a Slack thread."""

    async def __call__(
        self,
        channel_id: str,
        thread_ts: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {
            "channel": channel_id,
            "ts": thread_ts,
        }
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        response = await self.provider.request(
            "GET",
            "/conversations.replies",
            params=params,
        )
        payload = self.provider.process_httpx_response(response)
        if isinstance(payload, dict):
            return payload.get("messages", [])
        return payload
