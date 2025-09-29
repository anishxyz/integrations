"""Action for replacing the contents of a Google Drive file."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class ReplaceFile(GoogleDriveBaseAction):
    """Upload new contents for an existing file."""

    async def __call__(
        self,
        file_id: str,
        content: bytes | str,
        *,
        mime_type: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        if isinstance(content, str):
            content_bytes = content.encode("utf-8")
            resolved_mime_type = mime_type or "text/plain"
        else:
            content_bytes = content
            resolved_mime_type = mime_type or "application/octet-stream"

        return await self.upload_file_content(
            file_id,
            content_bytes,
            mime_type=resolved_mime_type,
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
