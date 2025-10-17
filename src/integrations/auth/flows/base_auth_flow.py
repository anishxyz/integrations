from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAuthFlow(ABC):
    """Base contract for auth flows."""

    kind: str = "generic"

    @abstractmethod
    async def authorize(self, **kwargs: Any) -> Any:
        """Initiate authorization and return flow metadata."""

    @abstractmethod
    async def exchange(self, *, subject: Any, **kwargs: Any) -> Any:
        """Exchange an auth code or payload for credentials."""

    @abstractmethod
    async def refresh(
        self,
        *,
        subject: Any | None = None,
        credentials: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """Refresh credentials or provide a default no-op."""
