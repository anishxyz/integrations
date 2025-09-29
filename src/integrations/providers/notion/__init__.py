"""Notion provider exports."""

from ...core import ProviderKey, register_provider

from .notion_provider import NotionProvider
from .notion_settings import NotionSettings

register_provider(ProviderKey.NOTION, NotionProvider)

__all__ = [
    "NotionProvider",
    "NotionSettings",
]
