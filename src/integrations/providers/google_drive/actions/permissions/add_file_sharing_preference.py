"""Action for adding a sharing preference to a Google Drive file."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class AddFileSharingPreference(GoogleDriveBaseAction):
    """Add a sharing permission to a file without removing existing ones."""

    async def __call__(
        self,
        file_id: str,
        *,
        role: str,
        permission_type: str,
        email_address: str | None = None,
        domain: str | None = None,
        allow_file_discovery: bool | None = None,
        send_notification_email: bool | None = None,
        expiration_time: str | None = None,
        view: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
        use_domain_admin_access: bool | None = None,
    ) -> MutableMapping[str, Any]:
        body: MutableMapping[str, Any] = {"role": role, "type": permission_type}
        if email_address is not None:
            body["emailAddress"] = email_address
        if domain is not None:
            body["domain"] = domain
        if allow_file_discovery is not None:
            body["allowFileDiscovery"] = allow_file_discovery
        if expiration_time is not None:
            body["expirationTime"] = expiration_time
        if view is not None:
            body["view"] = view

        params: MutableMapping[str, Any] = {"supportsAllDrives": supports_all_drives}
        if send_notification_email is not None:
            params["sendNotificationEmail"] = send_notification_email
        if fields is not None:
            params["fields"] = fields
        if use_domain_admin_access is not None:
            params["useDomainAdminAccess"] = use_domain_admin_access

        response = await self.provider.request(
            "POST",
            f"/files/{file_id}/permissions",
            params=params,
            json=body,
        )
        return self.provider.process_httpx_response(response)
