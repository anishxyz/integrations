"""Action for formatting arbitrary cell ranges."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class FormatCellRange(GoogleSheetsBaseAction):
    """Apply formatting to a specific range of cells."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_: Mapping[str, Any],
        cell_format: Mapping[str, Any],
        *,
        fields: str = "userEnteredFormat",
    ) -> MutableMapping[str, Any]:
        request = {
            "repeatCell": {
                "range": dict(range_),
                "cell": {"userEnteredFormat": dict(cell_format)},
                "fields": fields,
            }
        }
        return await self.batch_update(spreadsheet_id, [request])
