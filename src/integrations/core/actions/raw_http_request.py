"""Generic action for issuing raw HTTP requests via a provider."""

from __future__ import annotations

from typing import Any, Mapping

import httpx

from . import BaseAction
from ..mixins.httpx import HttpMethod


class RawHttpRequestAction(BaseAction):
    """Execute a raw HTTP request using the provider's configured client."""

    async def __call__(
        self,
        method: HttpMethod | str,
        slug: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        data: Mapping[str, Any] | None = None,
        files: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        **request_kwargs: Any,
    ) -> Any:
        """Send a request and parse the response with provider defaults.

        Parameters
        ----------
        method:
            HTTP method to use (case-insensitive).
        slug:
            Request slug or path passed through to ``provider.request``.
        request_kwargs:
            Additional keyword arguments forwarded to ``provider.request``.
        """

        response = await self.provider.request(
            method,
            slug,
            params=params,
            json=json,
            data=data,
            files=files,
            headers=headers,
            **request_kwargs,
        )

        if isinstance(response, httpx.Response) or (
            hasattr(response, "raise_for_status") and hasattr(response, "headers")
        ):
            return self.provider.process_httpx_response(response)

        return response


__all__ = ["RawHttpRequestAction"]
