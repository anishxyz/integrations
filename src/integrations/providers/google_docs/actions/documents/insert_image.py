"""Action for inserting an inline image into a Google Doc."""

from __future__ import annotations

from typing import Any, MutableMapping

from ..google_docs_base_action import GoogleDocsBaseAction


class InsertImage(GoogleDocsBaseAction):
    """Insert an inline image at the specified document index."""

    async def __call__(
        self,
        document_id: str,
        image_uri: str,
        *,
        index: int,
        segment_id: str | None = None,
        width: float | None = None,
        height: float | None = None,
        size_unit: str = "PT",
    ) -> MutableMapping[str, Any]:
        if not image_uri:
            raise ValueError("image_uri must be provided")
        if index < 1:
            raise ValueError("Index must be greater than or equal to 1")

        location: MutableMapping[str, Any] = {"index": index}
        if segment_id is not None:
            location["segmentId"] = segment_id

        image_request: MutableMapping[str, Any] = {
            "location": location,
            "uri": image_uri,
        }
        size_payload: MutableMapping[str, Any] = {}
        if width is not None:
            size_payload["width"] = {"magnitude": float(width), "unit": size_unit}
        if height is not None:
            size_payload["height"] = {"magnitude": float(height), "unit": size_unit}
        if size_payload:
            image_request["objectSize"] = size_payload

        request = {"insertInlineImage": image_request}
        return await self.batch_update(document_id, [request])
