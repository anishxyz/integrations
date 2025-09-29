"""Action for listing permissions on a Google Drive file."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class GetFilePermissions(GoogleDriveBaseAction):
    """List all permissions applied to a file."""

    async def __call__(
        self,
        file_id: str,
        *,
        page_size: int | None = None,
        page_token: str | None = None,
        use_domain_admin_access: bool | None = None,
        supports_all_drives: bool = True,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {"supportsAllDrives": supports_all_drives}
        if page_size is not None:
            params["pageSize"] = page_size
        if page_token is not None:
            params["pageToken"] = page_token
        if use_domain_admin_access is not None:
            params["useDomainAdminAccess"] = use_domain_admin_access
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "GET",
            f"/files/{file_id}/permissions",
            params=params,
        )
        return self.provider.process_httpx_response(response)
