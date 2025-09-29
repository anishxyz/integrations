"""Gmail provider package."""

from ...core import ProviderKey, register_provider
from .gmail_provider import GmailProvider
from .gmail_settings import GmailSettings

register_provider(ProviderKey.GMAIL, GmailProvider)

__all__ = ["GmailProvider", "GmailSettings"]
