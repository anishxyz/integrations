"""Action for finding or creating Github pull requests."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class FindOrCreatePullRequest(BaseAction):
    """Find an existing pull request by head/base or create one."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repository: str,
        *,
        title: str,
        head: str,
        base: str,
        body: str | None = None,
        draft: bool | None = None,
        maintainer_can_modify: bool | None = None,
        state: str = "open",
    ) -> Any:
        response = await self.provider.request(
            "GET",
            f"/repos/{owner}/{repository}/pulls",
            params={
                "state": state,
                "head": head,
                "base": base,
                "per_page": 1,
            },
        )
        items = self.provider.process_httpx_response(response)

        if items:
            return items[0]

        payload: Dict[str, Any] = {
            "title": title,
            "head": head,
            "base": base,
        }
        if body is not None:
            payload["body"] = body
        if draft is not None:
            payload["draft"] = draft
        if maintainer_can_modify is not None:
            payload["maintainer_can_modify"] = maintainer_can_modify

        create_response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/pulls",
            json=payload,
        )
        return self.provider.process_httpx_response(create_response)
