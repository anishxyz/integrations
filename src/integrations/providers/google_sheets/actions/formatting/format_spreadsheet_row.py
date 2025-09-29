"""Action for formatting rows."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class FormatSpreadsheetRow(GoogleSheetsBaseAction):
    """Apply formatting to an entire row."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        row_index: int,
        *,
        row_count: int = 1,
        cell_format: Mapping[str, Any],
        fields: str = "userEnteredFormat",
    ) -> MutableMapping[str, Any]:
        if row_count <= 0:
            raise ValueError("row_count must be a positive integer")

        request = {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_index,
                    "endRowIndex": row_index + row_count,
                },
                "cell": {"userEnteredFormat": dict(cell_format)},
                "fields": fields,
            }
        }

        return await self.batch_update(spreadsheet_id, [request])
