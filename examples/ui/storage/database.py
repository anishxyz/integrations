"""Database helpers for the UI backend."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from integrations import available_providers
from integrations.core.integrations import Integrations
from integrations.core.provider_key import provider_key

from .models import Provider

BASE_DIR = Path(__file__).resolve().parent.parent
sqlite_path = BASE_DIR / "integrations.db"
sqlite_path.parent.mkdir(parents=True, exist_ok=True)
sqlite_url = f"sqlite:///{sqlite_path}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def sync_provider_registry() -> None:
    """Ensure every registered provider has a row in the database."""

    # Import side effects that register providers against the global registry.
    import_module("integrations.providers")

    provider_keys = _known_provider_keys()
    with Session(engine) as session:
        for key in provider_keys:
            if session.get(Provider, key) is None:
                session.add(Provider(key=key))
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session


DSession = Annotated[Session, Depends(get_session)]


def _known_provider_keys() -> set[str]:
    """Return the union of provider keys defined in the registry and integrations container."""

    keys = {str(provider_key(name)) for name in available_providers().keys()}
    if not keys:
        keys.update(Integrations.__annotations__.keys())
    return keys
