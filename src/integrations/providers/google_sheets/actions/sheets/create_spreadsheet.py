"""Action for creating Google Sheets spreadsheets."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_sheets_base_action import GoogleSheetsBaseAction


class CreateSpreadsheet(GoogleSheetsBaseAction):
    """Create a new Google Sheets spreadsheet."""

    async def __call__(
        self,
        *,
        properties: Mapping[str, Any] | None = None,
        sheets: Sequence[Mapping[str, Any]] | None = None,
        named_ranges: Sequence[Mapping[str, Any]] | None = None,
        developer_metadata: Sequence[Mapping[str, Any]] | None = None,
        **extra_fields: Any,
    ) -> MutableMapping[str, Any]:
        payload: MutableMapping[str, Any] = dict(extra_fields)
        if properties is not None:
            payload["properties"] = dict(properties)
        if sheets is not None:
            payload["sheets"] = [dict(sheet) for sheet in sheets]
        if named_ranges is not None:
            payload["namedRanges"] = [dict(named_range) for named_range in named_ranges]
        if developer_metadata is not None:
            payload["developerMetadata"] = [dict(meta) for meta in developer_metadata]

        response = await self.provider.request("POST", "/", json=payload)
        return self.provider.process_httpx_response(response)
