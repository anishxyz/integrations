"""Action for updating sheet properties."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class ChangeSheetProperties(GoogleSheetsBaseAction):
    """Update properties of a worksheet within a spreadsheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        sheet_id: int,
        properties: Mapping[str, Any],
        *,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        if not properties:
            raise ValueError("properties must include at least one field to update")

        props = dict(properties)
        props.setdefault("sheetId", sheet_id)

        update_request: MutableMapping[str, Any] = {
            "properties": props,
            "fields": fields
            or ",".join(sorted(k for k in props.keys() if k != "sheetId"))
            or "sheetId",
        }

        request = {"updateSheetProperties": update_request}
        return await self.batch_update(spreadsheet_id, [request])
