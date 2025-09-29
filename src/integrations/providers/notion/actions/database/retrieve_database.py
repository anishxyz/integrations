"""Retrieve a Notion database."""

from __future__ import annotations

from integrations.core import BaseAction


class RetrieveDatabase(BaseAction):
    """Fetch metadata for a database."""

    async def __call__(self, database_id: str) -> dict[str, object]:
        response = await self.provider.request("GET", f"databases/{database_id}")
        return self.provider.process_httpx_response(response)
