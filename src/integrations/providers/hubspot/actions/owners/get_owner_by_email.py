"""Get HubSpot owner by email."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ..hubspot_base_action import HubspotBaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...hubspot_provider import HubspotProvider


class GetOwnerByEmail(HubspotBaseAction):
    """Retrieve an owner by their email address."""

    provider: "HubspotProvider"

    async def __call__(self, email: str) -> Any:
        response = await self.provider.request(
            "GET",
            "/crm/v3/owners/",
            params={"email": email},
        )
        return self.provider.process_httpx_response(response)
