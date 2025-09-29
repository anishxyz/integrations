"""Get HubSpot owner by ID."""

from __future__ import annotations

from typing import Any

from .....core.actions import BaseAction


class GetOwnerById(BaseAction):
    """Retrieve an owner by ID."""

    async def __call__(self, owner_id: str) -> Any:
        response = await self.provider.request(
            "GET",
            f"/crm/v3/owners/{owner_id}",
        )
        return self.provider.process_httpx_response(response)
