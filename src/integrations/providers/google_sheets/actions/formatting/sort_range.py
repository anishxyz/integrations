"""Action for sorting a range."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class SortRange(GoogleSheetsBaseAction):
    """Sort a range of cells by the provided specifications."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_: Mapping[str, Any],
        sort_specs: Sequence[Mapping[str, Any]],
    ) -> MutableMapping[str, Any]:
        request = {
            "sortRange": {
                "range": dict(range_),
                "sortSpecs": [dict(spec) for spec in sort_specs],
            }
        }
        return await self.batch_update(spreadsheet_id, [request])
