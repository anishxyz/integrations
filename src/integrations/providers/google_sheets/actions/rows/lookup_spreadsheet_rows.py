"""Action for looking up multiple rows by column value."""

from __future__ import annotations

from itertools import zip_longest
from typing import Any, Iterable, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


def _normalize(value: Any, *, case_sensitive: bool) -> str:
    text = "" if value is None else str(value)
    return text if case_sensitive else text.casefold()


def _coerce_match_row(
    row: Sequence[Any],
    header: Sequence[Any] | None,
    *,
    return_as_objects: bool,
) -> Any:
    if return_as_objects and header is not None:
        keys = [str(item) if item is not None else "" for item in header]
        return {key: cell for key, cell in zip_longest(keys, row, fillvalue=None)}
    return list(row)


class LookupSpreadsheetRows(GoogleSheetsBaseAction):
    """Find rows whose values match the provided lookup criteria."""

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
        return_as_objects: bool | None = None,
    ) -> MutableMapping[str, Any]:
        payload = await self.values_get(
            spreadsheet_id,
            range_name,
            major_dimension="ROWS",
            value_render_option=value_render_option,
        )
        rows = payload.get("values")
        if not isinstance(rows, list) or not rows:
            return {
                "matches": [],
                "header": None,
                "matched_row_numbers": [],
                "range": payload.get("range"),
                "majorDimension": payload.get("majorDimension"),
            }

        header: Sequence[Any] | None = rows[0] if use_header_row else None
        data_rows: Iterable[Sequence[Any]]
        start_index = 0
        if header is not None:
            data_rows = rows[1:]
            start_index = 1
        else:
            data_rows = rows

        if isinstance(lookup_column, int):
            column_index = lookup_column
        else:
            if header is None:
                raise ValueError(
                    "A header row is required when lookup_column is a string name"
                )
            comparison = lookup_column if case_sensitive else lookup_column.casefold()
            column_index = None
            for idx, name in enumerate(header):
                if name is None:
                    continue
                candidate = str(name)
                candidate = candidate if case_sensitive else candidate.casefold()
                if candidate == comparison:
                    column_index = idx
                    break
            if column_index is None:
                raise ValueError(
                    f"Column '{lookup_column}' was not found in the header row"
                )

        normalized_target = _normalize(lookup_value, case_sensitive=case_sensitive)

        if return_as_objects is None:
            return_as_objects = header is not None

        matches: list[Any] = []
        matched_row_numbers: list[int] = []
        for offset, row in enumerate(data_rows):
            if column_index >= len(row):
                continue
            candidate_value = row[column_index]
            if (
                _normalize(candidate_value, case_sensitive=case_sensitive)
                == normalized_target
            ):
                matches.append(
                    _coerce_match_row(
                        row,
                        header,
                        return_as_objects=return_as_objects,
                    )
                )
                matched_row_numbers.append(start_index + offset + 1)

        return {
            "matches": matches,
            "header": list(header) if header is not None else None,
            "matched_row_numbers": matched_row_numbers,
            "range": payload.get("range"),
            "majorDimension": payload.get("majorDimension"),
        }
