"""Action for retrieving Github organizations."""

from __future__ import annotations

from typing import Any

from .....core import BaseAction


class FindOrganization(BaseAction):
    """Fetch organization metadata by login."""

    async def __call__(self, organization: str) -> Any | None:
        response = await self.provider.request("GET", f"/orgs/{organization}")
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
