from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar, cast

from authlib.integrations.httpx_client import AsyncOAuth2Client
from pydantic import AliasChoices, ConfigDict, Field

from ..credentials import AppCredentials, UserCredentials
from .base_auth_flow import BaseAuthFlow


TokenT = TypeVar("TokenT", bound="OAuth2Token")
AppCredsT = TypeVar("AppCredsT", bound="OAuth2AppCredentials")


class OAuth2Flow(BaseAuthFlow, Generic[AppCredsT, TokenT]):
    """OAuth2 authorization code flow built on Authlib."""

    kind = "oauth2"

    def __init__(
        self,
        app_credentials: AppCredsT,
        *,
        default_scope: Sequence[str] | None = None,
        client_kwargs: Mapping[str, Any] | None = None,
        token_class: type[TokenT] | None = None,
    ) -> None:
        self.app_credentials = app_credentials
        self._default_scope = tuple(default_scope or ())
        self._client_kwargs = dict(client_kwargs or {})
        self._token_class: type[TokenT] = cast(type[TokenT], token_class or OAuth2Token)

    async def authorize(
        self,
        *,
        state: str | None = None,
        scope: Sequence[str] | None = None,
        redirect_uri: str | None = None,
        extra_params: Mapping[str, Any] | None = None,
        client_kwargs: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        async with self.client(
            scope=scope,
            redirect_uri=redirect_uri,
            **dict(client_kwargs or {}),
        ) as client:
            authorization_url, resolved_state = client.create_authorization_url(
                self._authorization_url(),
                state=state,
                **dict(extra_params or {}),
            )
        return {"authorization_url": authorization_url, "state": resolved_state}

    async def exchange(
        self,
        *,
        subject: Any,
        code: str | None = None,
        authorization_response: str | None = None,
        redirect_uri: str | None = None,
        scope: Sequence[str] | None = None,
        token_params: Mapping[str, Any] | None = None,
        client_kwargs: Mapping[str, Any] | None = None,
    ) -> TokenT:
        if code is None and authorization_response is None:
            raise ValueError("Provide either an authorization code or response URI.")
        async with self.client(
            scope=scope,
            redirect_uri=redirect_uri,
            **dict(client_kwargs or {}),
        ) as client:
            token = await client.fetch_token(
                self._token_url(),
                code=code,
                authorization_response=authorization_response,
                include_client_id=self.app_credentials.include_client_id,
                **dict(token_params or {}),
            )
        return self._token_class.from_dict(
            token, scope_separator=self.app_credentials.scope_separator
        )

    async def refresh(
        self,
        *,
        subject: Any | None = None,
        credentials: Any | None = None,
        refresh_token: str | None = None,
        scope: Sequence[str] | None = None,
        token_params: Mapping[str, Any] | None = None,
        client_kwargs: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> TokenT:
        token_data = self._coerce_token(credentials)
        refresh_token = refresh_token or token_data.get("refresh_token")
        if not refresh_token:
            raise ValueError("OAuth2 refresh requires a refresh token.")
        async with self.client(
            scope=scope,
            token=token_data or None,
            **dict(client_kwargs or {}),
        ) as client:
            refreshed = await client.refresh_token(
                self._token_url(),
                refresh_token=refresh_token,
                **dict(token_params or {}),
                **kwargs,
            )
        return self._token_class.from_dict(
            refreshed, scope_separator=self.app_credentials.scope_separator
        )

    def client(
        self,
        *,
        scope: Sequence[str] | None = None,
        redirect_uri: str | None = None,
        token: Mapping[str, Any] | None = None,
        timeout: float | tuple[float, float] | None = None,
        **client_kwargs: Any,
    ) -> AsyncOAuth2Client:
        resolved_scope = self._format_scope(scope)
        kwargs: dict[str, Any] = {
            "client_id": self.app_credentials.client_id,
            "client_secret": self.app_credentials.client_secret,
            "scope": resolved_scope,
            "redirect_uri": redirect_uri or self.app_credentials.redirect_uri,
            "token_endpoint_auth_method": self.app_credentials.token_endpoint_auth_method,
        }
        if token is not None:
            kwargs["token"] = dict(token)
        if timeout is not None:
            kwargs["timeout"] = timeout
        kwargs.update(self._client_kwargs)
        kwargs.update(client_kwargs)
        return AsyncOAuth2Client(**{k: v for k, v in kwargs.items() if v is not None})

    def create_client(
        self,
        *,
        scope: Sequence[str] | None = None,
        redirect_uri: str | None = None,
        token: Mapping[str, Any] | None = None,
        timeout: float | tuple[float, float] | None = None,
        **client_kwargs: Any,
    ) -> AsyncOAuth2Client:
        """Backward-compatible alias for `client`."""
        return self.client(
            scope=scope,
            redirect_uri=redirect_uri,
            token=token,
            timeout=timeout,
            **client_kwargs,
        )

    def _format_scope(self, scope: Sequence[str] | None) -> str | None:
        effective = tuple(scope or self._default_scope)
        if not effective:
            return None
        return self.app_credentials.scope_separator.join(effective)

    def _coerce_token(self, credentials: Any | None) -> dict[str, Any]:
        if credentials is None:
            return {}
        if isinstance(credentials, OAuth2Token):
            return credentials.to_dict(
                scope_separator=self.app_credentials.scope_separator
            )
        if isinstance(credentials, Mapping):
            return dict(credentials)
        raise TypeError("credentials must be OAuth2Token or mapping")

    def _authorization_url(self) -> str:
        url = self.app_credentials.authorization_url
        if not url:
            raise ValueError("OAuth2 flow requires 'authorization_url'.")
        return url

    def _token_url(self) -> str:
        url = self.app_credentials.token_url
        if not url:
            raise ValueError("OAuth2 flow requires 'token_url'.")
        return url


class OAuth2AppCredentials(AppCredentials):
    """Static configuration for an OAuth2 flow."""

    authorization_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("authorization_url", "authorize_url"),
    )
    token_url: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    redirect_uri: str | None = None
    scope_separator: str = " "
    include_client_id: bool = False
    token_endpoint_auth_method: str | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True, frozen=True)


class OAuth2Token(UserCredentials):
    """Normalized OAuth2 token payload."""

    access_token: str
    token_type: str = "Bearer"
    refresh_token: str | None = None
    scope: tuple[str, ...] | None = None
    expires_in: int | None = None
    expires_at: float | None = None
    id_token: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @classmethod
    def from_dict(
        cls, data: Mapping[str, Any], *, scope_separator: str = " "
    ) -> "OAuth2Token":
        scope = data.get("scope")
        if isinstance(scope, str):
            scope_tuple = tuple(filter(None, scope.split(scope_separator)))
        elif scope is None:
            scope_tuple = None
        elif isinstance(scope, Sequence):
            scope_tuple = tuple(scope)
        else:  # pragma: no cover - defensive only
            scope_tuple = None
        payload = dict(data)
        if scope_tuple is not None:
            payload["scope"] = scope_tuple
        token = cls(**payload)
        token.raw = dict(data)
        return token

    def to_dict(self, *, scope_separator: str = " ") -> dict[str, Any]:
        payload = dict(self.raw)
        payload.update(self.model_dump(exclude={"raw"}))
        if self.scope is not None:
            payload["scope"] = scope_separator.join(self.scope)
        return payload
