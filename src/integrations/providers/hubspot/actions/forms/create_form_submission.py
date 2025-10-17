"""Submit a HubSpot form."""

from __future__ import annotations

from typing import Any, Mapping, TYPE_CHECKING

from ..hubspot_base_action import HubspotBaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...hubspot_provider import HubspotProvider


class CreateFormSubmission(HubspotBaseAction):
    """Submit data to a HubSpot form."""

    provider: "HubspotProvider"

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
