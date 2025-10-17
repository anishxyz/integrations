"""Move a page to a new parent."""

from __future__ import annotations

from typing import Any, Mapping, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class MovePage(BaseAction):
    """Move a page under a different parent."""

    provider: "NotionProvider"

    async def __call__(self, page_id: str, parent: Mapping[str, Any]) -> dict[str, Any]:
        payload = {"parent": dict(parent)}
        response = await self.provider.request(
            "PATCH",
            f"pages/{page_id}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
