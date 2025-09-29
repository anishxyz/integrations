"""Action for tagging Asana tasks."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class AddTagToTask(BaseAction):
    """Attach a tag to an Asana task."""

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
            f"/tasks/{task_gid}/addTag",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
