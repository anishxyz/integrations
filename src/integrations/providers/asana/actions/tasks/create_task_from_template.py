"""Action for instantiating tasks from templates."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class CreateTaskFromTemplate(BaseAction):
    """Instantiate a task from an Asana template."""

    async def __call__(
        self,
        template_gid: str,
        *,
        name: str | None = None,
        workspace_gid: str | None = None,
        project_gid: str | None = None,
        assignee: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to use a task template")

        data: dict[str, Any] = {"workspace": workspace}

        if name is not None:
            data["name"] = name
        if project_gid is not None:
            data["project"] = project_gid
        if assignee is not None:
            data["assignee"] = assignee
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            f"/task_templates/{template_gid}/instantiateTask",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
