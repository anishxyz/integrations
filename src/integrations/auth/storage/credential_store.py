from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

SubjectLike = str | Mapping[str, Any]
StoredData = Mapping[str, Any]


class CredentialStore(Protocol):
    """Contract for persisting provider credentials."""

    async def get(self, provider: str, subject: SubjectLike) -> StoredData | None: ...

    async def set(
        self,
        provider: str,
        subject: SubjectLike,
        data: StoredData,
    ) -> None: ...

    async def delete(self, provider: str, subject: SubjectLike) -> None: ...


__all__ = ["CredentialStore", "SubjectLike", "StoredData"]
