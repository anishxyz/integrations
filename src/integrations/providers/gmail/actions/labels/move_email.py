"""Action for moving an email by adjusting Gmail labels."""

from __future__ import annotations

from typing import Any, Iterable

from ..gmail_base_action import GmailBaseAction


class MoveEmail(GmailBaseAction):
    """Move an email to the provided set of labels."""

    async def __call__(
        self,
        message_id: str,
        *,
        add_label_ids: Iterable[str] | None = None,
        remove_label_ids: Iterable[str] | None = None,
        user_id: str | None = None,
    ) -> Any:
        payload: dict[str, Any] = {}
        if add_label_ids is not None:
            payload["addLabelIds"] = list(add_label_ids)
        if remove_label_ids is not None:
            payload["removeLabelIds"] = list(remove_label_ids)

        resolved_user = self.resolve_user_id(user_id)

        response = await self.provider.request(
            "POST",
            f"/users/{resolved_user}/messages/{message_id}/modify",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
