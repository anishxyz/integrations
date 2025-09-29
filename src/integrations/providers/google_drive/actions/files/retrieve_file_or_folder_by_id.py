"""Action for retrieving a Google Drive file or folder by ID."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class RetrieveFileOrFolderById(GoogleDriveBaseAction):
    """Get metadata for a file or folder using its Drive ID."""

    async def __call__(
        self,
        file_id: str,
        *,
        fields: str | None = None,
        supports_all_drives: bool = True,
        acknowledge_abuse: bool | None = None,
        include_permissions_for_view: str | None = None,
    ) -> MutableMapping[str, Any]:
        return await self.get_file(
            file_id,
            fields=fields,
            supports_all_drives=supports_all_drives,
            acknowledge_abuse=acknowledge_abuse,
            include_permissions_for_view=include_permissions_for_view,
        )
