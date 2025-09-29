"""Action for finding or creating a worksheet."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_sheets_base_action import GoogleSheetsBaseAction


class FindOrCreateWorksheet(GoogleSheetsBaseAction):
    """Find a worksheet by title or create it if it does not exist."""

    async def __call__(
        self,
        spreadsheet_id: str,
        title: str,
        *,
        sheet_properties: Mapping[str, Any] | None = None,
        case_sensitive: bool = False,
    ) -> MutableMapping[str, Any]:
        worksheet = await self.fetch_worksheet_by_title(
            spreadsheet_id,
            title,
            case_sensitive=case_sensitive,
        )
        if worksheet is not None:
            return worksheet

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
