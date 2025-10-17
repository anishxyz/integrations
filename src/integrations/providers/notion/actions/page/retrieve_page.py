"""Retrieve a Notion page."""

from __future__ import annotations

from typing import TYPE_CHECKING
from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class RetrievePage(BaseAction):
    """Fetch a page by its identifier."""

    provider: "NotionProvider"

    async def __call__(self, page_id: str) -> dict[str, object]:
        response = await self.provider.request("GET", f"pages/{page_id}")
        return self.provider.process_httpx_response(response)
