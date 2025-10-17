"""Get public URL for a HubSpot file."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ..hubspot_base_action import HubspotBaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...hubspot_provider import HubspotProvider


class GetFilePublicUrl(HubspotBaseAction):
    """Retrieve a file's public URL."""

    provider: "HubspotProvider"

    async def __call__(self, file_id: str) -> Any:
        response = await self.provider.request(
            "POST",
            f"/files/v3/files/{file_id}/public-url",
        )
        return self.provider.process_httpx_response(response)
