"""Action for checking Github organization membership."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CheckOrganizationMembership(BaseAction):
    """Return membership details when a user belongs to an organization."""

    provider: "GithubProvider"

    async def __call__(self, organization: str, username: str) -> Any | None:
        response = await self.provider.request(
            "GET",
            f"/orgs/{organization}/memberships/{username}",
        )
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
