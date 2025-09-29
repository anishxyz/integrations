"""Action for moving a Gmail message to the trash."""

from __future__ import annotations

from typing import Any

from ..gmail_base_action import GmailBaseAction


class TrashEmail(GmailBaseAction):
    """Move a Gmail message to the trash."""

    async def __call__(
        self,
        message_id: str,
        *,
        user_id: str | None = None,
    ) -> Any:
        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/messages/{message_id}/trash",
        )
        return self.provider.process_httpx_response(response)
