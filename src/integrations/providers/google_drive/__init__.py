"""Google Drive provider package."""

from ...core import ProviderKey, register_provider
from .google_drive_provider import GoogleDriveProvider
from .google_drive_settings import GoogleDriveSettings

register_provider(ProviderKey.GOOGLE_DRIVE, GoogleDriveProvider)

__all__ = ["GoogleDriveProvider", "GoogleDriveSettings"]
