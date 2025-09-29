"""Action for clearing row contents."""

from __future__ import annotations

from typing import MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class ClearSpreadsheetRows(GoogleSheetsBaseAction):
    """Clear the values of the specified rows while keeping the structure intact."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        partial_match: bool | None = None,
    ) -> MutableMapping[str, object]:
        return await self.values_clear(
            spreadsheet_id,
            range_name,
            partial_match=partial_match,
        )
