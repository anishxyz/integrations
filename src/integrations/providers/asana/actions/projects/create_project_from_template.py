"""Action for instantiating projects from templates."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class CreateProjectFromTemplate(BaseAction):
    """Instantiate a project from an Asana template."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        template_gid: str,
        *,
        name: str,
        workspace_gid: str | None = None,
        team_gid: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to use a project template")

        project_payload: dict[str, Any] = {"name": name}
        if extra_fields:
            project_payload.update(extra_fields)

        data: dict[str, Any] = {
            "project": project_payload,
            "workspace": workspace,
        }
        if team_gid is not None:
            data["team"] = team_gid

        response = await self.provider.request(
            "POST",
            f"/project_templates/{template_gid}/instantiateProject",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
