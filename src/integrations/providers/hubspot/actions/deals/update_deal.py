"""Update a HubSpot deal."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from ..hubspot_base_action import HubspotBaseAction


class UpdateDeal(HubspotBaseAction):
    """Update an existing HubSpot deal."""

    async def __call__(
        self,
        deal_id: str,
        properties: Mapping[str, Any],
        *,
        associations: Iterable[Mapping[str, Any]] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> Any:
        payload = self.build_object_payload(properties, associations, options)
        response = await self.provider.request(
            "PATCH",
            self.crm_object_path("deals", deal_id),
            json=payload,
        )
        return self.provider.process_httpx_response(response)
