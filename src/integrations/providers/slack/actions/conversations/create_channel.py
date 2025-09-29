"""Action for creating Slack channels."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class CreateChannel(BaseAction):
    """Create a Slack channel."""

    async def __call__(
        self,
        name: str,
        *,
        is_private: bool | None = None,
        team_id: str | None = None,
    ) -> Any:
        payload: dict[str, Any] = {"name": name}
        if is_private is not None:
            payload["is_private"] = is_private
        if team_id is not None:
            payload["team_id"] = team_id

        response = await self.provider.request(
            "POST",
            "/conversations.create",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
