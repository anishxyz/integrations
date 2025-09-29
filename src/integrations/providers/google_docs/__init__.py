"""Google Docs provider package."""

from ...core import ProviderKey, register_provider
from .google_docs_provider import GoogleDocsProvider
from .google_docs_settings import GoogleDocsSettings

register_provider(ProviderKey.GOOGLE_DOCS, GoogleDocsProvider)

__all__ = ["GoogleDocsProvider", "GoogleDocsSettings"]
