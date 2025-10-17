"""Update an existing Notion database item."""

from __future__ import annotations

from typing import Any, Mapping, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class UpdateDatabaseItem(BaseAction):
    """Update a database item (page) in Notion."""

    provider: "NotionProvider"

    async def __call__(
        self,
        page_id: str,
        *,
        properties: Mapping[str, Any] | None = None,
        archived: bool | None = None,
        icon: Mapping[str, Any] | None = None,
        cover: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if properties is not None:
            payload["properties"] = dict(properties)
        if archived is not None:
            payload["archived"] = archived
        if icon is not None:
            payload["icon"] = dict(icon)
        if cover is not None:
            payload["cover"] = dict(cover)
        response = await self.provider.request(
            "PATCH",
            f"pages/{page_id}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
