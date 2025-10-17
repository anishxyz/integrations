"""Action for creating Asana project sections."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class CreateSection(BaseAction):
    """Create a section in an Asana project."""

    provider: "AsanaProvider"

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
