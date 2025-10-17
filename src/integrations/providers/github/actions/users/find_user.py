"""Action for retrieving Github users."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class FindUser(BaseAction):
    """Fetch a user profile by login."""

    provider: "GithubProvider"

    async def __call__(self, username: str) -> Any | None:
        response = await self.provider.request("GET", f"/users/{username}")
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
