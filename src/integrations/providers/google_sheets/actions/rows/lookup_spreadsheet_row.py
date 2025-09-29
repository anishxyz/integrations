"""Action for looking up a single row by column value."""

from __future__ import annotations

from typing import Any, Mapping

from ..google_sheets_base_action import GoogleSheetsBaseAction
from .lookup_spreadsheet_rows import LookupSpreadsheetRows


class LookupSpreadsheetRow(GoogleSheetsBaseAction):
    """Return the first row that matches the lookup criteria."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        lookup_column: str | int,
        lookup_value: Any,
        value_render_option: str | None = None,
        case_sensitive: bool = False,
        use_header_row: bool = True,
        return_as_object: bool | None = None,
    ) -> Mapping[str, Any] | Any | None:
        rows_action = LookupSpreadsheetRows(self.provider)
        result = await rows_action(
            spreadsheet_id,
            range_name,
            lookup_column=lookup_column,
            lookup_value=lookup_value,
            value_render_option=value_render_option,
            case_sensitive=case_sensitive,
            use_header_row=use_header_row,
            return_as_objects=return_as_object,
        )
        matches = result.get("matches", [])
        return matches[0] if matches else None
