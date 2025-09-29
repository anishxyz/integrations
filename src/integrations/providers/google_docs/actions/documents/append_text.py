"""Action for appending text to a Google Doc."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_docs_base_action import GoogleDocsBaseAction


class AppendTextToDocument(GoogleDocsBaseAction):
    """Append text at the end of a Google Doc segment."""

    async def __call__(
        self,
        document_id: str,
        text: str,
        *,
        segment_id: str | None = None,
        append_newline: bool = False,
    ) -> MutableMapping[str, Any]:
        if not text:
            raise ValueError("Text to append must be provided")

        payload_text = text
        if append_newline and not payload_text.endswith("\n"):
            payload_text = f"{payload_text}\n"

        end_location: MutableMapping[str, Any] = {}
        if segment_id is not None:
            end_location["segmentId"] = segment_id

        request = {
            "insertText": {
                "text": payload_text,
                "endOfSegmentLocation": end_location or {},
            }
        }
        return await self.batch_update(document_id, [request])
