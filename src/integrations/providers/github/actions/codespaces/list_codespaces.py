"""List codespaces for the authenticated user."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class ListCodespaces(BaseAction):
    """List codespaces owned by the authenticated user."""

    provider: "GithubProvider"

    async def __call__(
        self,
        *,
        per_page: int | None = None,
        page: int | None = None,
        repository_id: int | None = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if per_page is not None:
            params["per_page"] = per_page
        if page is not None:
            params["page"] = page
        if repository_id is not None:
            params["repository_id"] = repository_id

        response = await self.provider.request(
            "GET",
            "/user/codespaces",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
