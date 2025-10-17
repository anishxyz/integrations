"""Create a HubSpot engagement."""

from __future__ import annotations

from typing import Any, Mapping, TYPE_CHECKING

from ..hubspot_base_action import HubspotBaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...hubspot_provider import HubspotProvider


class CreateEngagement(HubspotBaseAction):
    """Create an engagement record (notes, tasks, calls, etc.)."""

    provider: "HubspotProvider"

    async def __call__(self, payload: Mapping[str, Any]) -> Any:
        response = await self.provider.request(
            "POST",
            "/engagements/v1/engagements",
            json=dict(payload),
        )
        return self.provider.process_httpx_response(response)
