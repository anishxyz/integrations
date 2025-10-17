"""Create a HubSpot COS blog post."""

from __future__ import annotations

from typing import Any, Mapping, TYPE_CHECKING

from ..hubspot_base_action import HubspotBaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...hubspot_provider import HubspotProvider


class CreateCosBlogPost(HubspotBaseAction):
    """Create a CMS blog post via HubSpot's COS API."""

    provider: "HubspotProvider"

    async def __call__(self, payload: Mapping[str, Any]) -> Any:
        response = await self.provider.request(
            "POST",
            "/cms/v3/blogs/posts",
            json=dict(payload),
        )
        return self.provider.process_httpx_response(response)
