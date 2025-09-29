"""Get public URL for a HubSpot file."""

from __future__ import annotations

from typing import Any

from .....core.actions import BaseAction


class GetFilePublicUrl(BaseAction):
    """Retrieve a file's public URL."""

    async def __call__(self, file_id: str) -> Any:
        response = await self.provider.request(
            "POST",
            f"/files/v3/files/{file_id}/public-url",
        )
        return self.provider.process_httpx_response(response)
