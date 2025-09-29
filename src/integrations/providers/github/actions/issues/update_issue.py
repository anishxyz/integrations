"""Action for updating Github issues."""

from __future__ import annotations

from typing import Any, Dict, Iterable

from .....core import BaseAction


class UpdateIssue(BaseAction):
    """Update fields on an existing issue."""

    async def __call__(
        self,
        owner: str,
        repository: str,
        issue_number: int,
        *,
        title: str | None = None,
        body: str | None = None,
        state: str | None = None,
        assignees: Iterable[str] | None = None,
        labels: Iterable[str] | None = None,
        milestone: int | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {}

        if title is not None:
            payload["title"] = title
        if body is not None:
            payload["body"] = body
        if state is not None:
            payload["state"] = state
        if assignees is not None:
            payload["assignees"] = list(assignees)
        if labels is not None:
            payload["labels"] = list(labels)
        if milestone is not None:
            payload["milestone"] = milestone

        response = await self.provider.request(
            "PATCH",
            f"/repos/{owner}/{repository}/issues/{issue_number}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
