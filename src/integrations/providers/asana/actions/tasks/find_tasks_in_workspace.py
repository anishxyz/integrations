"""Action for listing tasks in an Asana workspace."""

from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class FindTasksInWorkspace(BaseAction):
    """List tasks within a workspace, optionally fetching all pages."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        *,
        workspace_gid: str | None = None,
        assignee: str | None = None,
        project_gid: str | None = None,
        section_gid: str | None = None,
        completed_since: str | None = None,
        limit: int | None = None,
        opt_fields: Iterable[str] | None = None,
        fetch_all: bool = False,
    ) -> Any:
        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to list tasks")

        params: dict[str, Any] = {"workspace": workspace}
        if assignee is not None:
            params["assignee"] = assignee
        if project_gid is not None:
            params["project"] = project_gid
        if section_gid is not None:
            params["section"] = section_gid
        if completed_since is not None:
            params["completed_since"] = completed_since
        if limit is not None:
            params["limit"] = limit
        if opt_fields is not None:
            params["opt_fields"] = ",".join(opt_fields)

        tasks: list[Any] = []
        next_params = params

        while True:
            response = await self.provider.request(
                "GET",
                "/tasks",
                params=next_params,
            )
            payload = self.provider.parse_httpx_response(response, require_json=True)
            data = payload.get("data", []) if isinstance(payload, dict) else payload

            if not fetch_all:
                return data

            tasks.extend(data)
            next_page = payload.get("next_page") if isinstance(payload, dict) else None
            if not next_page or "offset" not in next_page:
                break
            next_params = dict(params)
            next_params["offset"] = next_page["offset"]

        return tasks
