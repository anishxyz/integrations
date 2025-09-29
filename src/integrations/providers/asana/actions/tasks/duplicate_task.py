"""Action for duplicating Asana tasks."""

from __future__ import annotations

from typing import Any, Iterable

from integrations.core import BaseAction


class DuplicateTask(BaseAction):
    """Duplicate an Asana task."""

    async def __call__(
        self,
        task_gid: str,
        *,
        name: str | None = None,
        include: Iterable[str] | None = None,
        **extra_fields: Any,
    ) -> Any:
        data: dict[str, Any] = {}

        if name is not None:
            data["name"] = name
        if include is not None:
            data["include"] = list(include)
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            f"/tasks/{task_gid}/duplicate",
            json={"data": data} if data else None,
        )
        return self.provider.process_httpx_response(response)
