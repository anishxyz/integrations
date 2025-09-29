"""Remove HubSpot object associations."""

from __future__ import annotations

from typing import Any

from .....core.actions import BaseAction


class RemoveAssociations(BaseAction):
    """Remove associations between two CRM records."""

    async def __call__(
        self,
        from_object_type: str,
        from_object_id: str,
        to_object_type: str,
        to_object_id: str,
        *,
        association_type: str | None = None,
    ) -> Any:
        params = {"associationType": association_type} if association_type else None
        response = await self.provider.request(
            "DELETE",
            f"/crm/v4/objects/{from_object_type}/{from_object_id}/associations/{to_object_type}/{to_object_id}",
            params=params,
        )
        return self.provider.process_httpx_response(response)
