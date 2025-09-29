"""Action for exporting Google Workspace documents to alternate formats."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class ExportFile(GoogleDriveBaseAction):
    """Export a file to a different mime type such as PDF or DOCX."""

    async def __call__(
        self,
        file_id: str,
        mime_type: str,
        *,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        params = {
            "mimeType": mime_type,
            "supportsAllDrives": supports_all_drives,
        }
        response = await self.provider.request(
            "GET",
            f"/files/{file_id}/export",
            params=params,
        )
        response.raise_for_status()
        return {
            "file_id": file_id,
            "mime_type": response.headers.get("Content-Type", mime_type),
            "data": response.content,
        }
