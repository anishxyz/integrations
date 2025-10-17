"""Stop a codespace owned by the authenticated user."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class StopCodespace(BaseAction):
    """Stop the specified codespace."""

    provider: "GithubProvider"

    async def __call__(self, codespace_name: str) -> Any:
        response = await self.provider.request(
            "POST",
            f"/user/codespaces/{codespace_name}/stop",
        )
        return self.provider.process_httpx_response(response)
