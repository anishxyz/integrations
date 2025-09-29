"""Action for locating a Google Drive file by name."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class FindFile(GoogleDriveBaseAction):
    """Search for a file by name and optional filters."""

    async def __call__(
        self,
        name: str,
        *,
        mime_type: str | None = None,
        parent_id: str | None = None,
        drive_id: str | None = None,
        trashed: bool = False,
        case_sensitive: bool = False,
        include_items_from_all_drives: bool = True,
        supports_all_drives: bool = True,
        fields: str | None = None,
        order_by: str | None = None,
    ) -> MutableMapping[str, Any] | None:
        query_parts = [f"name = '{name.replace("'", "\\'")}'"]
        if mime_type is not None:
            query_parts.append(f"mimeType = '{mime_type}'")
        if parent_id is not None:
            query_parts.append(f"'{parent_id}' in parents")
        query_parts.append(f"trashed = {str(trashed).lower()}")
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
        if order_by is not None:
            params["orderBy"] = order_by

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
