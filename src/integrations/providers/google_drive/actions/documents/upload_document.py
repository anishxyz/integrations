"""Action for uploading and converting a document to Google Docs format."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction

DOC_MIME_TYPE = "application/vnd.google-apps.document"


class UploadDocument(GoogleDriveBaseAction):
    """Upload a document and convert it to a Google Doc."""

    async def __call__(
        self,
        name: str,
        *,
        content: bytes | str | None = None,
        source_url: str | None = None,
        source_mime_type: str | None = None,
        description: str | None = None,
        parents: Sequence[str] | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        if content is None and source_url is None:
            raise ValueError("Provide content bytes/str or a source_url to upload")

        resolved_content: bytes
        resolved_upload_mime: str | None = source_mime_type
        if content is not None:
            if isinstance(content, str):
                resolved_content = content.encode("utf-8")
                resolved_upload_mime = source_mime_type or "text/plain"
            else:
                resolved_content = content
                resolved_upload_mime = source_mime_type or "application/octet-stream"
        else:
            assert source_url is not None
            resolved_content, inferred_mime = await self.download_external(source_url)
            if resolved_upload_mime is None:
                resolved_upload_mime = inferred_mime

        metadata: MutableMapping[str, Any] = {
            "name": name,
            "mimeType": DOC_MIME_TYPE,
        }
        if description is not None:
            metadata["description"] = description
        if parents is not None:
            metadata["parents"] = list(parents)

        return await self.create_file(
            metadata,
            fields=fields,
            supports_all_drives=supports_all_drives,
            upload_content=resolved_content,
            upload_mime_type=resolved_upload_mime,
        )
