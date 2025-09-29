"""Action for fetching branches on Github."""

from __future__ import annotations

from typing import Any

from .....core import BaseAction


class FindBranch(BaseAction):
    """Return metadata for a branch when it exists."""

    async def __call__(self, owner: str, repository: str, branch: str) -> Any | None:
        response = await self.provider.request(
            "GET",
            f"/repos/{owner}/{repository}/branches/{branch}",
        )
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
