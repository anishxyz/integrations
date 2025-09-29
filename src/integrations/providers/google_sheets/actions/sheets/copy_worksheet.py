"""Action for copying worksheets between spreadsheets."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CopyWorksheet(GoogleSheetsBaseAction):
    """Copy a worksheet to another spreadsheet and optionally rename it."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        *,
        destination_spreadsheet_id: str,
        new_sheet_name: str | None = None,
    ) -> MutableMapping[str, Any]:
        response = await self.provider.request(
            "POST",
            f"/{spreadsheet_id}/sheets/{sheet_id}:copyTo",
            json={"destinationSpreadsheetId": destination_spreadsheet_id},
        )
        copied = self.provider.process_httpx_response(response)

        if new_sheet_name:
            new_sheet_id = copied.get("sheetId")
            if new_sheet_id is not None:
                await self.batch_update(
                    destination_spreadsheet_id,
                    [
                        {
                            "updateSheetProperties": {
                                "properties": {
                                    "sheetId": new_sheet_id,
                                    "title": new_sheet_name,
                                },
                                "fields": "title",
                            }
                        }
                    ],
                )
                copied = dict(copied)
                copied["title"] = new_sheet_name
        return copied
