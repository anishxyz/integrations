"""Action for finding Asana users."""

from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class FindUser(BaseAction):
    """Find an Asana user by GID or email."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        *,
        user_gid: str | None = None,
        email: str | None = None,
        workspace_gid: str | None = None,
        opt_fields: Iterable[str] | None = None,
    ) -> Any:
        if user_gid is None and email is None:
            raise ValueError("Provide user_gid or email to find a user")

        params = {}
        if opt_fields is not None:
            params["opt_fields"] = ",".join(opt_fields)

        if user_gid is not None:
            response = await self.provider.request(
                "GET",
                f"/users/{user_gid}",
                params=params or None,
            )
            return self.provider.process_httpx_response(response)

        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to find a user by email")

        params.update({"workspace": workspace, "email": email})

        response = await self.provider.request(
            "GET",
            "/users",
            params=params,
        )
        results = self.provider.process_httpx_response(response)
        if isinstance(results, list) and results:
            return results[0]

        raise LookupError(f"User with email '{email}' was not found")
