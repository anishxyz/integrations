"""Action to archive Slack channels."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...slack_provider import SlackProvider


class ArchiveChannel(BaseAction):
    """Archive a Slack conversation."""

    provider: "SlackProvider"

    async def __call__(self, channel_id: str) -> Any:
        response = await self.provider.request(
            "POST",
            "/conversations.archive",
            json={"channel": channel_id},
        )
        return self.provider.process_httpx_response(response)
