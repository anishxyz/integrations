"""Action for creating Asana projects."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class CreateProject(BaseAction):
    """Create a project within an Asana workspace."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        name: str,
        *,
        workspace_gid: str | None = None,
        team_gid: str | None = None,
        public: bool | None = None,
        notes: str | None = None,
        color: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to create a project")

        data: dict[str, Any] = {"name": name, "workspace": workspace}

        if team_gid is not None:
            data["team"] = team_gid
        if public is not None:
            data["public"] = public
        if notes is not None:
            data["notes"] = notes
        if color is not None:
            data["color"] = color
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            "/projects",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
