"""Action for retrieving Github users."""

from __future__ import annotations

from typing import Any

from .....core import BaseAction


class FindUser(BaseAction):
    """Fetch a user profile by login."""

    async def __call__(self, username: str) -> Any | None:
        response = await self.provider.request("GET", f"/users/{username}")
        if response.status_code == 404:
            return None
        return self.provider.process_httpx_response(response)
