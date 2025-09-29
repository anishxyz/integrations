"""Append content blocks to a Notion page."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from integrations.core import BaseAction


class AddContentToPage(BaseAction):
    """Append blocks to a page or block."""

    async def __call__(
        self,
        block_id: str,
        children: Sequence[Mapping[str, Any]],
        *,
        after: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"children": list(children)}
        if after is not None:
            payload["after"] = after
        response = await self.provider.request(
            "PATCH",
            f"blocks/{block_id}/children",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
