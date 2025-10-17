"""Action for fetching Github pull requests."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class FindPullRequest(BaseAction):
    """Fetch a pull request by number."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repository: str,
        pull_number: int,
    ) -> Any | None:
        response = await self.provider.request(
            "GET",
            f"/repos/{owner}/{repository}/pulls/{pull_number}",
        )
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
