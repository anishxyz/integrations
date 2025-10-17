"""Retrieve a Notion database."""

from __future__ import annotations

from typing import TYPE_CHECKING
from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class RetrieveDatabase(BaseAction):
    """Fetch metadata for a database."""

    provider: "NotionProvider"

    async def __call__(self, database_id: str) -> dict[str, object]:
        response = await self.provider.request("GET", f"databases/{database_id}")
        return self.provider.process_httpx_response(response)
