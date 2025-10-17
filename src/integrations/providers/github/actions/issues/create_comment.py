"""Action for creating comments on Github issues or pull requests."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CreateComment(BaseAction):
    """Create a comment on an issue or pull request."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repository: str,
        issue_number: int,
        body: str,
    ) -> Any:
        payload: Dict[str, Any] = {"body": body}

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/issues/{issue_number}/comments",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
