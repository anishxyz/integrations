"""Shared helpers for HubSpot actions."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, TYPE_CHECKING

from integrations.core.actions import BaseAction

if TYPE_CHECKING:  # pragma: no cover
    from ..hubspot_provider import HubspotProvider


class HubspotBaseAction(BaseAction):
    """Base class exposing common HubSpot action helpers."""

    provider: "HubspotProvider"

    def build_object_payload(
        self,
        properties: Mapping[str, Any],
        associations: Iterable[Mapping[str, Any]] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"properties": dict(properties)}
        if associations:
            payload["associations"] = [dict(item) for item in associations]
        if options:
            payload.update(dict(options))
        return payload

    def build_properties_params(
        self,
        properties: Iterable[str] | None,
        associations: Iterable[str] | None,
    ) -> Mapping[str, Any] | None:
        params: dict[str, Any] = {}
        if properties:
            params["properties"] = list(properties)
        if associations:
            params["associations"] = list(associations)
        return params or None

    def crm_object_path(self, object_type: str, object_id: str | None = None) -> str:
        normalized = object_type.strip("/")
        path = f"/crm/v3/objects/{normalized}"
        if object_id:
            path = f"{path}/{object_id}"
        return path

    async def search_objects(
        self,
        object_type: str,
        *,
        filters: Sequence[Mapping[str, Any]] | None = None,
        filter_groups: Sequence[Mapping[str, Any]] | None = None,
        query: str | None = None,
        properties: Iterable[str] | None = None,
        limit: int | None = None,
        after: str | None = None,
        sorts: Sequence[Mapping[str, Any]] | None = None,
    ) -> Any:
        payload: dict[str, Any] = {}
        if filter_groups:
            payload["filterGroups"] = [dict(group) for group in filter_groups]
        elif filters:
            payload["filterGroups"] = [{"filters": [dict(flt) for flt in filters]}]
        if query:
            payload["query"] = query
        if properties:
            payload["properties"] = list(properties)
        if limit is not None:
            payload["limit"] = limit
        if after is not None:
            payload["after"] = after
        if sorts:
            payload["sorts"] = [dict(sort) for sort in sorts]
        response = await self.provider.request(
            "POST",
            f"{self.crm_object_path(object_type)}/search",
            json=payload,
        )
        return self.provider.process_httpx_response(response)

    async def find_or_create_object(
        self,
        object_type: str,
        *,
        create_properties: Mapping[str, Any],
        create_associations: Iterable[Mapping[str, Any]] | None = None,
        filters: Sequence[Mapping[str, Any]] | None = None,
        filter_groups: Sequence[Mapping[str, Any]] | None = None,
        query: str | None = None,
        properties: Iterable[str] | None = None,
        sorts: Sequence[Mapping[str, Any]] | None = None,
    ) -> Any:
        search_response = await self.search_objects(
            object_type,
            filters=filters,
            filter_groups=filter_groups,
            query=query,
            properties=properties,
            limit=1,
            sorts=sorts,
        )
        if isinstance(search_response, Mapping):
            results = search_response.get("results")
            if isinstance(results, Sequence) and results:
                return results[0]
        response = await self.provider.request(
            "POST",
            self.crm_object_path(object_type),
            json=self.build_object_payload(
                create_properties,
                create_associations,
            ),
        )
        return self.provider.process_httpx_response(response)

    def encode_json(self, payload: Mapping[str, Any]) -> str:
        return json.dumps(payload)
