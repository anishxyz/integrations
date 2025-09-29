"""Action for renaming worksheets."""

from __future__ import annotations

from typing import MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class RenameSheet(GoogleSheetsBaseAction):
    """Rename an existing worksheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        new_title: str,
    ) -> MutableMapping[str, object]:
        request = {
            "updateSheetProperties": {
                "properties": {"sheetId": sheet_id, "title": new_title},
                "fields": "title",
            }
        }
        return await self.batch_update(spreadsheet_id, [request])
