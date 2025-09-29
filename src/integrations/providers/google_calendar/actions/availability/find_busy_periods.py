"""Action for retrieving busy periods within calendars."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from ..google_calendar_base_action import GoogleCalendarBaseAction


class FindBusyPeriods(GoogleCalendarBaseAction):
    """Find busy periods across one or more Google Calendars."""

    async def __call__(
        self,
        time_min: str,
        time_max: str,
        *,
        calendar_ids: Sequence[str | Mapping[str, Any]],
        time_zone: str | None = None,
        group_expansion_max: int | None = None,
        calendar_expansion_max: int | None = None,
        extra_body: Mapping[str, Any] | None = None,
    ) -> MutableMapping[str, Any]:
        if not calendar_ids:
            raise ValueError("Provide at least one calendar to check for availability")

        items = [
            item if isinstance(item, Mapping) else {"id": item} for item in calendar_ids
        ]

        body: MutableMapping[str, Any] = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [dict(item) for item in items],
        }
        if time_zone is not None:
            body["timeZone"] = time_zone
        if group_expansion_max is not None:
            body["groupExpansionMax"] = group_expansion_max
        if calendar_expansion_max is not None:
            body["calendarExpansionMax"] = calendar_expansion_max
        if extra_body is not None:
            body.update(dict(extra_body))

        response = await self.provider.request("POST", "/freeBusy", json=body)
        return self.provider.process_httpx_response(response)
