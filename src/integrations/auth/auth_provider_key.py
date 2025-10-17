from __future__ import annotations

from enum import StrEnum
from typing import Union


class AuthProviderKey(StrEnum):
    GITHUB = "github"
    GOOGLE = "google"
    GMAIL = "gmail"
    GOOGLE_CALENDAR = "google_calendar"
    GOOGLE_DOCS = "google_docs"
    GOOGLE_DRIVE = "google_drive"
    GOOGLE_SHEETS = "google_sheets"
    ASANA = "asana"
    HUBSPOT = "hubspot"
    NOTION = "notion"
    SLACK = "slack"


AuthProviderIdentifier = Union[str, AuthProviderKey]


def auth_provider_key(name: AuthProviderIdentifier) -> str:
    return name if isinstance(name, str) else name.value


def normalize_auth_provider_key(
    identifier: AuthProviderIdentifier | str,
) -> AuthProviderKey:
    if isinstance(identifier, AuthProviderKey):
        return identifier
    key = auth_provider_key(identifier)
    try:
        return AuthProviderKey(key)
    except ValueError as exc:  # pragma: no cover - defensive only
        raise ValueError(f"Unknown auth provider key '{identifier}'.") from exc
