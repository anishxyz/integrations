"""Action for creating a Google Drive file from plain text."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class CreateFileFromText(GoogleDriveBaseAction):
    """Create a file in Google Drive using a text payload."""

    async def __call__(
        self,
        name: str,
        content: str,
        *,
        mime_type: str = "text/plain",
        parents: Sequence[str] | None = None,
        description: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        metadata: MutableMapping[str, Any] = {"name": name, "mimeType": mime_type}
        if parents is not None:
            metadata["parents"] = list(parents)
        if description is not None:
            metadata["description"] = description

        content_bytes = content.encode("utf-8")
        return await self.create_file(
            metadata,
            fields=fields,
            supports_all_drives=supports_all_drives,
            upload_content=content_bytes,
            upload_mime_type=mime_type,
        )
