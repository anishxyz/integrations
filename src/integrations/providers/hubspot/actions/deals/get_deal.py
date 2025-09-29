"""Retrieve a HubSpot deal."""

from __future__ import annotations

from typing import Any, Iterable

from ..hubspot_base_action import HubspotBaseAction


class GetDeal(HubspotBaseAction):
    """Retrieve a HubSpot deal by ID."""

    async def __call__(
        self,
        deal_id: str,
        *,
        properties: Iterable[str] | None = None,
        associations: Iterable[str] | None = None,
    ) -> Any:
        params = self.build_properties_params(properties, associations)
        response = await self.provider.request(
            "GET",
            self.crm_object_path("deals", deal_id),
            params=params,
        )
        return self.provider.process_httpx_response(response)
