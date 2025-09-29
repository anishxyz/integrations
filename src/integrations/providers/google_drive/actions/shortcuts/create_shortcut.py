"""Action for creating a shortcut in Google Drive."""

from __future__ import annotations

from typing import MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class CreateShortcut(GoogleDriveBaseAction):
    """Create a shortcut to an existing Google Drive file."""

    async def __call__(
        self,
        name: str,
        target_id: str,
        *,
        target_mime_type: str | None = None,
        parents: Sequence[str] | None = None,
        description: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, object]:
        metadata: MutableMapping[str, object] = {
            "name": name,
            "mimeType": "application/vnd.google-apps.shortcut",
            "shortcutDetails": {"targetId": target_id},
        }
        if target_mime_type is not None:
            metadata["shortcutDetails"]["targetMimeType"] = target_mime_type
        if parents is not None:
            metadata["parents"] = list(parents)
        if description is not None:
            metadata["description"] = description

        return await self.create_file(
            metadata,
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
