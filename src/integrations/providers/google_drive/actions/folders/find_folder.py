"""Action for finding a Google Drive folder by name."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction

FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"


class FindFolder(GoogleDriveBaseAction):
    """Locate a folder by name, optionally within a parent."""

    async def __call__(
        self,
        name: str,
        *,
        parent_id: str | None = None,
        drive_id: str | None = None,
        include_items_from_all_drives: bool = True,
        supports_all_drives: bool = True,
        case_sensitive: bool = False,
        fields: str | None = None,
    ) -> MutableMapping[str, Any] | None:
        query_parts = [
            f"name = '{name.replace("'", "\\'")}'",
            f"mimeType = '{FOLDER_MIME_TYPE}'",
        ]
        query_parts.append("trashed = false")
        if parent_id is not None:
            query_parts.append(f"'{parent_id}' in parents")
        query = " and ".join(query_parts)

        params: dict[str, Any] = {
            "q": query,
            "pageSize": 100,
            "supportsAllDrives": supports_all_drives,
            "includeItemsFromAllDrives": include_items_from_all_drives,
        }
        if drive_id is not None:
            params["driveId"] = drive_id
            params["corpora"] = "drive"
        if fields is not None:
            params["fields"] = fields

        data = await self.list_files(params)
        files = data.get("files", []) if isinstance(data, MutableMapping) else []
        if not files:
            return None

        if case_sensitive:
            return files[0]

        target = name.casefold()
        for item in files:
            item_name = str(item.get("name", ""))
            if item_name.casefold() == target:
                return item
        return files[0]
