"""Restore an archived database item."""

from __future__ import annotations

from typing import TYPE_CHECKING
from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class RestoreDatabaseItem(BaseAction):
    """Restore a previously archived database item."""

    provider: "NotionProvider"

    async def __call__(self, page_id: str) -> dict[str, object]:
        payload = {"archived": False}
        response = await self.provider.request(
            "PATCH",
            f"pages/{page_id}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
