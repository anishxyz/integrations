from __future__ import annotations

import asyncio
import copy
import json
from typing import Any

from .credential_store import CredentialStore, StoredData, SubjectLike


class InMemoryCredentialStore(CredentialStore):
    """Async-safe in-memory store for development and tests."""

    def __init__(self) -> None:
        self._records: dict[str, dict[str, dict[str, Any]]] = {}
        self._lock = asyncio.Lock()

    async def get(self, provider: str, subject: SubjectLike) -> StoredData | None:
        key = _normalize_subject(subject)
        async with self._lock:
            provider_data = self._records.get(provider)
            if not provider_data:
                return None
            record = provider_data.get(key)
            if record is None:
                return None
            return copy.deepcopy(record)

    async def set(
        self,
        provider: str,
        subject: SubjectLike,
        data: StoredData,
    ) -> None:
        key = _normalize_subject(subject)
        async with self._lock:
            provider_data = self._records.setdefault(provider, {})
            provider_data[key] = copy.deepcopy(dict(data))

    async def delete(self, provider: str, subject: SubjectLike) -> None:
        key = _normalize_subject(subject)
        async with self._lock:
            provider_data = self._records.get(provider)
            if not provider_data:
                return
            provider_data.pop(key, None)
            if not provider_data:
                self._records.pop(provider, None)


def _normalize_subject(subject: SubjectLike) -> str:
    if isinstance(subject, str):
        return subject
    try:
        return json.dumps(subject, sort_keys=True, separators=(",", ":"))
    except TypeError as exc:  # pragma: no cover - defensive only
        raise TypeError("Subject mappings must be JSON-serializable") from exc


__all__ = ["InMemoryCredentialStore"]
