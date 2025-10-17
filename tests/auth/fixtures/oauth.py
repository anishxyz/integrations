from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class DummyOAuthClient:
    """Async OAuth client stub capturing constructor arguments and calls."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.authorization_calls: list[dict[str, Any]] = []
        self.fetch_calls: list[dict[str, Any]] = []
        self.refresh_calls: list[dict[str, Any]] = []

    async def __aenter__(self) -> "DummyOAuthClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        return None

    def create_authorization_url(self, url: str, **params: Any) -> tuple[str, str]:
        self.authorization_calls.append({"url": url, "params": params})
        return (f"{url}?state={params.get('state', 'state')}", params.get("state", ""))

    async def fetch_token(
        self,
        url: str,
        code: str | None = None,
        authorization_response: str | None = None,
        include_client_id: bool = False,
        **kwargs: Any,
    ) -> Mapping[str, Any]:
        self.fetch_calls.append(
            {
                "url": url,
                "code": code,
                "authorization_response": authorization_response,
                "include_client_id": include_client_id,
                "kwargs": kwargs,
            }
        )
        return {
            "access_token": "token",
            "token_type": "bearer",
            "scope": "repo user",
            "refresh_token": "refresh",
            "expires_in": 3600,
        }

    async def refresh_token(
        self, url: str, refresh_token: str | None = None, **kwargs: Any
    ) -> Mapping[str, Any]:
        self.refresh_calls.append(
            {"url": url, "refresh_token": refresh_token, "kwargs": kwargs}
        )
        return {
            "access_token": "new-token",
            "token_type": "bearer",
            "scope": "repo user",
            "refresh_token": refresh_token or "refresh",
        }
