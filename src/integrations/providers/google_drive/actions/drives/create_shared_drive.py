"""Action for creating a shared drive in Google Drive."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping

from ..google_drive_base_action import GoogleDriveBaseAction


class CreateSharedDrive(GoogleDriveBaseAction):
    """Create a new shared drive (Team Drive)."""

    async def __call__(
        self,
        name: str,
        *,
        request_id: str,
        theme_id: str | None = None,
        color_rgb: str | None = None,
        restrictions: Mapping[str, Any] | None = None,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        body: MutableMapping[str, Any] = {"name": name}
        if theme_id is not None:
            body["themeId"] = theme_id
        if color_rgb is not None:
            body["colorRgb"] = color_rgb
        if restrictions is not None:
            body["restrictions"] = dict(restrictions)

        params: MutableMapping[str, Any] = {"requestId": request_id}
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "POST",
            "/drives",
            params=params,
            json=body,
        )
        return self.provider.process_httpx_response(response)
