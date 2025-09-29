"""Get HubSpot owner by email."""

from __future__ import annotations

from typing import Any

from .....core.actions import BaseAction


class GetOwnerByEmail(BaseAction):
    """Retrieve an owner by their email address."""

    async def __call__(self, email: str) -> Any:
        response = await self.provider.request(
            "GET",
            "/crm/v3/owners/",
            params={"email": email},
        )
        return self.provider.process_httpx_response(response)
