"""Create a HubSpot COS blog post."""

from __future__ import annotations

from typing import Any, Mapping

from .....core.actions import BaseAction


class CreateCosBlogPost(BaseAction):
    """Create a CMS blog post via HubSpot's COS API."""

    async def __call__(self, payload: Mapping[str, Any]) -> Any:
        response = await self.provider.request(
            "POST",
            "/cms/v3/blogs/posts",
            json=dict(payload),
        )
        return self.provider.process_httpx_response(response)
