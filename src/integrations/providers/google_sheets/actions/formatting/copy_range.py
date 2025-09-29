"""Action for copying a range of cells."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CopyRange(GoogleSheetsBaseAction):
    """Copy data from one range to another within a spreadsheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        source: Mapping[str, Any],
        destination: Mapping[str, Any],
        *,
        paste_type: str | None = None,
        paste_orientation: str | None = None,
    ) -> MutableMapping[str, Any]:
        request: MutableMapping[str, Any] = {
            "copyPaste": {
                "source": dict(source),
                "destination": dict(destination),
            }
        }
        copy_paste = request["copyPaste"]
        if paste_type is not None:
            copy_paste["pasteType"] = paste_type
        if paste_orientation is not None:
            copy_paste["pasteOrientation"] = paste_orientation

        return await self.batch_update(spreadsheet_id, [request])
