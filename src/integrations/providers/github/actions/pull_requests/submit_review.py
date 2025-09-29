"""Action for submitting Github pull request reviews."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping

from .....core import BaseAction


class SubmitReview(BaseAction):
    """Submit a review for a pull request."""

    async def __call__(
        self,
        owner: str,
        repository: str,
        pull_number: int,
        *,
        body: str | None = None,
        event: str | None = None,
        comments: Iterable[Mapping[str, Any]] | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {}

        if body is not None:
            payload["body"] = body
        if event is not None:
            payload["event"] = event
        if comments is not None:
            payload["comments"] = [dict(comment) for comment in comments]

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/pulls/{pull_number}/reviews",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
