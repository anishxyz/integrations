"""Action for renaming a Google Drive file or folder."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class UpdateFileOrFolderName(GoogleDriveBaseAction):
    """Update the display name of a file or folder."""

    async def __call__(
        self,
        file_id: str,
        name: str,
        *,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        return await self.update_file_metadata(
            file_id,
            {"name": name},
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
