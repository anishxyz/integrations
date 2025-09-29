"""Notion provider implementation."""

from __future__ import annotations

from typing import Any, Dict

import httpx

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddComment,
    AddContentToPage,
    ArchiveDatabaseItem,
    CreateDatabaseItem,
    CreatePage,
    MovePage,
    RestoreDatabaseItem,
    RetrieveDatabase,
    RetrievePage,
    UpdateDatabaseItem,
)
from .notion_settings import NotionSettings


class NotionProvider(HttpxClientMixin, BaseProvider[NotionSettings]):
    """Provider exposing Notion REST API operations."""

    settings_class = NotionSettings

    archive_database_item: ArchiveDatabaseItem
    create_database_item: CreateDatabaseItem
    update_database_item: UpdateDatabaseItem
    create_page: CreatePage
    add_content_to_page: AddContentToPage
    move_page: MovePage
    restore_database_item: RestoreDatabaseItem
    retrieve_page: RetrievePage
    retrieve_database: RetrieveDatabase
    add_comment: AddComment
    raw_request: RawHttpRequestAction

    archive_database_item = action(
        ArchiveDatabaseItem,
        description="Archive a database item (page).",
    )
    create_database_item = action(
        CreateDatabaseItem,
        description="Create a database item within Notion.",
    )
    update_database_item = action(
        UpdateDatabaseItem,
        description="Update properties on a database item.",
    )
    create_page = action(
        CreatePage,
        description="Create a standalone page in Notion.",
    )
    add_content_to_page = action(
        AddContentToPage,
        description="Append content blocks to a page.",
    )
    move_page = action(
        MovePage,
        description="Move a page to a new parent.",
    )
    restore_database_item = action(
        RestoreDatabaseItem,
        description="Restore an archived database item.",
    )
    retrieve_page = action(
        RetrievePage,
        description="Retrieve a page by its identifier.",
    )
    retrieve_database = action(
        RetrieveDatabase,
        description="Retrieve a database by its identifier.",
    )
    add_comment = action(
        AddComment,
        description="Add a comment to a page or block.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Send a raw API request to Notion.",
    )

    def httpx_headers(self) -> Dict[str, str]:
        token = self.settings.token
        if not token:
            raise ValueError("Notion token is required")

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": self.settings.version,
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
        unwrap_data: bool = False,
        empty_value: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """Parse Notion responses, defaulting empty payloads to an empty dict."""

        return super().process_httpx_response(
            response,
            require_json=require_json,
            unwrap_data=unwrap_data,
            empty_value={} if empty_value is None else empty_value,
            **kwargs,
        )
