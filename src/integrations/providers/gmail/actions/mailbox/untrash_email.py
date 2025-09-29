"""Action for restoring a Gmail message from the trash."""

from __future__ import annotations

from typing import Any

from ..gmail_base_action import GmailBaseAction


class UntrashEmail(GmailBaseAction):
    """Restore a Gmail message from the trash."""

    async def __call__(
        self,
        message_id: str,
        *,
        user_id: str | None = None,
    ) -> Any:
        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/messages/{message_id}/untrash",
        )
        return self.provider.process_httpx_response(response)
