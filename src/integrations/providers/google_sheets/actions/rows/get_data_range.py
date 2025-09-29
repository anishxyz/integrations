"""Action for retrieving data from a specific range."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class GetDataRange(GoogleSheetsBaseAction):
    """Fetch data from a range using A1 notation."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        major_dimension: str | None = None,
        value_render_option: str | None = None,
        date_time_render_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        return await self.values_get(
            spreadsheet_id,
            range_name,
            major_dimension=major_dimension,
            value_render_option=value_render_option,
            date_time_render_option=date_time_render_option,
        )
