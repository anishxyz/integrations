"""Action for finding or creating a Google Doc."""

from __future__ import annotations

from typing import MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction

DOC_MIME_TYPE = "application/vnd.google-apps.document"


class FindOrCreateDocument(GoogleDriveBaseAction):
    """Find a Google Doc by name or create it when missing."""

    async def __call__(
        self,
        name: str,
        *,
        content: bytes | str | None = None,
        description: str | None = None,
        parents: Sequence[str] | None = None,
        drive_id: str | None = None,
        trashed: bool = False,
        fields: str | None = None,
        supports_all_drives: bool = True,
        include_items_from_all_drives: bool = True,
    ) -> MutableMapping[str, object]:
        existing = await self.provider.find_document(
            name,
            parent_id=parents[0] if parents else None,
            drive_id=drive_id,
            trashed=trashed,
            supports_all_drives=supports_all_drives,
            include_items_from_all_drives=include_items_from_all_drives,
            fields=fields,
        )
        if existing is not None:
            return {"created": False, "document": existing}

        metadata: MutableMapping[str, object] = {
            "name": name,
            "mimeType": DOC_MIME_TYPE,
        }
        if description is not None:
            metadata["description"] = description
        if parents is not None:
            metadata["parents"] = list(parents)

        upload_content: bytes | None
        upload_mime_type: str | None
        if content is None:
            upload_content = None
            upload_mime_type = None
        elif isinstance(content, str):
            upload_content = content.encode("utf-8")
            upload_mime_type = "text/plain"
        else:
            upload_content = content
            upload_mime_type = "application/octet-stream"

        created = await self.create_file(
            metadata,
            fields=fields,
            supports_all_drives=supports_all_drives,
            upload_content=upload_content,
            upload_mime_type=upload_mime_type,
        )
        return {"created": True, "document": created}
