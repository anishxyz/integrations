"""Action for finding or creating Github issues."""

from __future__ import annotations

from typing import Any, Iterable

from .....core import BaseAction


class FindOrCreateIssue(BaseAction):
    """Find an existing issue by title or create it."""

    async def __call__(
        self,
        owner: str,
        repository: str,
        title: str,
        *,
        body: str | None = None,
        state: str = "open",
        assignees: Iterable[str] | None = None,
        labels: Iterable[str] | None = None,
        milestone: int | None = None,
    ) -> Any:
        query_parts = [f"repo:{owner}/{repository}", "in:title", f"state:{state}"]
        query_parts.append(f'"{title}"')
        query = " ".join(query_parts)

        response = await self.provider.request(
            "GET",
            "/search/issues",
            params={"q": query, "per_page": 1},
        )
        payload = self.provider.process_httpx_response(response)

        if payload.get("total_count"):
            items = payload.get("items") or []
            if items:
                return items[0]

        return await self.provider.create_issue(
            owner,
            repository,
            title,
            body=body,
            assignees=assignees,
            labels=labels,
            milestone=milestone,
        )
