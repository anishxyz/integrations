"""Action for copying a Google Drive file."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class CopyFile(GoogleDriveBaseAction):
    """Create a copy of an existing file."""

    async def __call__(
        self,
        file_id: str,
        *,
        name: str | None = None,
        parents: Sequence[str] | None = None,
        description: str | None = None,
        keep_revision_forever: bool | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        body: MutableMapping[str, Any] = {}
        if name is not None:
            body["name"] = name
        if parents is not None:
            body["parents"] = list(parents)
        if description is not None:
            body["description"] = description
        if keep_revision_forever is not None:
            body["keepRevisionForever"] = keep_revision_forever

        params: MutableMapping[str, Any] = {"supportsAllDrives": supports_all_drives}
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "POST",
            f"/files/{file_id}/copy",
            params=params,
            json=body or None,
        )
        return self.provider.process_httpx_response(response)
