"""Action for updating Asana tasks."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class UpdateTask(BaseAction):
    """Update an existing Asana task."""

    provider: "AsanaProvider"

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
