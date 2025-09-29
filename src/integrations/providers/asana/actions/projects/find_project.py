"""Action for retrieving Asana projects."""

from __future__ import annotations

from typing import Any, Iterable

from integrations.core import BaseAction


class FindProject(BaseAction):
    """Retrieve a project by its GID."""

    async def __call__(
        self,
        project_gid: str,
        *,
        opt_fields: Iterable[str] | None = None,
    ) -> Any:
        params = {}
        if opt_fields is not None:
            params["opt_fields"] = ",".join(opt_fields)

        response = await self.provider.request(
            "GET",
            f"/projects/{project_gid}",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
