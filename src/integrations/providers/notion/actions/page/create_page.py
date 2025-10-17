"""Create a standalone Notion page."""

from __future__ import annotations

from typing import Any, Mapping, Sequence, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...notion_provider import NotionProvider


class CreatePage(BaseAction):
    """Create a page outside of database contexts."""

    provider: "NotionProvider"

    async def __call__(
        self,
        parent: Mapping[str, Any],
        *,
        properties: Mapping[str, Any] | None = None,
        children: Sequence[Mapping[str, Any]] | None = None,
        icon: Mapping[str, Any] | None = None,
        cover: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"parent": dict(parent)}
        if properties is not None:
            payload["properties"] = dict(properties)
        if children is not None:
            payload["children"] = list(children)
        if icon is not None:
            payload["icon"] = dict(icon)
        if cover is not None:
            payload["cover"] = dict(cover)
        response = await self.provider.request("POST", "pages", json=payload)
        return self.provider.process_httpx_response(response)
