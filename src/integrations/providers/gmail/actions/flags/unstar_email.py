"""Action for removing the star from a Gmail message."""

from __future__ import annotations

from typing import Any

from ..gmail_base_action import GmailBaseAction


class UnstarEmail(GmailBaseAction):
    """Remove the STARRED label from a Gmail message."""

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
            json={"removeLabelIds": ["STARRED"]},
        )
        return self.provider.process_httpx_response(response)
