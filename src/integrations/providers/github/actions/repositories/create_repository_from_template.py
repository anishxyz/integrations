"""Create repository from template action for Github."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CreateRepositoryFromTemplate(BaseAction):
    """Generate a repository from an existing Github template."""

    provider: "GithubProvider"

    async def __call__(
        self,
        template_owner: str,
        template_repository: str,
        name: str,
        *,
        owner: str | None = None,
        description: str | None = None,
        private: bool | None = None,
        include_all_branches: bool | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {"name": name}

        if owner is not None:
            payload["owner"] = owner
        if description is not None:
            payload["description"] = description
        if private is not None:
            payload["private"] = private
        if include_all_branches is not None:
            payload["include_all_branches"] = include_all_branches

        url = f"/repos/{template_owner}/{template_repository}/generate"
        response = await self.provider.request("POST", url, json=payload)
        return self.provider.process_httpx_response(response)
