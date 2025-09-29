"""Restore an archived database item."""

from __future__ import annotations

from integrations.core import BaseAction


class RestoreDatabaseItem(BaseAction):
    """Restore a previously archived database item."""

    async def __call__(self, page_id: str) -> dict[str, object]:
        payload = {"archived": False}
        response = await self.provider.request(
            "PATCH",
            f"pages/{page_id}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
