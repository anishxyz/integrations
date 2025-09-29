"""Action for updating multiple spreadsheet rows."""

from __future__ import annotations

from typing import Any, Iterable, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class UpdateSpreadsheetRows(GoogleSheetsBaseAction):
    """Update multiple rows within a given range."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        rows: Iterable[Sequence[Any]],
        *,
        value_input_option: str = "USER_ENTERED",
        include_values_in_response: bool | None = None,
    ) -> MutableMapping[str, Any]:
        row_values = [list(row) for row in rows]
        if not row_values:
            raise ValueError("rows must contain at least one row")
        return await self.values_update(
            spreadsheet_id,
            range_name,
            row_values,
            value_input_option=value_input_option,
            include_values_in_response=include_values_in_response,
        )
