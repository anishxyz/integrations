"""Action for updating document-level properties."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_docs_base_action import GoogleDocsBaseAction


class UpdateDocumentProperties(GoogleDocsBaseAction):
    """Update document style properties such as margins and background."""

    async def __call__(
        self,
        document_id: str,
        document_style: Mapping[str, Any],
        *,
        fields: Sequence[str] | str | None = None,
        write_control: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        if not document_style:
            raise ValueError("document_style must include at least one property")

        if fields is None:
            field_names = sorted(document_style.keys())
            fields_value = ",".join(field_names)
        elif isinstance(fields, str):
            fields_value = fields
        else:
            fields_value = ",".join(fields)

        request = {
            "updateDocumentStyle": {
                "documentStyle": dict(document_style),
                "fields": fields_value,
            }
        }
        return await self.batch_update(
            document_id,
            [request],
            write_control=dict(write_control) if write_control is not None else None,
        )
