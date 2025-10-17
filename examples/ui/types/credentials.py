"""Pydantic credential payloads tracked by the UI backend."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field


class OAuth2Credentials(BaseModel):
    type: Literal["oauth2"] = "oauth2"
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None


class ApiKeyCredentials(BaseModel):
    type: Literal["api_key"] = "api_key"
    api_key: str


class GitHubInstallationCredentials(BaseModel):
    type: Literal["github_app"] = "github_app"
    installation_id: int
    installation_token: str
    expires_at: datetime


class ServiceAccountCredentials(BaseModel):
    type: Literal["service_account"] = "service_account"
    access_token: str
    expires_at: datetime


CredentialsModel = Annotated[
    Union[
        OAuth2Credentials,
        ApiKeyCredentials,
        GitHubInstallationCredentials,
        ServiceAccountCredentials,
    ],
    Field(discriminator="type"),
]
