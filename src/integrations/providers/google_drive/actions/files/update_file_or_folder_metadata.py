"""Action for updating Google Drive file or folder metadata."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class UpdateFileOrFolderMetadata(GoogleDriveBaseAction):
    """Patch file metadata such as name, description, and custom properties."""

    async def __call__(
        self,
        file_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        starred: bool | None = None,
        folder_color_rgb: str | None = None,
        color_rgb: str | None = None,
        properties: Mapping[str, Any] | None = None,
        app_properties: Mapping[str, Any] | None = None,
        viewers_can_copy_content: bool | None = None,
        writers_can_share: bool | None = None,
        keep_forever: bool | None = None,
        fields: str | None = None,
        add_parents: Sequence[str] | None = None,
        remove_parents: Sequence[str] | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        body: MutableMapping[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if starred is not None:
            body["starred"] = starred
        if folder_color_rgb is not None:
            body["folderColorRgb"] = folder_color_rgb
        if color_rgb is not None:
            body["colorRgb"] = color_rgb
        if properties is not None:
            body["properties"] = dict(properties)
        if app_properties is not None:
            body["appProperties"] = dict(app_properties)
        if viewers_can_copy_content is not None:
            body["viewersCanCopyContent"] = viewers_can_copy_content
        if writers_can_share is not None:
            body["writersCanShare"] = writers_can_share
        if keep_forever is not None:
            body["keepForever"] = keep_forever

        return await self.update_file_metadata(
            file_id,
            body,
            fields=fields,
            add_parents=add_parents,
            remove_parents=remove_parents,
            supports_all_drives=supports_all_drives,
        )
