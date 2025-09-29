"""Action for starring a Gmail message."""

from __future__ import annotations

from typing import Any

from ..gmail_base_action import GmailBaseAction


class StarEmail(GmailBaseAction):
    """Add the STARRED label to a Gmail message."""

    async def __call__(
        self,
        message_id: str,
        *,
        user_id: str | None = None,
    ) -> Any:
        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/messages/{message_id}/modify",
            json={"addLabelIds": ["STARRED"]},
        )
        return self.provider.process_httpx_response(response)
