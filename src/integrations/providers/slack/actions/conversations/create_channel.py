"""Action for creating Slack channels."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...slack_provider import SlackProvider


class CreateChannel(BaseAction):
    """Create a Slack channel."""

    provider: "SlackProvider"

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
