"""Action for deleting Slack reminders."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class DeleteReminder(BaseAction):
    """Delete a Slack reminder."""

    async def __call__(self, reminder_id: str) -> Any:
        response = await self.provider.request(
            "POST",
            "/reminders.delete",
            json={"reminder": reminder_id},
        )
        return self.provider.process_httpx_response(response)
