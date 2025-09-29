"""Registry for provider classes keyed by container attribute name."""

from __future__ import annotations

from typing import Dict

from .provider_key import ProviderIdentifier, provider_key
from .provider import BaseProvider

_REGISTRY: Dict[str, type[BaseProvider]] = {}


def register_provider(
    name: ProviderIdentifier, provider_cls: type[BaseProvider]
) -> None:
    """Register a provider implementation under a canonical name."""
    key = provider_key(name)
    existing = _REGISTRY.get(key)
    if existing is not None and existing is not provider_cls:
        raise ValueError(f"Provider '{name}' is already registered")
    _REGISTRY[key] = provider_cls


def get_provider(name: ProviderIdentifier) -> type[BaseProvider]:
    key = provider_key(name)
    try:
        return _REGISTRY[key]
    except KeyError as exc:  # pragma: no cover - defensive only
        raise KeyError(f"No provider registered as '{name}'") from exc


def available_providers() -> Dict[str, type[BaseProvider]]:
    """Return a copy of the registered providers mapping."""
    return dict(_REGISTRY)
