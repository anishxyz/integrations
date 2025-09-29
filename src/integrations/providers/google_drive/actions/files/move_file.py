"""Action for moving a Google Drive file between folders."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_drive_base_action import GoogleDriveBaseAction


class MoveFile(GoogleDriveBaseAction):
    """Move a file to a different parent folder."""

    async def __call__(
        self,
        file_id: str,
        destination_parent_id: str,
        *,
        remove_previous_parents: bool = True,
        previous_parent_ids: Sequence[str] | None = None,
        supports_all_drives: bool = True,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {
            "supportsAllDrives": supports_all_drives,
            "addParents": destination_parent_id,
        }
        if remove_previous_parents:
            parents = (
                list(previous_parent_ids) if previous_parent_ids is not None else None
            )
            if parents is None:
                metadata = await self.provider.retrieve_file_or_folder_by_id(
                    file_id,
                    supports_all_drives=supports_all_drives,
                    fields="id,parents",
                )
                parents = list(metadata.get("parents", []))
            if parents:
                params["removeParents"] = ",".join(parents)
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "PATCH",
            f"/files/{file_id}",
            params=params,
            json={},
        )
        return self.provider.process_httpx_response(response)
