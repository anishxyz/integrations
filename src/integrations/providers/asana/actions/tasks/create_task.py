"""Action for creating Asana tasks."""

from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class CreateTask(BaseAction):
    """Create a task within an Asana workspace or project."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        name: str,
        *,
        workspace_gid: str | None = None,
        projects: Iterable[str] | None = None,
        assignee: str | None = None,
        due_on: str | None = None,
        notes: str | None = None,
        html_notes: str | None = None,
        custom_fields: dict[str, Any] | None = None,
        followers: Iterable[str] | None = None,
        **extra_fields: Any,
    ) -> Any:
        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to create a task")

        data: dict[str, Any] = {"name": name, "workspace": workspace}

        if projects is not None:
            data["projects"] = list(projects)
        if assignee is not None:
            data["assignee"] = assignee
        if due_on is not None:
            data["due_on"] = due_on
        if notes is not None:
            data["notes"] = notes
        if html_notes is not None:
            data["html_notes"] = html_notes
        if custom_fields is not None:
            data["custom_fields"] = custom_fields
        if followers is not None:
            data["followers"] = list(followers)
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            "/tasks",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
