"""Retrieve a HubSpot product."""

from __future__ import annotations

from typing import Any, Iterable

from ..hubspot_base_action import HubspotBaseAction


class GetProduct(HubspotBaseAction):
    """Retrieve a product by ID."""

    async def __call__(
        self,
        product_id: str,
        *,
        properties: Iterable[str] | None = None,
        associations: Iterable[str] | None = None,
    ) -> Any:
        params = self.build_properties_params(properties, associations)
        response = await self.provider.request(
            "GET",
            self.crm_object_path("products", product_id),
            params=params,
        )
        return self.provider.process_httpx_response(response)
