"""Action for creating Slack reminders."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class AddReminder(BaseAction):
    """Create a reminder for a Slack user or channel."""

    async def __call__(
        self,
        text: str,
        time: str | int,
        *,
        user_id: str | None = None,
    ) -> Any:
        payload: dict[str, Any] = {
            "text": text,
            "time": time,
        }
        if user_id is not None:
            payload["user"] = user_id

        response = await self.provider.request(
            "POST",
            "/reminders.add",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
