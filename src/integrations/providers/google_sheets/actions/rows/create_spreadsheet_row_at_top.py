"""Action for inserting a row near the top of a worksheet."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateSpreadsheetRowAtTop(GoogleSheetsBaseAction):
    """Insert a row after the header and populate it with values."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        range_name: str,
        row: Sequence[Any],
        *,
        start_index: int = 1,
        inherit_from_before: bool | None = None,
        value_input_option: str = "USER_ENTERED",
    ) -> MutableMapping[str, Any]:
        insert_dimension = {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start_index,
                "endIndex": start_index + 1,
            }
        }
        if inherit_from_before is not None:
            insert_dimension["inheritFromBefore"] = inherit_from_before

        await self.batch_update(
            spreadsheet_id,
            [{"insertDimension": insert_dimension}],
        )

        return await self.values_update(
            spreadsheet_id,
            range_name,
            [list(row)],
            value_input_option=value_input_option,
        )
