"""Action for sending an email through the Gmail API."""

from __future__ import annotations

from typing import Any, Dict

from ..gmail_base_action import GmailBaseAction


class SendEmail(GmailBaseAction):
    """Send an email using the authenticated Gmail account."""

    async def __call__(
        self,
        raw: str,
        *,
        user_id: str | None = None,
        thread_id: str | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {"raw": raw}
        if thread_id is not None:
            payload["threadId"] = thread_id

        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/messages/send",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
