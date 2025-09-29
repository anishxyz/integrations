"""Action for setting data validation rules."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class SetDataValidation(GoogleSheetsBaseAction):
    """Set data validation rules on a range."""

    async def __call__(
        self,
        spreadsheet_id: str,
        range_: Mapping[str, Any],
        rule: Mapping[str, Any] | None,
    ) -> MutableMapping[str, Any]:
        request = {
            "setDataValidation": {
                "range": dict(range_),
                "rule": dict(rule) if rule is not None else None,
            }
        }
        return await self.batch_update(spreadsheet_id, [request])
