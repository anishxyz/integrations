"""Google Sheets provider implementation."""

from __future__ import annotations

from typing import Any, Callable, Dict, Mapping, MutableMapping

import httpx

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    ChangeSheetProperties,
    ClearSpreadsheetRows,
    CopyRange,
    CopyWorksheet,
    CreateConditionalFormattingRule,
    CreateMultipleSpreadsheetRows,
    CreateSpreadsheet,
    CreateSpreadsheetColumn,
    CreateSpreadsheetRow,
    CreateSpreadsheetRowAtTop,
    CreateWorksheet,
    DeleteSheet,
    DeleteSpreadsheetRows,
    FindOrCreateRow,
    FindOrCreateWorksheet,
    FindWorksheet,
    FormatCellRange,
    FormatSpreadsheetRow,
    GetDataRange,
    GetManySpreadsheetRows,
    GetRowById,
    GetSpreadsheetById,
    LookupSpreadsheetRow,
    LookupSpreadsheetRows,
    RenameSheet,
    SetDataValidation,
    SortRange,
    UpdateSpreadsheetRow,
    UpdateSpreadsheetRows,
)
from .google_sheets_settings import GoogleSheetsSettings


class GoogleSheetsProvider(HttpxClientMixin, BaseProvider[GoogleSheetsSettings]):
    """Provider exposing common Google Sheets operations."""

    settings_class = GoogleSheetsSettings

    create_spreadsheet: CreateSpreadsheet
    create_spreadsheet_column: CreateSpreadsheetColumn
    create_multiple_spreadsheet_rows: CreateMultipleSpreadsheetRows
    create_spreadsheet_row: CreateSpreadsheetRow
    create_spreadsheet_row_at_top: CreateSpreadsheetRowAtTop
    change_sheet_properties: ChangeSheetProperties
    copy_range: CopyRange
    copy_worksheet: CopyWorksheet
    clear_spreadsheet_rows: ClearSpreadsheetRows
    delete_spreadsheet_rows: DeleteSpreadsheetRows
    delete_sheet: DeleteSheet
    format_spreadsheet_row: FormatSpreadsheetRow
    set_data_validation: SetDataValidation
    update_spreadsheet_row: UpdateSpreadsheetRow
    update_spreadsheet_rows: UpdateSpreadsheetRows
    raw_request: RawHttpRequestAction
    find_worksheet: FindWorksheet
    get_many_spreadsheet_rows: GetManySpreadsheetRows
    get_spreadsheet_by_id: GetSpreadsheetById
    find_or_create_worksheet: FindOrCreateWorksheet
    create_worksheet: CreateWorksheet
    create_conditional_formatting_rule: CreateConditionalFormattingRule
    format_cell_range: FormatCellRange
    rename_sheet: RenameSheet
    sort_range: SortRange
    lookup_spreadsheet_rows: LookupSpreadsheetRows
    lookup_spreadsheet_row: LookupSpreadsheetRow
    find_or_create_row: FindOrCreateRow
    get_data_range: GetDataRange
    get_row_by_id: GetRowById

    create_spreadsheet = action(
        CreateSpreadsheet,
        description="Create a new spreadsheet with optional initial sheets.",
    )
    create_spreadsheet_column = action(
        CreateSpreadsheetColumn,
        description="Insert one or more columns in a worksheet.",
    )
    create_multiple_spreadsheet_rows = action(
        CreateMultipleSpreadsheetRows,
        description="Append multiple rows to the end of a worksheet.",
    )
    create_spreadsheet_row = action(
        CreateSpreadsheetRow,
        description="Append a single row to a worksheet.",
    )
    create_spreadsheet_row_at_top = action(
        CreateSpreadsheetRowAtTop,
        description="Insert a row near the top of a worksheet and populate it.",
    )
    change_sheet_properties = action(
        ChangeSheetProperties,
        description="Update worksheet properties such as frozen rows or visibility.",
    )
    copy_range = action(
        CopyRange,
        description="Copy data and formatting from one range to another.",
    )
    copy_worksheet = action(
        CopyWorksheet,
        description="Copy a worksheet to another spreadsheet.",
    )
    clear_spreadsheet_rows = action(
        ClearSpreadsheetRows,
        description="Clear row contents without deleting the rows.",
    )
    delete_spreadsheet_rows = action(
        DeleteSpreadsheetRows,
        description="Delete one or more rows from a worksheet.",
    )
    delete_sheet = action(
        DeleteSheet,
        description="Delete a worksheet from the spreadsheet.",
    )
    format_spreadsheet_row = action(
        FormatSpreadsheetRow,
        description="Apply formatting to a spreadsheet row.",
    )
    format_cell_range = action(
        FormatCellRange,
        description="Apply formatting to an arbitrary cell range.",
    )
    set_data_validation = action(
        SetDataValidation,
        description="Set or clear data validation rules on a range.",
    )
    update_spreadsheet_row = action(
        UpdateSpreadsheetRow,
        description="Update the values in a single spreadsheet row.",
    )
    update_spreadsheet_rows = action(
        UpdateSpreadsheetRows,
        description="Update the values in multiple rows at once.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Execute a raw Google Sheets API request.",
    )
    find_worksheet = action(
        FindWorksheet,
        description="Locate a worksheet by its title.",
    )
    get_many_spreadsheet_rows = action(
        GetManySpreadsheetRows,
        description="Retrieve many rows from a worksheet range.",
    )
    get_spreadsheet_by_id = action(
        GetSpreadsheetById,
        description="Fetch the raw spreadsheet metadata and sheets.",
    )
    find_or_create_worksheet = action(
        FindOrCreateWorksheet,
        description="Find a worksheet or create it if missing.",
    )
    create_worksheet = action(
        CreateWorksheet,
        description="Create a new worksheet inside the spreadsheet.",
    )
    create_conditional_formatting_rule = action(
        CreateConditionalFormattingRule,
        description="Add a conditional formatting rule to a worksheet.",
    )
    rename_sheet = action(
        RenameSheet,
        description="Rename a worksheet.",
    )
    sort_range = action(
        SortRange,
        description="Sort a range by the specified columns.",
    )
    lookup_spreadsheet_rows = action(
        LookupSpreadsheetRows,
        description="Find rows matching a lookup value.",
    )
    lookup_spreadsheet_row = action(
        LookupSpreadsheetRow,
        description="Find the first row matching a lookup value.",
    )
    find_or_create_row = action(
        FindOrCreateRow,
        description="Find a row or create it if none exists.",
    )
    get_data_range = action(
        GetDataRange,
        description="Get the values for a specific range.",
    )
    get_row_by_id = action(
        GetRowById,
        description="Retrieve a row by its row number.",
    )

    def httpx_headers(self) -> Dict[str, str]:
        settings = self.settings
        token = settings.token
        if not token:
            raise ValueError("Google Sheets authorization is required")

        scheme = settings.authorization_scheme or "Bearer"
        authorization = f"{scheme} {token}".strip()

        headers: Dict[str, str] = {
            "Authorization": authorization,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        user_agent = self.settings.user_agent
        if user_agent:
            headers["User-Agent"] = user_agent
        return headers

    def process_httpx_response(
        self,
        response: httpx.Response,
        *,
        require_json: bool = True,
        unwrap_data: bool = True,
        empty_value: Any | None = None,
        fallback: Callable[[httpx.Response], Any] | Any | None = None,
    ) -> MutableMapping[str, Any]:
        if fallback is None:

            def fallback(resp: httpx.Response) -> dict[str, str]:
                return {"value": resp.text}

        payload = super().process_httpx_response(
            response,
            require_json=require_json,
            unwrap_data=unwrap_data,
            empty_value={} if empty_value is None else empty_value,
            fallback=fallback,
        )
        if isinstance(payload, Mapping):
            error = payload.get("error")
            if isinstance(error, Mapping):
                message = error.get("message", "Google Sheets API error")
                raise ValueError(message)
            return dict(payload)
        return {"value": payload}
