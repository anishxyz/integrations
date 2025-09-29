"""Action for fetching Github issues."""

from __future__ import annotations

from typing import Any

from .....core import BaseAction


class FindIssue(BaseAction):
    """Find an issue by number."""

    async def __call__(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> Any | None:
        response = await self.provider.request(
            "GET",
            f"/repos/{owner}/{repository}/issues/{issue_number}",
        )
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
