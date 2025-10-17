"""Action for locating Github repositories."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class FindRepository(BaseAction):
    """Fetch repository metadata, returning ``None`` when absent."""

    provider: "GithubProvider"

    async def __call__(self, owner: str, repository: str) -> Any | None:
        response = await self.provider.request("GET", f"/repos/{owner}/{repository}")
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
