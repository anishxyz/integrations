"""Action for inviting users to Slack channels."""

from __future__ import annotations

from typing import Any, Iterable

from integrations.core import BaseAction


class InviteUserToChannel(BaseAction):
    """Invite one or more users to a Slack channel."""

    async def __call__(
        self,
        channel_id: str,
        user_ids: Iterable[str],
    ) -> Any:
        users = ",".join(user_ids)
        response = await self.provider.request(
            "POST",
            "/conversations.invite",
            json={"channel": channel_id, "users": users},
        )
        return self.provider.process_httpx_response(response)
