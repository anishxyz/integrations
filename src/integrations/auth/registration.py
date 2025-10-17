"""Auth flow registration helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Protocol, TypeVar, overload

from .flows.base_auth_flow import BaseAuthFlow

if TYPE_CHECKING:  # pragma: no cover
    from .auth_provider import AuthProvider


FlowT = TypeVar("FlowT", bound=BaseAuthFlow)


class FlowFactory(Protocol[FlowT]):
    def __call__(self, provider: "AuthProvider") -> FlowT: ...


class _FlowDescriptor(Generic[FlowT]):
    """Descriptor that lazily instantiates provider flows."""

    def __init__(self, factory: FlowFactory[FlowT]) -> None:
        self._factory = factory
        self._attr_name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr_name = name

    @overload
    def __get__(
        self, instance: None, owner: type | None = None
    ) -> "_FlowDescriptor[FlowT]": ...

    @overload
    def __get__(self, instance: "AuthProvider", owner: type | None = None) -> FlowT: ...

    def __get__(
        self, instance: "AuthProvider" | None, owner: type | None = None
    ) -> FlowT | "_FlowDescriptor[FlowT]":
        if instance is None:
            return self
        if self._attr_name is None:
            raise AttributeError("Flow descriptor is missing attribute name")
        return instance._get_or_create_flow(self._attr_name, self._factory)


def flow(factory: FlowFactory[FlowT]) -> _FlowDescriptor[FlowT]:
    """Register a flow on an auth provider."""

    return _FlowDescriptor(factory)


def declared_flow_names(provider: "AuthProvider") -> tuple[str, ...]:
    """Return flow attribute names declared on a provider class."""

    names: list[str] = []
    for cls in type(provider).__mro__:
        for attr, value in cls.__dict__.items():
            if isinstance(value, _FlowDescriptor) and attr not in names:
                names.append(attr)
    return tuple(names)
