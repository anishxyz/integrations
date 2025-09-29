"""Action for archiving a Gmail message."""

from __future__ import annotations

from typing import Any

from ..gmail_base_action import GmailBaseAction


class ArchiveEmail(GmailBaseAction):
    """Archive a Gmail message by removing the INBOX label."""

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
            json={"removeLabelIds": ["INBOX"]},
        )
        return self.provider.process_httpx_response(response)
