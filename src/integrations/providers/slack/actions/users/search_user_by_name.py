"""Action for searching Slack users by name."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...slack_provider import SlackProvider


class SearchUserByName(BaseAction):
    """Search for Slack users by their display name."""

    provider: "SlackProvider"

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
