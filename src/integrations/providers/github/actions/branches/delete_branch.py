"""Action for deleting branches on Github."""

from __future__ import annotations

from typing import Any

from .....core import BaseAction


class DeleteBranch(BaseAction):
    """Delete a branch from a repository."""

    async def __call__(self, owner: str, repository: str, branch: str) -> Any:
        response = await self.provider.request(
            "DELETE",
            f"/repos/{owner}/{repository}/git/refs/heads/{branch}",
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return True
