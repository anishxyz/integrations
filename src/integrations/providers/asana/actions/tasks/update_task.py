"""Action for updating Asana tasks."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class UpdateTask(BaseAction):
    """Update an existing Asana task."""

    async def __call__(
        self,
        task_gid: str,
        *,
        data: dict[str, Any] | None = None,
        **fields: Any,
    ) -> Any:
        payload = dict(data or {})
        if fields:
            payload.update(fields)

        if not payload:
            raise ValueError("Provide at least one field to update")

        response = await self.provider.request(
            "PUT",
            f"/tasks/{task_gid}",
            json={"data": payload},
        )
        return self.provider.process_httpx_response(response)
