"""Action for adding labels to Github issues."""

from __future__ import annotations

from typing import Any, Dict, Iterable

from .....core import BaseAction


class AddLabelsToIssue(BaseAction):
    """Add labels to an issue without removing existing labels."""

    async def __call__(
        self,
        owner: str,
        repository: str,
        issue_number: int,
        labels: Iterable[str],
    ) -> Any:
        payload: Dict[str, Any] = {"labels": list(labels)}

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/issues/{issue_number}/labels",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
