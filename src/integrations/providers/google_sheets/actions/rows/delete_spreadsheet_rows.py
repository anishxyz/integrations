"""Action for deleting rows from a worksheet."""

from __future__ import annotations

from typing import MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class DeleteSpreadsheetRows(GoogleSheetsBaseAction):
    """Delete one or more rows from a worksheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        *,
        start_index: int,
        end_index: int,
    ) -> MutableMapping[str, object]:
        if end_index <= start_index:
            raise ValueError("end_index must be greater than start_index")

        request = {
            "deleteDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": start_index,
                    "endIndex": end_index,
                }
            }
        }
        return await self.batch_update(spreadsheet_id, [request])
