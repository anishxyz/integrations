"""Action for inviting users to Slack channels."""

from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...slack_provider import SlackProvider


class InviteUserToChannel(BaseAction):
    """Invite one or more users to a Slack channel."""

    provider: "SlackProvider"

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
