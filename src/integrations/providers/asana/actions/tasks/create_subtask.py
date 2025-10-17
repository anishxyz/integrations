"""Action for creating Asana subtasks."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class CreateSubtask(BaseAction):
    """Create a subtask under an Asana task."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        parent_task_gid: str,
        name: str,
        *,
        assignee: str | None = None,
        due_on: str | None = None,
        notes: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        data: dict[str, Any] = {"name": name}

        if assignee is not None:
            data["assignee"] = assignee
        if due_on is not None:
            data["due_on"] = due_on
        if notes is not None:
            data["notes"] = notes
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            f"/tasks/{parent_task_gid}/subtasks",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
