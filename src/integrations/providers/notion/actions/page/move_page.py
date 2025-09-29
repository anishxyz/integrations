"""Move a page to a new parent."""

from __future__ import annotations

from typing import Any, Mapping

from integrations.core import BaseAction


class MovePage(BaseAction):
    """Move a page under a different parent."""

    async def __call__(self, page_id: str, parent: Mapping[str, Any]) -> dict[str, Any]:
        payload = {"parent": dict(parent)}
        response = await self.provider.request(
            "PATCH",
            f"pages/{page_id}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
