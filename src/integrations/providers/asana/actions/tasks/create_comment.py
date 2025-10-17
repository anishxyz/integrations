"""Action for creating comments on Asana tasks."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from integrations.core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...asana_provider import AsanaProvider


class CreateComment(BaseAction):
    """Create a comment (story) on an Asana task."""

    provider: "AsanaProvider"

    async def __call__(
        self,
        task_gid: str,
        *,
        text: str | None = None,
        html_text: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        if text is None and html_text is None:
            raise ValueError("Either text or html_text must be provided")

        data: dict[str, Any] = {}
        if text is not None:
            data["text"] = text
        if html_text is not None:
            data["html_text"] = html_text
        if extra_fields:
            data.update(extra_fields)

        response = await self.provider.request(
            "POST",
            f"/tasks/{task_gid}/stories",
            json={"data": data},
        )
        return self.provider.process_httpx_response(response)
