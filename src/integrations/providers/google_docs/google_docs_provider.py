"""Google Docs provider implementation."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

import httpx

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AppendTextToDocument,
    CreateDocumentFromText,
    FindAndReplaceText,
    FormatText,
    GetDocumentContent,
    InsertImage,
    InsertText,
    UpdateDocumentProperties,
)
from .google_docs_settings import GoogleDocsSettings


class GoogleDocsProvider(HttpxClientMixin, BaseProvider[GoogleDocsSettings]):
    """Provider exposing Google Docs document operations."""

    settings_class = GoogleDocsSettings

    append_text_to_document: AppendTextToDocument
    insert_text: InsertText
    format_text: FormatText
    update_document_properties: UpdateDocumentProperties
    find_and_replace_text: FindAndReplaceText
    insert_image: InsertImage
    get_document_content: GetDocumentContent
    create_document_from_text: CreateDocumentFromText
    raw_request: RawHttpRequestAction

    append_text_to_document = action(
        AppendTextToDocument,
        description="Append text to the end of a Google Doc.",
    )
    insert_text = action(
        InsertText,
        description="Insert text at a specific index in a Google Doc.",
    )
    format_text = action(
        FormatText,
        description="Apply formatting to a text range in a Google Doc.",
    )
    update_document_properties = action(
        UpdateDocumentProperties,
        description="Update document-level properties such as margins or background.",
    )
    find_and_replace_text = action(
        FindAndReplaceText,
        description="Find and replace text across a Google Doc.",
    )
    insert_image = action(
        InsertImage,
        description="Insert an inline image into a Google Doc.",
    )
    get_document_content = action(
        GetDocumentContent,
        description="Retrieve the full content and metadata of a Google Doc.",
    )
    create_document_from_text = action(
        CreateDocumentFromText,
        description="Create a new Google Doc populated with text.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Execute a raw Google Docs API request (beta).",
    )

    def httpx_headers(self) -> MutableMapping[str, str]:
        settings = self.settings
        token = settings.token
        if not token:
            raise ValueError("Google Docs authorization token is required")

        scheme = settings.authorization_scheme or "Bearer"
        headers: MutableMapping[str, str] = {
            "Authorization": f"{scheme} {token}".strip(),
            "Accept": "application/json",
        }
        if self.settings.user_agent:
            headers["User-Agent"] = self.settings.user_agent
        headers.setdefault("Content-Type", "application/json")
        return headers

    def process_httpx_response(
        self, response: httpx.Response
    ) -> MutableMapping[str, Any]:
        def fallback(resp: httpx.Response) -> dict[str, str]:
            return {"value": resp.text}

        payload = self.parse_httpx_response(
            response,
            require_json=True,
            empty_value={},
            fallback=fallback,
        )
        if isinstance(payload, Mapping):
            return dict(payload)
        return {"value": payload}
