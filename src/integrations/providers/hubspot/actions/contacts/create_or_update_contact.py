"""Create or update a HubSpot contact by identifier."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from ..hubspot_base_action import HubspotBaseAction


class CreateOrUpdateContact(HubspotBaseAction):
    """Create or update a contact using a custom identifier."""

    async def __call__(
        self,
        identifier: str,
        properties: Mapping[str, Any],
        *,
        id_property: str = "email",
        associations: Iterable[Mapping[str, Any]] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> Any:
        payload = self.build_object_payload(properties, associations, options)
        params = {"idProperty": id_property}
        response = await self.provider.request(
            "PATCH",
            self.crm_object_path("contacts", identifier),
            params=params,
            json=payload,
        )
        return self.provider.process_httpx_response(response)
