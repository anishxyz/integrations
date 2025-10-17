"""Get the authenticated Github user."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class GetAuthenticatedUser(BaseAction):
    """Return information about the authenticated Github user."""

    provider: "GithubProvider"

    async def __call__(self) -> Any:
        response = await self.provider.request("GET", "/user")
        return self.provider.process_httpx_response(response)
