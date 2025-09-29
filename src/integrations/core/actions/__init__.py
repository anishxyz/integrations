"""Base action infrastructure and registration helpers."""

from __future__ import annotations

import inspect
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Literal,
    Protocol,
    TypeVar,
    overload,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..provider import BaseProvider
    from agents import AgentBase, FunctionTool, RunContextWrapper
    from agents.function_schema import DocstringStyle
    from agents.tool import ToolErrorFunction
    from agents.util._types import MaybeAwaitable


ActionT = TypeVar("ActionT", bound="BaseAction")


class BaseAction:
    """Base class for actions bound to a provider."""

    def __init__(
        self,
        provider: "BaseProvider",
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        self.provider = provider
        self.name = name or getattr(self, "name", self.__class__.__name__)
        self.description = (
            description
            if description is not None
            else getattr(self, "description", None)
        )

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def as_tool(
        self,
        *,
        platform: Literal["openai"] = "openai",
        name: str | None = None,
        description: str | None = None,
        docstring_style: "DocstringStyle" | None = None,
        use_docstring_info: bool | None = None,
        failure_error_function: "ToolErrorFunction" | None = None,
        strict_mode: bool = True,
        is_enabled: bool
        | Callable[
            ["RunContextWrapper[Any]", "AgentBase"], "MaybeAwaitable[bool]"
        ] = True,
    ) -> "FunctionTool":
        """Convert the action to a tool for the requested agent platform."""

        if platform != "openai":
            raise NotImplementedError(
                f"Tool conversion for platform '{platform}' is not implemented."
            )

        return self._as_openai_tool(
            name=name,
            description=description,
            docstring_style=docstring_style,
            use_docstring_info=use_docstring_info,
            failure_error_function=failure_error_function,
            strict_mode=strict_mode,
            is_enabled=is_enabled,
        )

    def _as_openai_tool(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        docstring_style: "DocstringStyle" | None = None,
        use_docstring_info: bool | None = None,
        failure_error_function: "ToolErrorFunction" | None = None,
        strict_mode: bool = True,
        is_enabled: bool
        | Callable[
            ["RunContextWrapper[Any]", "AgentBase"], "MaybeAwaitable[bool]"
        ] = True,
    ) -> "FunctionTool":
        """Expose the action as an ``agents.FunctionTool``."""

        try:  # Import lazily so core package does not hard-require agents.
            from agents import FunctionTool, function_tool
        except ImportError as exc:  # pragma: no cover - handled at runtime
            msg = (
                "The 'agents' package is required to convert actions to tools. "
                "Install 'openai-agents' to enable this functionality."
            )
            raise RuntimeError(msg) from exc

        resolved_name = name or self.name or self.__class__.__name__
        resolved_description = description
        if resolved_description is None:
            resolved_description = self.description
        if resolved_description is None:
            doc = inspect.cleandoc(self.__class__.__doc__ or "")
            resolved_description = doc or ""

        if use_docstring_info is None:
            # Avoid pulling in "Call self as a function." when we already have context.
            use_docstring_info = not bool(resolved_description)

        tool = function_tool(
            self.__call__,
            name_override=resolved_name,
            description_override=resolved_description,
            docstring_style=docstring_style,
            use_docstring_info=use_docstring_info,
            failure_error_function=failure_error_function,
            strict_mode=strict_mode,
            is_enabled=is_enabled,
        )

        if not isinstance(tool, FunctionTool):  # pragma: no cover - defensive guard
            raise TypeError("function_tool returned a decorator unexpectedly")

        return tool


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
