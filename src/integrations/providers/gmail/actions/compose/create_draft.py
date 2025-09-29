"""Action for creating a draft email."""

from __future__ import annotations

from typing import Any, Dict

from ..gmail_base_action import GmailBaseAction


class CreateDraft(GmailBaseAction):
    """Create an email draft for the authenticated Gmail account."""

    async def __call__(
        self,
        raw: str,
        *,
        user_id: str | None = None,
        thread_id: str | None = None,
    ) -> Any:
        message: Dict[str, Any] = {"raw": raw}
        if thread_id is not None:
            message["threadId"] = thread_id

        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/drafts",
            json={"message": message},
        )
        return self.provider.process_httpx_response(response)
