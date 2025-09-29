"""Base provider abstractions."""

from __future__ import annotations

import inspect
from typing import Any, Dict, Generic, TypeVar, cast

from pydantic_settings import BaseSettings, SettingsConfigDict

from .actions import ActionFactory, BaseAction

SettingsT = TypeVar("SettingsT", bound="ProviderSettings")
ActionT = TypeVar("ActionT", bound=BaseAction)


class ProviderSettings(BaseSettings):
    """Common provider settings model that allows extra configuration."""

    model_config = SettingsConfigDict(extra="allow", populate_by_name=True)


class BaseProvider(Generic[SettingsT]):
    """Base class providers can extend to gain action registration."""

    settings_class: type[SettingsT] = ProviderSettings  # type: ignore[assignment]

    def __init__(
        self,
        settings: SettingsT | None = None,
        **settings_data: Any,
    ) -> None:
        if settings is not None and settings_data:
            raise ValueError(
                "Provide either a settings instance or keyword overrides, not both."
            )
        if settings is None:
            settings = self.settings_class(**settings_data)
        self.settings = settings
        self._actions: Dict[str, BaseAction] = {}

    def __getattr__(self, name: str) -> Any:
        try:
            return self._actions[name]
        except KeyError as exc:  # pragma: no cover - defensive only
            raise AttributeError(name) from exc

    @property
    def actions(self) -> Dict[str, BaseAction]:
        """Return the instantiated actions keyed by attribute name."""
        return dict(self._actions)

    def get_action(self, name: str) -> BaseAction:
        return self._actions[name]

    def list_actions(self) -> Dict[str, BaseAction]:
        return dict(self._actions)

    # Internal API used by action descriptor
    def _get_or_create_action(
        self, name: str, factory: ActionFactory[ActionT]
    ) -> ActionT:
        try:
            return cast(ActionT, self._actions[name])
        except KeyError:
            action = factory(self)
            if name and action.name in {None, "", action.__class__.__name__}:
                action.name = name
            if not action.description:
                doc = inspect.cleandoc(action.__class__.__doc__ or "")
                if doc:
                    action.description = doc
            self._actions[name] = action
            return action
