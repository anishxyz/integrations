"""Pydantic models describing stored app-level configuration."""

from __future__ import annotations

from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class OAuth2AppConfig(BaseModel):
    type: Literal["oauth2"] = "oauth2"
    client_id: str
    client_secret: str
    auth_url: HttpUrl
    token_url: HttpUrl
    scopes: List[str] = Field(default_factory=list)
    redirect_urls: List[HttpUrl] = Field(default_factory=list)


class ApiKeyAppConfig(BaseModel):
    type: Literal["api_key"] = "api_key"
    api_key: str


class GitHubAppConfig(BaseModel):
    type: Literal["github.app"] = "github.app"
    app_id: str
    client_id: str
    client_secret: str
    private_key: str
    webhook_secret: Optional[str] = None


class ServiceAccountAppConfig(BaseModel):
    type: Literal["service_account"] = "service_account"
    client_email: str
    private_key: str
    scopes: List[str] = Field(default_factory=list)


AppConfigurationModel = Annotated[
    Union[
        OAuth2AppConfig,
        ApiKeyAppConfig,
        GitHubAppConfig,
        ServiceAccountAppConfig,
    ],
    Field(discriminator="type"),
]
