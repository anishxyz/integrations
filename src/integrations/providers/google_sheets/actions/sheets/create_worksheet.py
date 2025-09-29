"""Action for creating a worksheet."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateWorksheet(GoogleSheetsBaseAction):
    """Create a new worksheet within a spreadsheet."""

    async def __call__(
        self,
        spreadsheet_id: str,
        *,
        title: str,
        sheet_properties: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        properties = dict(sheet_properties or {})
        properties["title"] = title

        response = await self.batch_update(
            spreadsheet_id,
            [{"addSheet": {"properties": properties}}],
        )
        replies = response.get("replies", [])
        if replies:
            added = replies[0].get("addSheet", {})
            props = added.get("properties")
            if props is not None:
                return props
        return response
