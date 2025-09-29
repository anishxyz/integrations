"""Action for uploading files to Asana tasks."""

from __future__ import annotations

from typing import Any

from integrations.core import BaseAction


class AttachFile(BaseAction):
    """Upload an attachment to an Asana task."""

    async def __call__(
        self,
        task_gid: str,
        file_name: str,
        file_content: bytes | bytearray | memoryview,
        *,
        content_type: str | None = None,
        **extra_fields: Any,
    ) -> Any:
        data = {"parent": task_gid}
        if extra_fields:
            data.update(extra_fields)

        files = {
            "file": (
                file_name,
                file_content,
                content_type or "application/octet-stream",
            )
        }

        response = await self.provider.request(
            "POST",
            f"/tasks/{task_gid}/attachments",
            data=data,
            files=files,
        )
        return self.provider.process_httpx_response(response)
