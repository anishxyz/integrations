"""Get a codespace owned by the authenticated user."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class GetCodespace(BaseAction):
    """Fetch details for a specific codespace."""

    provider: "GithubProvider"

    async def __call__(self, codespace_name: str) -> Any:
        response = await self.provider.request(
            "GET",
            f"/user/codespaces/{codespace_name}",
        )
        return self.provider.process_httpx_response(response)
