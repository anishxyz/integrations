"""Get HubSpot owner by ID."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ..hubspot_base_action import HubspotBaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...hubspot_provider import HubspotProvider


class GetOwnerById(HubspotBaseAction):
    """Retrieve an owner by ID."""

    provider: "HubspotProvider"

    async def __call__(self, owner_id: str) -> Any:
        response = await self.provider.request(
            "GET",
            f"/crm/v3/owners/{owner_id}",
        )
        return self.provider.process_httpx_response(response)
