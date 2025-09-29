"""Action for moving a Google Drive file to the trash."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class DeleteFile(GoogleDriveBaseAction):
    """Move a file to the trash instead of permanently deleting it."""

    async def __call__(
        self,
        file_id: str,
        *,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        return await self.update_file_metadata(
            file_id,
            {"trashed": True},
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
