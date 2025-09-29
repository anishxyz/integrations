"""Action for adding conditional formatting rules."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateConditionalFormattingRule(GoogleSheetsBaseAction):
    """Add a conditional formatting rule to a worksheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        rule: Mapping[str, Any],
        *,
        index: int | None = None,
    ) -> MutableMapping[str, Any]:
        request: MutableMapping[str, Any] = {
            "addConditionalFormatRule": {
                "rule": dict(rule),
            }
        }
        if index is not None:
            request["addConditionalFormatRule"]["index"] = index

        return await self.batch_update(spreadsheet_id, [request])
