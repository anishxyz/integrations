"""Action for locating sections within Asana projects."""

from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class FindSectionInProject(BaseAction):
    """Find a section within a project by GID or name."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        project_gid: str,
        *,
        section_gid: str | None = None,
        section_name: str | None = None,
        opt_fields: Iterable[str] | None = None,
    ) -> Any:
        if section_gid is None and section_name is None:
            raise ValueError("Provide section_gid or section_name to find a section")

        params = {}
        if opt_fields is not None:
            params["opt_fields"] = ",".join(opt_fields)

        if section_gid is not None:
            response = await self.provider.request(
                "GET",
                f"/sections/{section_gid}",
                params=params or None,
            )
            return self.provider.process_httpx_response(response)

        response = await self.provider.request(
            "GET",
            f"/projects/{project_gid}/sections",
            params=params or None,
        )
        sections = self.provider.process_httpx_response(response)

        target = section_name.casefold() if section_name is not None else None
        for section in sections or []:
            name = str(section.get("name", "")).casefold()
            if name == target:
                return section

        raise LookupError(
            f"Section named '{section_name}' was not found in project {project_gid}"
        )
