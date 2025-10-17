"""Action for creating Github pull requests."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CreatePullRequest(BaseAction):
    """Create a pull request and optionally merge it immediately."""

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
        merge: bool = False,
        merge_method: str | None = None,
        commit_title: str | None = None,
        commit_message: str | None = None,
    ) -> Dict[str, Any]:
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

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repository}/pulls",
            json=payload,
        )
        pull_request = self.provider.process_httpx_response(response)

        merge_result: Dict[str, Any] | None = None
        if merge:
            merge_payload: Dict[str, Any] = {}
            if commit_title is not None:
                merge_payload["commit_title"] = commit_title
            if commit_message is not None:
                merge_payload["commit_message"] = commit_message
            if merge_method is not None:
                merge_payload["merge_method"] = merge_method

            merge_response = await self.provider.request(
                "PUT",
                f"/repos/{owner}/{repository}/pulls/{pull_request['number']}/merge",
                json=merge_payload or None,
            )
            merge_result = self.provider.process_httpx_response(merge_response)

        result: Dict[str, Any] = {"pull_request": pull_request}
        if merge_result is not None:
            result["merge"] = merge_result
        return result
