"""Action for deleting Slack reminders."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...slack_provider import SlackProvider


class DeleteReminder(BaseAction):
    """Delete a Slack reminder."""

    provider: "SlackProvider"

    async def __call__(self, reminder_id: str) -> Any:
        response = await self.provider.request(
            "POST",
            "/reminders.delete",
            json={"reminder": reminder_id},
        )
        return self.provider.process_httpx_response(response)
