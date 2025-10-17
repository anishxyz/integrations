"""Action for retrieving Asana tasks."""

from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class FindTask(BaseAction):
    """Retrieve a task by its Asana GID."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        task_gid: str,
        *,
        opt_fields: Iterable[str] | None = None,
    ) -> Any:
        params = {}
        if opt_fields is not None:
            params["opt_fields"] = ",".join(opt_fields)

        response = await self.provider.request(
            "GET",
            f"/tasks/{task_gid}",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)
