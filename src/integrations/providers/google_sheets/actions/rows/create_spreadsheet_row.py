"""Action for appending a single row."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateSpreadsheetRow(GoogleSheetsBaseAction):
    """Append a single row to the end of a worksheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        row: Sequence[Any],
        *,
        value_input_option: str = "USER_ENTERED",
        insert_data_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        return await self.values_append(
            spreadsheet_id,
            range_name,
            [list(row)],
            value_input_option=value_input_option,
            insert_data_option=insert_data_option,
        )
