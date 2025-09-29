"""Action for uploading a file to Google Drive."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class UploadFile(GoogleDriveBaseAction):
    """Upload new file content to Google Drive."""

    async def __call__(
        self,
        name: str,
        *,
        content: bytes | str | None = None,
        source_url: str | None = None,
        mime_type: str | None = None,
        parents: Sequence[str] | None = None,
        description: str | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        if content is None and source_url is None:
            raise ValueError("Provide either content bytes or a source_url to upload")

        resolved_content: bytes
        resolved_mime: str | None = mime_type
        if content is not None:
            if isinstance(content, str):
                resolved_content = content.encode("utf-8")
                resolved_mime = mime_type or "text/plain"
            else:
                resolved_content = content
                resolved_mime = mime_type or "application/octet-stream"
        else:
            assert source_url is not None
            resolved_content, inferred_mime = await self.download_external(source_url)
            if resolved_mime is None:
                resolved_mime = inferred_mime

        metadata: MutableMapping[str, Any] = {"name": name}
        if resolved_mime is not None:
            metadata["mimeType"] = resolved_mime
        if parents is not None:
            metadata["parents"] = list(parents)
        if description is not None:
            metadata["description"] = description

        return await self.create_file(
            metadata,
            fields=fields,
            supports_all_drives=supports_all_drives,
            upload_content=resolved_content,
            upload_mime_type=resolved_mime,
        )
