"""Action for retrieving many rows from a worksheet."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class GetManySpreadsheetRows(GoogleSheetsBaseAction):
    """Return up to 1,500 rows from the specified range."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        limit: int | None = None,
        major_dimension: str | None = None,
        value_render_option: str | None = None,
        date_time_render_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        payload = await self.values_get(
            spreadsheet_id,
            range_name,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
        )
        if limit is not None:
            values = payload.get("values")
            if isinstance(values, list):
                payload = dict(payload)
                payload["values"] = values[:limit]
        return payload
