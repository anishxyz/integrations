"""Action for finding or creating a row based on lookup criteria."""

from __future__ import annotations

from itertools import zip_longest
from typing import Any, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction
from .create_spreadsheet_row import CreateSpreadsheetRow
from .lookup_spreadsheet_rows import LookupSpreadsheetRows


class FindOrCreateRow(GoogleSheetsBaseAction):
    """Find a row matching the lookup criteria or append a new one."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        lookup_column: str | int,
        lookup_value: Any,
        row: Sequence[Any],
        value_input_option: str = "USER_ENTERED",
        case_sensitive: bool = False,
        use_header_row: bool = True,
        return_as_object: bool | None = None,
    ) -> MutableMapping[str, Any]:
        lookup_action = LookupSpreadsheetRows(self.provider)
        lookup_result = await lookup_action(
            spreadsheet_id,
            range_name,
            lookup_column=lookup_column,
            lookup_value=lookup_value,
            value_render_option=None,
            case_sensitive=case_sensitive,
            use_header_row=use_header_row,
            return_as_objects=return_as_object,
        )
        matches = lookup_result.get("matches", [])
        if matches:
            row_number = None
            numbers = lookup_result.get("matched_row_numbers")
            if isinstance(numbers, list) and numbers:
                row_number = numbers[0]
            return {
                "row": matches[0],
                "created": False,
                "row_number": row_number,
            }

        append_action = CreateSpreadsheetRow(self.provider)
        append_result = await append_action(
            spreadsheet_id,
            range_name,
            row,
            value_input_option=value_input_option,
        )
        header = lookup_result.get("header")
        create_as_object = (
            return_as_object if return_as_object is not None else header is not None
        )
        if create_as_object and header is not None:
            keys = [str(key) if key is not None else "" for key in header]
            converted = {
                key: value for key, value in zip_longest(keys, row, fillvalue=None)
            }
        else:
            converted = list(row)
        return {
            "row": converted,
            "created": True,
            "append_result": append_result,
        }
