"""Find or create HubSpot company."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from ..hubspot_base_action import HubspotBaseAction


class FindOrCreateCompany(HubspotBaseAction):
    """Find a company or create one if none match."""

    async def __call__(
        self,
        *,
        create_properties: Mapping[str, Any],
        create_associations: Iterable[Mapping[str, Any]] | None = None,
        search_filters: Sequence[Mapping[str, Any]] | None = None,
        search_filter_groups: Sequence[Mapping[str, Any]] | None = None,
        search_query: str | None = None,
        search_properties: Iterable[str] | None = None,
        search_sorts: Sequence[Mapping[str, Any]] | None = None,
    ) -> Any:
        return await self.find_or_create_object(
            "companies",
            create_properties=create_properties,
            create_associations=create_associations,
            filters=search_filters,
            filter_groups=search_filter_groups,
            query=search_query,
            properties=search_properties,
            sorts=search_sorts,
        )
