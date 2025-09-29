"""Action for locating a Google Doc by name."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction

DOC_MIME_TYPE = "application/vnd.google-apps.document"


class FindDocument(GoogleDriveBaseAction):
    """Search for a Google Doc by name using Drive."""

    async def __call__(
        self,
        name: str,
        *,
        parent_id: str | None = None,
        drive_id: str | None = None,
        trashed: bool = False,
        case_sensitive: bool = False,
        include_items_from_all_drives: bool = True,
        supports_all_drives: bool = True,
        fields: str | None = None,
        order_by: str | None = None,
    ) -> MutableMapping[str, Any] | None:
        return await self.provider.find_file(
            name,
            mime_type=DOC_MIME_TYPE,
            parent_id=parent_id,
            drive_id=drive_id,
            trashed=trashed,
            case_sensitive=case_sensitive,
            include_items_from_all_drives=include_items_from_all_drives,
            supports_all_drives=supports_all_drives,
            fields=fields,
            order_by=order_by,
        )
