"""Retrieve a Notion page."""

from __future__ import annotations

from integrations.core import BaseAction


class RetrievePage(BaseAction):
    """Fetch a page by its identifier."""

    async def __call__(self, page_id: str) -> dict[str, object]:
        response = await self.provider.request("GET", f"pages/{page_id}")
        return self.provider.process_httpx_response(response)
