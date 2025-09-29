"""Action for retrieving a spreadsheet by its identifier."""

from __future__ import annotations

from typing import Any, Mapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class GetSpreadsheetById(GoogleSheetsBaseAction):
    """Return the raw spreadsheet payload for the provided ID."""

    async def __call__(
        self,
        spreadsheet_id: str,
        *,
        include_grid_data: bool | None = None,
        ranges: list[str] | None = None,
    ) -> Mapping[str, Any]:
        return await self.get_spreadsheet(
            spreadsheet_id,
            include_grid_data=include_grid_data,
            ranges=ranges,
        )
