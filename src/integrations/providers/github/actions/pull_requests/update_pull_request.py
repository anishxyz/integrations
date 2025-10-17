"""Action for updating Github pull requests."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class UpdatePullRequest(BaseAction):
    """Update fields on a pull request."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repository: str,
        pull_number: int,
        *,
        title: str | None = None,
        body: str | None = None,
        state: str | None = None,
        base: str | None = None,
        maintainer_can_modify: bool | None = None,
        draft: bool | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {}

        if title is not None:
            payload["title"] = title
        if body is not None:
            payload["body"] = body
        if state is not None:
            payload["state"] = state
        if base is not None:
            payload["base"] = base
        if maintainer_can_modify is not None:
            payload["maintainer_can_modify"] = maintainer_can_modify
        if draft is not None:
            payload["draft"] = draft

        response = await self.provider.request(
            "PATCH",
            f"/repos/{owner}/{repository}/pulls/{pull_number}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
