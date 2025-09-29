"""Action for deleting a worksheet."""

from __future__ import annotations

from typing import MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class DeleteSheet(GoogleSheetsBaseAction):
    """Delete a worksheet from a spreadsheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
    ) -> MutableMapping[str, object]:
        request = {"deleteSheet": {"sheetId": sheet_id}}
        return await self.batch_update(spreadsheet_id, [request])
