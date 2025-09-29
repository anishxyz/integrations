"""Action for permanently deleting a Google Drive file."""

from __future__ import annotations

from ..google_drive_base_action import GoogleDriveBaseAction


class DeleteFilePermanently(GoogleDriveBaseAction):
    """Permanently delete a file from Google Drive."""

    async def __call__(
        self,
        file_id: str,
        *,
        supports_all_drives: bool = True,
    ) -> dict[str, bool]:
        await self.delete_drive_file(
            file_id,
            supports_all_drives=supports_all_drives,
        )
        return {"deleted": True}
