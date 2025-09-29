"""Find HubSpot companies."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from ..hubspot_base_action import HubspotBaseAction


class FindCompany(HubspotBaseAction):
    """Search for HubSpot companies."""

    async def __call__(
        self,
        *,
        filters: Sequence[Mapping[str, Any]] | None = None,
        filter_groups: Sequence[Mapping[str, Any]] | None = None,
        query: str | None = None,
        properties: Iterable[str] | None = None,
        limit: int | None = None,
        after: str | None = None,
        sorts: Sequence[Mapping[str, Any]] | None = None,
    ) -> Any:
        return await self.search_objects(
            "companies",
            filters=filters,
            filter_groups=filter_groups,
            query=query,
            properties=properties,
            limit=limit,
            after=after,
            sorts=sorts,
        )
