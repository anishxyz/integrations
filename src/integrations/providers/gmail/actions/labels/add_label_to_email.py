"""Action for adding labels to a Gmail message."""

from __future__ import annotations

from typing import Any, Iterable

from ..gmail_base_action import GmailBaseAction


class AddLabelToEmail(GmailBaseAction):
    """Add one or more labels to an email message."""

    async def __call__(
        self,
        message_id: str,
        label_ids: Iterable[str],
        *,
        user_id: str | None = None,
    ) -> Any:
        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/messages/{message_id}/modify",
            json={"addLabelIds": list(label_ids)},
        )
        return self.provider.process_httpx_response(response)
