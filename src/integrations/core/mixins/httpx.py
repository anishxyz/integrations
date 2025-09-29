"""Reusable HTTPX helper mixins for providers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, Mapping

import httpx


HttpMethod = Literal["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]


class HttpxClientMixin:
    """Mixin that provides configured ``httpx`` clients for a provider."""

    def httpx_client(self, **client_kwargs: Any) -> httpx.AsyncClient:
        """Return a fresh ``httpx.AsyncClient`` configured from provider settings."""
        return self._build_httpx_async_client(**client_kwargs)

    def httpx_headers(self) -> Mapping[str, str]:
        """Return default headers for requests."""
        return {}

    def httpx_base_url(self) -> str | None:
        """Return default ``base_url`` for the client."""
        return getattr(self.settings, "base_url", None)

    def httpx_timeout(self) -> Any:
        """Return default timeout value for the client."""
        return getattr(self.settings, "timeout", None)

    async def request(
        self,
        method: HttpMethod | str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
        files: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        **request_kwargs: Any,
    ) -> httpx.Response:
        """Execute an HTTP request using a short-lived ``httpx.AsyncClient``."""

        http_method = method.upper() if isinstance(method, str) else method
        client_kwargs: dict[str, Any] = {}
        base_url = request_kwargs.pop("base_url", None)
        if base_url is not None:
            client_kwargs["base_url"] = base_url

        async with self.httpx_client(**client_kwargs) as client:
            response = await client.request(
                http_method,
                url,
                params=dict(params) if params else None,
                json=dict(json) if json else None,
                data=dict(data) if data else None,
                files=files,
                headers=dict(headers) if headers else None,
                **request_kwargs,
            )
        return response

    def parse_httpx_response(
        self,
        response: httpx.Response,
        *,
        empty_value: Any | None = None,
        require_json: bool = False,
        fallback: Callable[[httpx.Response], Any] | Any | None = None,
    ) -> Any:
        """Normalize an ``httpx`` response by raising errors and decoding the body."""

        response.raise_for_status()
        missing = object()
        content = getattr(response, "content", missing)
        if response.status_code == 204 or (content is not missing and not content):
            return empty_value

        try:
            return response.json()
        except ValueError as exc:
            if require_json:
                raise ValueError("Expected JSON response") from exc

        if fallback is not None:
            return fallback(response) if callable(fallback) else fallback

        return response.text

    def process_httpx_response(self, response: httpx.Response, **_: Any) -> Any:
        """Parse an ``httpx`` response and apply provider-specific post-processing."""

        payload = self.parse_httpx_response(response, require_json=True)
        return self.postprocess_httpx_payload(payload)

    def postprocess_httpx_payload(self, payload: Any, **_: Any) -> Any:
        """Hook for providers to adjust the parsed payload."""

        return payload

    # Internal helpers -------------------------------------------------

    def _build_httpx_async_client(self, **client_kwargs: Any) -> httpx.AsyncClient:
        kwargs = self._apply_httpx_defaults(client_kwargs)
        return httpx.AsyncClient(**kwargs)

    def _apply_httpx_defaults(self, client_kwargs: Mapping[str, Any]) -> dict[str, Any]:
        kwargs = dict(client_kwargs)
        base_url = self.httpx_base_url()
        headers = self.httpx_headers()
        timeout = self.httpx_timeout()
        if base_url is not None:
            kwargs.setdefault("base_url", base_url)
        if headers:
            kwargs.setdefault("headers", headers)
        if timeout is not None and "timeout" not in kwargs:
            kwargs["timeout"] = timeout
        return kwargs
