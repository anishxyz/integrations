"""Action for finding or creating Asana projects."""

from __future__ import annotations

from typing import Any, Iterable

from integrations.core import BaseAction


class FindOrCreateProject(BaseAction):
    """Find a project by name or create it if it does not exist."""

    async def __call__(
        self,
        name: str,
        *,
        workspace_gid: str | None = None,
        team_gid: str | None = None,
        public: bool | None = None,
        notes: str | None = None,
        color: str | None = None,
        opt_fields: Iterable[str] | None = None,
        **create_fields: Any,
    ) -> Any:
        workspace = workspace_gid or self.provider.settings.workspace_gid
        if workspace is None:
            raise ValueError("workspace_gid is required to find or create a project")

        params: dict[str, Any] = {
            "workspace": workspace,
            "archived": False,
        }
        if team_gid is not None:
            params["team"] = team_gid
        if opt_fields is not None:
            params["opt_fields"] = ",".join(opt_fields)

        search_name = name.casefold()
        next_params = params

        while True:
            response = await self.provider.request(
                "GET",
                "/projects",
                params=next_params,
            )
            payload = self.provider.parse_httpx_response(response, require_json=True)
            data = payload.get("data", []) if isinstance(payload, dict) else payload

            for project in data or []:
                project_name = str(project.get("name", "")).casefold()
                if project_name == search_name:
                    return project

            next_page = payload.get("next_page") if isinstance(payload, dict) else None
            if not next_page or "offset" not in next_page:
                break
            next_params = dict(params)
            next_params["offset"] = next_page["offset"]

        create_data: dict[str, Any] = {
            "name": name,
            "workspace": workspace,
        }
        if team_gid is not None:
            create_data["team"] = team_gid
        if public is not None:
            create_data["public"] = public
        if notes is not None:
            create_data["notes"] = notes
        if color is not None:
            create_data["color"] = color
        if create_fields:
            create_data.update(create_fields)

        response = await self.provider.request(
            "POST",
            "/projects",
            json={"data": create_data},
        )
        return self.provider.process_httpx_response(response)
