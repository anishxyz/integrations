"""List repositories action for Github."""

from __future__ import annotations

from typing import Any, Dict

from .....core import BaseAction


class ListRepositories(BaseAction):
    """List repositories accessible to the authenticated user."""

    async def __call__(
        self,
        *,
        visibility: str | None = None,
        affiliation: str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if visibility:
            params["visibility"] = visibility
        if affiliation:
            params["affiliation"] = affiliation
        if per_page is not None:
            params["per_page"] = per_page
        if page is not None:
            params["page"] = page

        response = await self.provider.request(
            "GET",
            "/user/repos",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
