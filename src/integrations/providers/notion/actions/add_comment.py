"""Add a comment to a Notion page or block."""

from __future__ import annotations

from typing import Any, Mapping, Sequence, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ..notion_provider import NotionProvider


class AddComment(BaseAction):
    """Create a comment on a page or block."""

    provider: "NotionProvider"

    async def __call__(
        self,
        parent: Mapping[str, Any],
        rich_text: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "parent": dict(parent),
            "rich_text": list(rich_text),
        }
        response = await self.provider.request("POST", "comments", json=payload)
        return self.provider.process_httpx_response(response)
