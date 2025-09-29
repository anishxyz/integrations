"""HubSpot provider package."""

from ...core import ProviderKey, register_provider
from .hubspot_provider import HubspotProvider
from .hubspot_settings import HubspotSettings

register_provider(ProviderKey.HUBSPOT, HubspotProvider)

__all__ = ["HubspotProvider", "HubspotSettings"]
