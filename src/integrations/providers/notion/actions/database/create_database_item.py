"""Create a new item within a Notion database."""

from __future__ import annotations

from typing import Any, Mapping, Sequence, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class CreateDatabaseItem(BaseAction):
    """Create a page item inside a database."""

    provider: "NotionProvider"

    async def __call__(
        self,
        database_id: str,
        properties: Mapping[str, Any],
        *,
        children: Sequence[Mapping[str, Any]] | None = None,
        icon: Mapping[str, Any] | None = None,
        cover: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "parent": {"database_id": database_id},
            "properties": dict(properties),
        }
        if children is not None:
            payload["children"] = list(children)
        if icon is not None:
            payload["icon"] = dict(icon)
        if cover is not None:
            payload["cover"] = dict(cover)
        response = await self.provider.request("POST", "pages", json=payload)
        return self.provider.process_httpx_response(response)
