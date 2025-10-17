"""Simple FastAPI UI that lists registered integrations."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Imports every provider module so the registry contains them all.
from integrations.providers import *  # noqa: F401,F403
from integrations import available_providers, get_provider
from integrations.core.actions import _ActionDescriptor
from integrations.core.provider_key import provider_key as normalise_provider_key

from .storage.database import (
    DSession,
    create_db_and_tables,
    engine,
    sync_provider_registry,
)
from .storage.models import AppConfiguration, Connection, Provider
from .types.app_configuration import AppConfigurationModel
from .types.credentials import CredentialsModel

BASE_DIR = Path(__file__).parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs once on startup
    create_db_and_tables()
    sync_provider_registry()
    try:
        yield
    finally:
        # runs once on shutdown
        engine.dispose()


app = FastAPI(title="Integrations SDK UI", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def ui_root(request: Request) -> HTMLResponse:
    provider_map = available_providers()
    providers = sorted(provider_map.keys())
    provider_actions = {}
    for key in providers:
        provider_cls = get_provider(key)
        action_names = sorted(
            name
            for name, attr in provider_cls.__dict__.items()
            if isinstance(attr, _ActionDescriptor)
        )
        provider_actions[key] = action_names
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "providers": providers,
            "provider_actions": provider_actions,
        },
    )


class AppConfigurationCreate(BaseModel):
    provider_key: str
    configuration: AppConfigurationModel


class ConnectionCreate(BaseModel):
    provider_key: str
    credential: CredentialsModel
    app_configuration_id: Optional[int] = None
    configuration: Optional[AppConfigurationModel] = None


@app.post("/app-configurations", status_code=status.HTTP_201_CREATED)
async def create_app_configuration(
    payload: AppConfigurationCreate,
    session: DSession,
) -> dict[str, Any]:
    key = normalise_provider_key(payload.provider_key).lower()
    if session.get(Provider, key) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown provider"
        )

    record = AppConfiguration(
        provider_key=key,
        configuration=payload.configuration.model_dump(),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return {"id": record.id, "provider_key": record.provider_key}


@app.post("/connections", status_code=status.HTTP_201_CREATED)
async def create_connection(
    payload: ConnectionCreate,
    session: DSession,
) -> dict[str, Any]:
    key = normalise_provider_key(payload.provider_key).lower()
    if session.get(Provider, key) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown provider"
        )

    app_config_id = payload.app_configuration_id
    app_config: AppConfiguration | None = None

    if app_config_id is not None:
        app_config = session.get(AppConfiguration, app_config_id)
        if app_config is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App configuration not found",
            )
        if app_config.provider_key != key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider mismatch",
            )
    elif payload.configuration is not None:
        app_config = AppConfiguration(
            provider_key=key,
            configuration=payload.configuration.model_dump(),
        )
        session.add(app_config)
        session.commit()
        session.refresh(app_config)
        app_config_id = app_config.id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide app_configuration_id or configuration",
        )

    connection = Connection(
        provider_key=key,
        app_configuration_id=app_config_id,
        credential=payload.credential.model_dump(),
    )
    session.add(connection)
    session.commit()
    session.refresh(connection)
    return {
        "id": connection.id,
        "provider_key": connection.provider_key,
        "app_configuration_id": connection.app_configuration_id,
    }
