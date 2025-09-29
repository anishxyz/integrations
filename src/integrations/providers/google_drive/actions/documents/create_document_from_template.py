"""Action for creating a Google Doc from a template."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class CreateDocumentFromTemplate(GoogleDriveBaseAction):
    """Copy an existing template document into a new Google Doc."""

    async def __call__(
        self,
        template_document_id: str,
        *,
        name: str | None = None,
        parents: Sequence[str] | None = None,
        description: str | None = None,
        keep_revision_forever: bool | None = None,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        copied = await self.provider.copy_file(
            template_document_id,
            name=name,
            parents=parents,
            description=description,
            keep_revision_forever=keep_revision_forever,
            fields=fields,
            supports_all_drives=supports_all_drives,
        )
        return {"document": copied}
