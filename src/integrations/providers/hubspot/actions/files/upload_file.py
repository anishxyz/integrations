"""Upload a file to HubSpot."""

from __future__ import annotations

from typing import Any, Mapping

from ..hubspot_base_action import HubspotBaseAction


class UploadFile(HubspotBaseAction):
    """Upload a binary file to HubSpot's file manager."""

    async def __call__(
        self,
        *,
        file_name: str,
        file_bytes: bytes,
        content_type: str | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> Any:
        files = {
            "file": (file_name, file_bytes, content_type or "application/octet-stream"),
        }
        data = {"options": self.encode_json(options) if options else None}
        data = {k: v for k, v in data.items() if v is not None}
        response = await self.provider.request(
            "POST",
            "/files/v3/files",
            files=files,
            data=data or None,
        )
        return self.provider.process_httpx_response(response)
