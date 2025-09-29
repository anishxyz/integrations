"""Action for retrieving a Google Doc's content."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_docs_base_action import GoogleDocsBaseAction


class GetDocumentContent(GoogleDocsBaseAction):
    """Fetch the full document content and metadata."""

    async def __call__(
        self,
        document_id: str,
        *,
        fields: str | None = None,
        suggestions_view_mode: str | None = None,
    ) -> MutableMapping[str, Any]:
        return await self.get_document(
            document_id,
            fields=fields,
            suggestions_view_mode=suggestions_view_mode,
        )
