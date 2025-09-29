"""Shared helpers for Google Docs actions."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING, Any

from integrations.core.actions import BaseAction

if TYPE_CHECKING:  # pragma: no cover - import cycle guard
    from ..google_docs_provider import GoogleDocsProvider


class GoogleDocsBaseAction(BaseAction):
    """Base class exposing shared Google Docs helpers."""

    provider: "GoogleDocsProvider"

    async def batch_update(
        self,
        document_id: str,
        requests: Sequence[Mapping[str, Any]],
        *,
        write_control: Mapping[str, Any] | None = None,
        fields: str | None = None,
    ) -> MutableMapping[str, Any]:
        payload: MutableMapping[str, Any] = {
            "requests": [dict(request) for request in requests],
        }
        if write_control is not None:
            payload["writeControl"] = dict(write_control)

        params: MutableMapping[str, Any] = {}
        if fields is not None:
            params["fields"] = fields

        response = await self.provider.request(
            "POST",
            f"/documents/{document_id}:batchUpdate",
            json=payload,
            params=params or None,
        )
        return self.provider.process_httpx_response(response)

    async def get_document(
        self,
        document_id: str,
        *,
        fields: str | None = None,
        suggestions_view_mode: str | None = None,
    ) -> MutableMapping[str, Any]:
        params: MutableMapping[str, Any] = {}
        if fields is not None:
            params["fields"] = fields
        if suggestions_view_mode is not None:
            params["suggestionsViewMode"] = suggestions_view_mode

        response = await self.provider.request(
            "GET",
            f"/documents/{document_id}",
            params=params or None,
        )
        return self.provider.process_httpx_response(response)

    async def create_document(
        self,
        *,
        title: str | None = None,
    ) -> MutableMapping[str, Any]:
        payload: MutableMapping[str, Any] = {}
        if title is not None:
            payload["title"] = title

        response = await self.provider.request(
            "POST",
            "/documents",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
