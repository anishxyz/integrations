"""Registry for auth providers keyed by canonical name."""

from __future__ import annotations

from typing import Dict

from .auth_provider import AuthProvider
from .auth_provider_key import AuthProviderIdentifier, auth_provider_key

_AUTH_REGISTRY: Dict[str, type[AuthProvider]] = {}


def register_auth_provider(
    name: AuthProviderIdentifier,
    provider_cls: type[AuthProvider],
) -> None:
    """Register an auth provider implementation under a canonical name."""
    key = auth_provider_key(name)
    existing = _AUTH_REGISTRY.get(key)
    if existing is not None and existing is not provider_cls:
        raise ValueError(f"Auth provider '{name}' is already registered")
    _AUTH_REGISTRY[key] = provider_cls


def get_auth_provider(name: AuthProviderIdentifier) -> type[AuthProvider]:
    key = auth_provider_key(name)
    try:
        return _AUTH_REGISTRY[key]
    except KeyError as exc:  # pragma: no cover - defensive only
        raise KeyError(f"No auth provider registered as '{name}'") from exc


def available_auth_providers() -> Dict[str, type[AuthProvider]]:
    """Return a copy of the registered auth providers mapping."""
    return dict(_AUTH_REGISTRY)
