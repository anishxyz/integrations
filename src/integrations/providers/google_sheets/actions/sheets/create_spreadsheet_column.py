"""Action for inserting columns into a worksheet."""

from __future__ import annotations

from typing import MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateSpreadsheetColumn(GoogleSheetsBaseAction):
    """Insert one or more columns in a Google Sheets worksheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        *,
        start_index: int,
        end_index: int | None = None,
        inherit_from_before: bool | None = None,
    ) -> MutableMapping[str, object]:
        if end_index is None:
            end_index = start_index + 1

        insert_dimension = {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": start_index,
                "endIndex": end_index,
            }
        }
        if inherit_from_before is not None:
            insert_dimension["inheritFromBefore"] = inherit_from_before

        request = {"insertDimension": insert_dimension}
        return await self.batch_update(spreadsheet_id, [request])
