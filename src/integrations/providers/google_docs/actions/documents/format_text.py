"""Action for formatting text in a Google Doc."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_docs_base_action import GoogleDocsBaseAction


class FormatText(GoogleDocsBaseAction):
    """Update text styling over a document range."""

    async def __call__(
        self,
        document_id: str,
        text_style: Mapping[str, Any],
        *,
        start_index: int,
        end_index: int,
        segment_id: str | None = None,
        fields: Sequence[str] | str | None = None,
    ) -> MutableMapping[str, Any]:
        if start_index < 1 or end_index < 1:
            raise ValueError("Start and end indexes must be at least 1")
        if end_index <= start_index:
            raise ValueError("end_index must be greater than start_index")
        if not text_style:
            raise ValueError("text_style must include at least one field to update")

        range_payload: MutableMapping[str, Any] = {
            "startIndex": start_index,
            "endIndex": end_index,
        }
        if segment_id is not None:
            range_payload["segmentId"] = segment_id

        if fields is None:
            field_names = sorted(text_style.keys())
            fields_value = ",".join(field_names)
        elif isinstance(fields, str):
            fields_value = fields
        else:
            fields_value = ",".join(fields)

        request = {
            "updateTextStyle": {
                "range": range_payload,
                "textStyle": dict(text_style),
                "fields": fields_value,
            }
        }
        return await self.batch_update(document_id, [request])
