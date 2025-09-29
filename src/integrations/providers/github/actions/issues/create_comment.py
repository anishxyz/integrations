"""Action for creating comments on Github issues or pull requests."""

from __future__ import annotations

from typing import Any, Dict

from .....core import BaseAction


class CreateComment(BaseAction):
    """Create a comment on an issue or pull request."""

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
