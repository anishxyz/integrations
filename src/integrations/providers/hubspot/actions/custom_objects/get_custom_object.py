"""Retrieve a HubSpot custom object."""

from __future__ import annotations

from typing import Any, Iterable

from ..hubspot_base_action import HubspotBaseAction


class GetCustomObject(HubspotBaseAction):
    """Retrieve a custom object record."""

    async def __call__(
        self,
        object_type: str,
        object_id: str,
        *,
        properties: Iterable[str] | None = None,
        associations: Iterable[str] | None = None,
    ) -> Any:
        params = self.build_properties_params(properties, associations)
        response = await self.provider.request(
            "GET",
            self.crm_object_path(object_type, object_id),
            params=params,
        )
        return self.provider.process_httpx_response(response)
