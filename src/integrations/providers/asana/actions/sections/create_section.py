"""Action for creating Asana project sections."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class CreateSection(BaseAction):
    """Create a section in an Asana project."""

    async def __call__(
        self,
        project_gid: str,
        name: str,
        **extra_fields: Any,
    ) -> Any:
        data: dict[str, Any] = {"name": name}
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            f"/projects/{project_gid}/sections",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
