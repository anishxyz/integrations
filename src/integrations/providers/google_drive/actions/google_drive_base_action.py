"""Shared helpers for Google Drive actions."""

from __future__ import annotations

import json
from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, TYPE_CHECKING

import httpx

from integrations.core.actions import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ..google_drive_provider import GoogleDriveProvider


async def _default_download_external(
    provider: "GoogleDriveProvider", url: str
) -> tuple[bytes, str | None]:
    timeout = provider.settings.timeout
    if timeout is None:
        timeout = 10.0
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content, response.headers.get("Content-Type")


class GoogleDriveBaseAction(BaseAction):
    """Base class exposing common Google Drive action helpers."""

    provider: "GoogleDriveProvider"

    async def create_file(
        self,
        metadata: Mapping[str, Any],
        *,
        fields: str | None = None,
        supports_all_drives: bool = True,
        upload_content: bytes | None = None,
        upload_mime_type: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {"supportsAllDrives": supports_all_drives}
        if fields is not None:
            params["fields"] = fields

        metadata_dict = dict(metadata)
        if upload_content is None:
            response = await self.provider.request(
                "POST",
                "/files",
                params=params,
                json=metadata_dict,
            )
        else:
            files_payload = {
                "metadata": (
                    "metadata",
                    json.dumps(metadata_dict, separators=(",", ":")),
                    "application/json; charset=UTF-8",
                ),
                "file": (
                    metadata_dict.get("name", "file"),
                    upload_content,
                    upload_mime_type
                    or metadata_dict.get("mimeType")
                    or "application/octet-stream",
                ),
            }
            upload_params = dict(params)
            upload_params["uploadType"] = "multipart"
            response = await self.provider.request(
                "POST",
                "/files",
                params=upload_params,
                files=files_payload,
                base_url=self.provider.settings.upload_base_url,
            )
        return self.provider.process_httpx_response(response)

    async def update_file_metadata(
        self,
        file_id: str,
        body: Mapping[str, Any],
        *,
        fields: str | None = None,
        add_parents: Sequence[str] | None = None,
        remove_parents: Sequence[str] | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {"supportsAllDrives": supports_all_drives}
        if fields is not None:
            params["fields"] = fields
        if add_parents:
            params["addParents"] = ",".join(add_parents)
        if remove_parents:
            params["removeParents"] = ",".join(remove_parents)

        response = await self.provider.request(
            "PATCH",
            f"/files/{file_id}",
            params=params,
            json=dict(body),
        )
        return self.provider.process_httpx_response(response)

    async def upload_file_content(
        self,
        file_id: str,
        content: bytes,
        *,
        mime_type: str,
        fields: str | None = None,
        supports_all_drives: bool = True,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {
            "supportsAllDrives": supports_all_drives,
            "uploadType": "media",
        }
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "PATCH",
            f"/files/{file_id}",
            params=params,
            data=content,
            headers={"Content-Type": mime_type},
            base_url=self.provider.settings.upload_base_url,
        )
        return self.provider.process_httpx_response(response)

    async def get_file(
        self,
        file_id: str,
        *,
        fields: str | None = None,
        supports_all_drives: bool = True,
        acknowledge_abuse: bool | None = None,
        include_permissions_for_view: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: dict[str, Any] = {"supportsAllDrives": supports_all_drives}
        if fields is not None:
            params["fields"] = fields
        if acknowledge_abuse is not None:
            params["acknowledgeAbuse"] = acknowledge_abuse
        if include_permissions_for_view is not None:
            params["includePermissionsForView"] = include_permissions_for_view

        response = await self.provider.request(
            "GET",
            f"/files/{file_id}",
            params=params,
        )
        return self.provider.process_httpx_response(response)

    async def list_files(self, params: Mapping[str, Any]) -> MutableMapping[str, Any]:
        response = await self.provider.request("GET", "/files", params=params)
        return self.provider.process_httpx_response(response)

    async def delete_drive_file(
        self,
        file_id: str,
        *,
        supports_all_drives: bool = True,
    ) -> None:
        params = {"supportsAllDrives": supports_all_drives}
        response = await self.provider.request(
            "DELETE",
            f"/files/{file_id}",
            params=params,
        )
        response.raise_for_status()

    async def download_external(self, url: str) -> tuple[bytes, str | None]:
        override = getattr(self.provider, "download_external", None)
        if (
            override is not None
            and override is not GoogleDriveBaseAction.download_external
        ):
            return await override(url)

        return await _default_download_external(self.provider, url)
