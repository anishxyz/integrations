"""Action for creating a Google Doc from provided text."""

from __future__ import annotations

from typing import MutableMapping

from ..google_docs_base_action import GoogleDocsBaseAction


class CreateDocumentFromText(GoogleDocsBaseAction):
    """Create a document and populate it with text content."""

    async def __call__(
        self,
        text: str,
        *,
        title: str | None = None,
        segment_id: str | None = None,
        append_newline: bool = False,
        fields: str | None = None,
    ) -> MutableMapping[str, object]:
        created = await self.create_document(title=title)
        document_id = created.get("documentId")
        if not isinstance(document_id, str) or not document_id:
            raise ValueError("Document creation response did not include a documentId")

        update_response: MutableMapping[str, object] | None = None
        if text:
            payload_text = text
            if append_newline and not payload_text.endswith("\n"):
                payload_text = f"{payload_text}\n"

            location: MutableMapping[str, object] = {"index": 1}
            if segment_id is not None:
                location["segmentId"] = segment_id

            request = {
                "insertText": {
                    "location": location,
                    "text": payload_text,
                }
            }
            update_response = await self.batch_update(document_id, [request])

        document = (
            await self.get_document(document_id, fields=fields)
            if fields is not None
            else dict(created)
        )

        result: MutableMapping[str, object] = {
            "documentId": document_id,
            "document": document,
        }
        if update_response is not None:
            result["update"] = update_response
        return result
