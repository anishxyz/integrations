"""Submit a HubSpot form."""

from __future__ import annotations

from typing import Any, Mapping

from .....core.actions import BaseAction


class CreateFormSubmission(BaseAction):
    """Submit data to a HubSpot form."""

    async def __call__(
        self,
        form_id: str,
        submission: Mapping[str, Any],
        *,
        portal_id: str | None = None,
    ) -> Any:
        payload = dict(submission)
        if portal_id:
            payload.setdefault("portalId", portal_id)
        response = await self.provider.request(
            "POST",
            f"/marketing/v3/forms/{form_id}/submissions",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
