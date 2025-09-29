"""Action for removing a permission from a Google Drive file."""

from __future__ import annotations

from typing import Any

from ..google_drive_base_action import GoogleDriveBaseAction


class RemoveFilePermission(GoogleDriveBaseAction):
    """Remove a specific permission from a file."""

    async def __call__(
        self,
        file_id: str,
        permission_id: str,
        *,
        supports_all_drives: bool = True,
        use_domain_admin_access: bool | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"supportsAllDrives": supports_all_drives}
        if use_domain_admin_access is not None:
            params["useDomainAdminAccess"] = use_domain_admin_access

        response = await self.provider.request(
            "DELETE",
            f"/files/{file_id}/permissions/{permission_id}",
            params=params,
        )
        response.raise_for_status()
        return {"removed": True}
