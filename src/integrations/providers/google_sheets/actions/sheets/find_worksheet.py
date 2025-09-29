"""Action for locating a worksheet by title."""

from __future__ import annotations

from typing import Any, Mapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class FindWorksheet(GoogleSheetsBaseAction):
    """Find a worksheet by its title."""

    async def __call__(
        self,
        spreadsheet_id: str,
        title: str,
        *,
        case_sensitive: bool = False,
        include_grid_data: bool | None = None,
    ) -> Mapping[str, Any] | None:
        return await self.fetch_worksheet_by_title(
            spreadsheet_id,
            title,
            case_sensitive=case_sensitive,
            include_grid_data=include_grid_data,
        )
