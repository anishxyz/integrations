"""Action for finding or creating a Google Drive folder."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class FindOrCreateFolder(GoogleDriveBaseAction):
    """Find a folder by name or create it if it does not exist."""

    async def __call__(
        self,
        name: str,
        *,
        parents: Sequence[str] | None = None,
        description: str | None = None,
        folder_color_rgb: str | None = None,
        drive_id: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
        include_items_from_all_drives: bool = True,
        case_sensitive: bool = False,
    ) -> MutableMapping[str, Any]:
        existing = await self.provider.find_folder(
            name,
            parent_id=parents[0] if parents else None,
            drive_id=drive_id,
            supports_all_drives=supports_all_drives,
            include_items_from_all_drives=include_items_from_all_drives,
            case_sensitive=case_sensitive,
            fields=fields,
        )
        if existing is not None:
            return {"created": False, "folder": existing}

        created = await self.provider.create_folder(
            name,
            parents=parents,
            description=description,
            folder_color_rgb=folder_color_rgb,
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
        return {"created": True, "folder": created}
