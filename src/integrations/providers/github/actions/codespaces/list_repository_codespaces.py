"""List codespaces for a repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class ListRepositoryCodespaces(BaseAction):
    """List codespaces for a repository owned by the authenticated user."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repo: str,
        *,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if per_page is not None:
            params["per_page"] = per_page
        if page is not None:
            params["page"] = page

        response = await self.provider.request(
            "GET",
            f"/repos/{owner}/{repo}/codespaces",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
