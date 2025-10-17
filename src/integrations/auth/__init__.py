"""Auth subsystem public API."""

from .auth_manager import AuthManager
from .auth_provider import AuthProvider
from .credentials import AppCredentials, UserCredentials
from .flows import BaseAuthFlow, OAuth2AppCredentials, OAuth2Flow, OAuth2Token
from .registration import flow
from .auth_registry import (
    available_auth_providers,
    get_auth_provider,
    register_auth_provider,
)

__all__ = [
    "AuthManager",
    "AuthProvider",
    "AppCredentials",
    "UserCredentials",
    "BaseAuthFlow",
    "OAuth2Flow",
    "OAuth2AppCredentials",
    "OAuth2Token",
    "flow",
    "available_auth_providers",
    "get_auth_provider",
    "register_auth_provider",
]
