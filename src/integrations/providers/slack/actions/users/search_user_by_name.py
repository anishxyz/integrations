"""Action for searching Slack users by name."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class SearchUserByName(BaseAction):
    """Search for Slack users by their display name."""

    async def __call__(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> Any:
        params: dict[str, Any] = {"query": query}
        if limit is not None:
            params["limit"] = limit

        response = await self.provider.request(
            "GET",
            "/users.search",
            params=params,
        )
        payload = self.provider.process_httpx_response(response)
        if isinstance(payload, dict):
            return payload.get("members", [])
        return payload
