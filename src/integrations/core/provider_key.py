"""Provider metadata and helper utilities."""

from __future__ import annotations

from enum import StrEnum
from typing import Union


class ProviderKey(StrEnum):
    """Canonical names for first-party providers."""

    GITHUB = "github"
    GMAIL = "gmail"
    SLACK = "slack"
    NOTION = "notion"
    HUBSPOT = "hubspot"
    ASANA = "asana"
    GOOGLE_SHEETS = "google_sheets"
    GOOGLE_DRIVE = "google_drive"
    GOOGLE_DOCS = "google_docs"
    GOOGLE_CALENDAR = "google_calendar"


ProviderIdentifier = Union[str, ProviderKey]


def provider_key(name: ProviderIdentifier) -> str:
    """Normalize provider identifiers to lowercase strings."""

    return name if isinstance(name, str) else name.value
