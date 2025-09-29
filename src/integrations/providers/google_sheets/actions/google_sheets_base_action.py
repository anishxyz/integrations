"""Shared helpers for Google Sheets actions."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING, Any

from integrations.core.actions import BaseAction

from ..utils import encode_a1_range

if TYPE_CHECKING:  # pragma: no cover - avoid circular imports at runtime
    from ..google_sheets_provider import GoogleSheetsProvider


class GoogleSheetsBaseAction(BaseAction):
    """Base class exposing common Google Sheets action helpers."""

    provider: "GoogleSheetsProvider"

    def resolve_spreadsheet_id(self, spreadsheet_id: str | None) -> str:
        if spreadsheet_id:
            return spreadsheet_id
        default_id = self.provider.settings.default_spreadsheet_id
        if not default_id:
            msg = "spreadsheet_id is required when no default is configured"
            raise ValueError(msg)
        return default_id

    async def get_spreadsheet(
        self,
        spreadsheet_id: str,
        *,
        include_grid_data: bool | None = None,
        ranges: Sequence[str] | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {}
        if include_grid_data is not None:
            params["includeGridData"] = include_grid_data
        if ranges is not None:
            params["ranges"] = list(ranges)
        response = await self.provider.request(
            "GET", f"/{spreadsheet_id}", params=params
        )
        return self.provider.process_httpx_response(response)

    async def fetch_worksheet_by_title(
        self,
        spreadsheet_id: str,
        title: str,
        *,
        case_sensitive: bool = False,
        include_grid_data: bool | None = None,
    ) -> MutableMapping[str, Any] | None:
        spreadsheet = await self.get_spreadsheet(
            spreadsheet_id,
            include_grid_data=include_grid_data,
        )
        sheets = spreadsheet.get("sheets", [])
        if not isinstance(sheets, list):
            return None
        target = title if case_sensitive else title.casefold()
        for sheet in sheets:
            if not isinstance(sheet, MutableMapping):
                continue
            properties = sheet.get("properties")
            if not isinstance(properties, Mapping):
                continue
            sheet_title = properties.get("title")
            if sheet_title is None:
                continue
            candidate = sheet_title if case_sensitive else str(sheet_title).casefold()
            if candidate == target:
                return sheet
        return None

    def _values_path(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        suffix: str = "",
    ) -> str:
        encoded_range = encode_a1_range(range_name)
        return f"/{spreadsheet_id}/values/{encoded_range}{suffix}"

    async def batch_update(
        self,
        spreadsheet_id: str,
        requests: Sequence[Mapping[str, Any]],
        *,
        include_spreadsheet_in_response: bool | None = None,
        response_ranges: Sequence[str] | None = None,
        response_include_grid_data: bool | None = None,
    ) -> MutableMapping[str, Any]:
        payload: MutableMapping[str, Any] = {
            "requests": [dict(req) for req in requests]
        }
        if include_spreadsheet_in_response is not None:
            payload["includeSpreadsheetInResponse"] = include_spreadsheet_in_response
        if response_ranges is not None:
            payload["responseRanges"] = list(response_ranges)
        if response_include_grid_data is not None:
            payload["responseIncludeGridData"] = response_include_grid_data

        response = await self.provider.request(
            "POST",
            f"/{spreadsheet_id}:batchUpdate",
            json=payload,
        )
        return self.provider.process_httpx_response(response)

    async def values_append(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: Sequence[Sequence[Any]],
        *,
        value_input_option: str = "USER_ENTERED",
        insert_data_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {"valueInputOption": value_input_option}
        if insert_data_option is not None:
            params["insertDataOption"] = insert_data_option

        response = await self.provider.request(
            "POST",
            self._values_path(spreadsheet_id, range_name, suffix=":append"),
            params=params,
            json={"values": [list(row) for row in values]},
        )
        return self.provider.process_httpx_response(response)

    async def values_update(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: Sequence[Sequence[Any]],
        *,
        value_input_option: str = "USER_ENTERED",
        include_values_in_response: bool | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {"valueInputOption": value_input_option}
        if include_values_in_response is not None:
            params["includeValuesInResponse"] = include_values_in_response

        response = await self.provider.request(
            "PUT",
            self._values_path(spreadsheet_id, range_name),
            params=params,
            json={"values": [list(row) for row in values]},
        )
        return self.provider.process_httpx_response(response)

    async def values_clear(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        partial_match: bool | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {}
        if partial_match is not None:
            params["partialMatch"] = partial_match

        response = await self.provider.request(
            "POST",
            self._values_path(spreadsheet_id, range_name, suffix=":clear"),
            params=params,
            json={},
        )
        return self.provider.process_httpx_response(response)

    async def values_get(
        self,
        spreadsheet_id: str,
        range_name: str,
        *,
        major_dimension: str | None = None,
        value_render_option: str | None = None,
        date_time_render_option: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {}
        if major_dimension is not None:
            params["majorDimension"] = major_dimension
        if value_render_option is not None:
            params["valueRenderOption"] = value_render_option
        if date_time_render_option is not None:
            params["dateTimeRenderOption"] = date_time_render_option

        response = await self.provider.request(
            "GET",
            self._values_path(spreadsheet_id, range_name),
            params=params,
        )
        return self.provider.process_httpx_response(response)
