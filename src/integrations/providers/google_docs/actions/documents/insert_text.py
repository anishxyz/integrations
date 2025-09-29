"""Action for inserting text at a specific position."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_docs_base_action import GoogleDocsBaseAction


class InsertText(GoogleDocsBaseAction):
    """Insert text at an explicit index within a Google Doc."""

    async def __call__(
        self,
        document_id: str,
        text: str,
        *,
        index: int,
        segment_id: str | None = None,
    ) -> MutableMapping[str, Any]:
        if not text:
            raise ValueError("Text to insert must be provided")
        if index < 1:
            raise ValueError("Index must be greater than or equal to 1")

        location: MutableMapping[str, Any] = {"index": index}
        if segment_id is not None:
            location["segmentId"] = segment_id

        request = {
            "insertText": {
                "location": location,
                "text": text,
            }
        }
        return await self.batch_update(document_id, [request])
