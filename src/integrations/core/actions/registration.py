"""Action registration helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Protocol, TypeVar, overload

from .base_action import BaseAction

if TYPE_CHECKING:  # pragma: no cover
    from ..provider import BaseProvider


ActionT = TypeVar("ActionT", bound=BaseAction)


class ActionFactory(Protocol[ActionT]):
    def __call__(self, provider: "BaseProvider") -> ActionT: ...


class _ActionDescriptor(Generic[ActionT]):
    """Descriptor that binds an action factory to a provider instance."""

    def __init__(self, factory: ActionFactory[ActionT]) -> None:
        self._factory = factory
        self._attr_name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr_name = name

    @overload
    def __get__(
        self, instance: None, owner: type | None = None
    ) -> "_ActionDescriptor[ActionT]": ...

    @overload
    def __get__(
        self, instance: "BaseProvider", owner: type | None = None
    ) -> ActionT: ...

    def __get__(
        self, instance: "BaseProvider" | None, owner: type | None = None
    ) -> ActionT | "_ActionDescriptor[ActionT]":
        if instance is None:
            return self
        if self._attr_name is None:
            raise AttributeError("Action descriptor is missing attribute name")
        return instance._get_or_create_action(self._attr_name, self._factory)  # type: ignore[attr-defined]


def action(
    action_cls: type[ActionT],
    *,
    name: str | None = None,
    description: str | None = None,
) -> _ActionDescriptor[ActionT]:
    """Register an action implemented as a ``BaseAction`` subclass."""

    if not issubclass(action_cls, BaseAction):
        raise TypeError("action() expects a BaseAction subclass")

    def factory(provider: "BaseProvider") -> ActionT:
        action_instance = action_cls(provider)
        if name is not None:
            action_instance.name = name
        if description is not None:
            action_instance.description = description
        return action_instance

    return _ActionDescriptor(factory)
