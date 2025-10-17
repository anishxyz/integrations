"""Convenience exports for UI configuration and persistence models."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, SQLModel

from ..types.app_configuration import AppConfigurationModel
from ..types.credentials import CredentialsModel
from ..utils.timestamp import unix_ts


class Provider(SQLModel, table=True):
    __tablename__ = "providers"

    key: str = Field(primary_key=True, index=True)
    created_at: int = Field(default_factory=unix_ts)


class AppConfiguration(SQLModel, table=True):
    __tablename__ = "app_configurations"

    id: Optional[int] = Field(default=None, primary_key=True)
    provider_key: str = Field(foreign_key="providers.key", index=True)
    created_at: int = Field(default_factory=unix_ts)
    configuration: Optional[AppConfigurationModel] = Field(
        default=None,
        sa_column=Column(JSON),
    )


class Connection(SQLModel, table=True):
    __tablename__ = "connections"

    id: Optional[int] = Field(default=None, primary_key=True)
    provider_key: str = Field(foreign_key="providers.key", index=True)
    app_configuration_id: int = Field(
        foreign_key="app_configurations.id",
        index=True,
    )
    created_at: int = Field(default_factory=unix_ts)
    credential: Optional[CredentialsModel] = Field(
        default=None,
        sa_column=Column(JSON),
    )
