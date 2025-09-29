"""Archive an existing database item."""

from __future__ import annotations

from integrations.core import BaseAction


class ArchiveDatabaseItem(BaseAction):
    """Archive a database item (page) in Notion."""

    async def __call__(self, page_id: str) -> dict[str, object]:
        payload = {"archived": True}
        response = await self.provider.request(
            "PATCH",
            f"pages/{page_id}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
