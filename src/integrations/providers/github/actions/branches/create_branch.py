"""Action for creating branches on Github."""

from __future__ import annotations

from typing import Any, Dict

from .....core import BaseAction


class CreateBranch(BaseAction):
    """Create a branch pointing to a specific commit SHA."""

    async def __call__(self, owner: str, repository: str, branch: str, sha: str) -> Any:
        payload: Dict[str, Any] = {
            "ref": f"refs/heads/{branch}",
            "sha": sha,
        }

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/git/refs",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
