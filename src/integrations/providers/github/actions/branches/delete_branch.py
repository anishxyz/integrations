"""Action for deleting branches on Github."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class DeleteBranch(BaseAction):
    """Delete a branch from a repository."""

    provider: "GithubProvider"

    async def __call__(self, owner: str, repository: str, branch: str) -> Any:
        response = await self.provider.request(
            "DELETE",
            f"/repos/{owner}/{repository}/git/refs/heads/{branch}",
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return True
