"""Action for fetching branches on Github."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class FindBranch(BaseAction):
    """Return metadata for a branch when it exists."""

    provider: "GithubProvider"

    async def __call__(self, owner: str, repository: str, branch: str) -> Any | None:
        response = await self.provider.request(
            "GET",
            f"/repos/{owner}/{repository}/branches/{branch}",
        )
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
