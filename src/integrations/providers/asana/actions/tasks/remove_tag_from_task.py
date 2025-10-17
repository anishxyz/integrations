"""Action for removing tags from Asana tasks."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class RemoveTagFromTask(BaseAction):
    """Remove a tag from an Asana task."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        task_gid: str,
        tag_gid: str,
        **extra_fields: Any,
    ) -> Any:
        data = {"tag": tag_gid}
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            f"/tasks/{task_gid}/removeTag",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
