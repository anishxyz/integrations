"""Notion auth provider registration."""

from ...auth.auth_provider_key import AuthProviderKey
from ...auth.auth_registry import register_auth_provider
from .notion_auth_provider import (
    NotionAppCredentials,
    NotionAuthProvider,
    NotionUserCredentials,
)

register_auth_provider(AuthProviderKey.NOTION, NotionAuthProvider)

__all__ = [
    "NotionAuthProvider",
    "NotionAppCredentials",
    "NotionUserCredentials",
]
