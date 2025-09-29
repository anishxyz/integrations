"""Action for creating Github issues."""

from __future__ import annotations

from typing import Any, Dict, Iterable

from .....core import BaseAction


class CreateIssue(BaseAction):
    """Create an issue within a repository."""

    async def __call__(
        self,
        owner: str,
        repository: str,
        title: str,
        *,
        body: str | None = None,
        assignees: Iterable[str] | None = None,
        labels: Iterable[str] | None = None,
        milestone: int | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {"title": title}

        if body is not None:
            payload["body"] = body
        if assignees is not None:
            payload["assignees"] = list(assignees)
        if labels is not None:
            payload["labels"] = list(labels)
        if milestone is not None:
            payload["milestone"] = milestone

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/issues",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
