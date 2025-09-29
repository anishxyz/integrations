"""Create a HubSpot engagement."""

from __future__ import annotations

from typing import Any, Mapping

from .....core.actions import BaseAction


class CreateEngagement(BaseAction):
    """Create an engagement record (notes, tasks, calls, etc.)."""

    async def __call__(self, payload: Mapping[str, Any]) -> Any:
        response = await self.provider.request(
            "POST",
            "/engagements/v1/engagements",
            json=dict(payload),
        )
        return self.provider.process_httpx_response(response)
