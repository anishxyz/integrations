"""Action for listing Slack conversation members."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class FindConversationMembers(BaseAction):
    """List the members of a Slack conversation."""

    async def __call__(
        self,
        channel_id: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Any:
        params: dict[str, Any] = {"channel": channel_id}
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit

        response = await self.provider.request(
            "GET",
            "/conversations.members",
            params=params,
        )
        return self.provider.process_httpx_response(response)
