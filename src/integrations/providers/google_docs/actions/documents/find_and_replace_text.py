"""Action for running find and replace across a Google Doc."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_docs_base_action import GoogleDocsBaseAction


class FindAndReplaceText(GoogleDocsBaseAction):
    """Find all matching text and replace it within a document."""

    async def __call__(
        self,
        document_id: str,
        search_text: str,
        replace_text: str,
        *,
        match_case: bool = False,
    ) -> MutableMapping[str, Any]:
        if not search_text:
            raise ValueError("search_text must be provided")

        request = {
            "replaceAllText": {
                "containsText": {
                    "text": search_text,
                    "matchCase": match_case,
                },
                "replaceText": replace_text,
            }
        }
        return await self.batch_update(document_id, [request])
