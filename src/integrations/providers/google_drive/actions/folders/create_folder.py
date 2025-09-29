"""Action for creating a folder in Google Drive."""

from __future__ import annotations

from typing import MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class CreateFolder(GoogleDriveBaseAction):
    """Create an empty folder in Google Drive."""

    async def __call__(
        self,
        name: str,
        *,
        parents: Sequence[str] | None = None,
        description: str | None = None,
        folder_color_rgb: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, object]:
        metadata: MutableMapping[str, object] = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parents is not None:
            metadata["parents"] = list(parents)
        if description is not None:
            metadata["description"] = description
        if folder_color_rgb is not None:
            metadata["folderColorRgb"] = folder_color_rgb

        return await self.create_file(
            metadata,
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
