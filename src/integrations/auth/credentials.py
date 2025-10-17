from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppCredentials(BaseSettings):
    """Base class for app-level credentials (client config, API keys, etc.)."""

    model_config = SettingsConfigDict(
        extra="allow",
        populate_by_name=True,
        frozen=True,
    )


class UserCredentials(BaseModel):
    """Base class for end-user credential payloads returned by flows."""

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
