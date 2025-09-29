"""Action for appending multiple rows to a worksheet."""

from __future__ import annotations

from typing import Any, Iterable, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateMultipleSpreadsheetRows(GoogleSheetsBaseAction):
    """Append one or more rows to the end of a worksheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        rows: Iterable[Sequence[Any]],
        *,
        value_input_option: str = "USER_ENTERED",
        insert_data_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        row_values = [list(row) for row in rows]
        if not row_values:
            raise ValueError("rows must contain at least one row to append")

        return await self.values_append(
            spreadsheet_id,
            range_name,
            row_values,
            value_input_option=value_input_option,
            insert_data_option=insert_data_option,
        )
