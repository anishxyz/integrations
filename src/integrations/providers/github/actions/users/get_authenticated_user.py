"""Get the authenticated Github user."""

from __future__ import annotations

from typing import Any

from .....core import BaseAction


class GetAuthenticatedUser(BaseAction):
    """Return information about the authenticated Github user."""

    async def __call__(self) -> Any:
        response = await self.provider.request("GET", "/user")
        return self.provider.process_httpx_response(response)
