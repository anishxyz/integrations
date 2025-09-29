"""Action for retrieving Google Drive files with custom query parameters."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class RetrieveFiles(GoogleDriveBaseAction):
    """Fetch files from Google Drive using the files.list endpoint."""

    async def __call__(
        self,
        *,
        query: str | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
        order_by: str | None = None,
        drive_id: str | None = None,
        corpora: str | None = None,
        spaces: str | None = None,
        include_items_from_all_drives: bool = True,
        supports_all_drives: bool = True,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {
            "supportsAllDrives": supports_all_drives,
            "includeItemsFromAllDrives": include_items_from_all_drives,
        }
        if query is not None:
            params["q"] = query
        if page_size is not None:
            params["pageSize"] = page_size
        if page_token is not None:
            params["pageToken"] = page_token
        if order_by is not None:
            params["orderBy"] = order_by
        if drive_id is not None:
            params["driveId"] = drive_id
            if corpora is None:
                params["corpora"] = "drive"
        if corpora is not None:
            params["corpora"] = corpora
        if spaces is not None:
            params["spaces"] = spaces
        if fields is not None:
            params["fields"] = fields

        return await self.list_files(params)
