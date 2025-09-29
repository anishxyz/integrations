"""Action for fetching a row by its numeric identifier."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class GetRowById(GoogleSheetsBaseAction):
    """Retrieve a row by its row number (1-indexed)."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_title: str,
        row_number: int,
        *,
        value_render_option: str | None = None,
        date_time_render_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        if row_number <= 0:
            raise ValueError("row_number must be greater than zero")

        range_name = f"{sheet_title}!{row_number}:{row_number}"
        payload = await self.values_get(
            spreadsheet_id,
            range_name,
            major_dimension="ROWS",
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
        )
        values = payload.get("values")
        if isinstance(values, list):
            payload = dict(payload)
            payload["values"] = values[0] if values else []
        return payload
