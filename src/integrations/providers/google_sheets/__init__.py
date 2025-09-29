"""Google Sheets provider package."""

from ...core import ProviderKey, register_provider
from .google_sheets_provider import GoogleSheetsProvider
from .google_sheets_settings import GoogleSheetsSettings

register_provider(ProviderKey.GOOGLE_SHEETS, GoogleSheetsProvider)

__all__ = ["GoogleSheetsProvider", "GoogleSheetsSettings"]
