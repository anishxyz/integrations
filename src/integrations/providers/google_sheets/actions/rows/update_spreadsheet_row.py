"""Action for updating a single spreadsheet row."""

from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class UpdateSpreadsheetRow(GoogleSheetsBaseAction):
    """Update the contents of a single row."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        row: Sequence[Any],
        *,
        value_input_option: str = "USER_ENTERED",
        include_values_in_response: bool | None = None,
    ) -> MutableMapping[str, Any]:
        return await self.values_update(
            spreadsheet_id,
            range_name,
            [list(row)],
            value_input_option=value_input_option,
            include_values_in_response=include_values_in_response,
        )
