"""Shared helpers for Gmail actions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from integrations.core.actions import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ..gmail_provider import GmailProvider


class GmailBaseAction(BaseAction):
    """Base class providing reusable Gmail helpers."""

    provider: "GmailProvider"

    def resolve_user_id(self, user_id: str | None = None) -> str:
        return user_id or self.provider.settings.user_id
