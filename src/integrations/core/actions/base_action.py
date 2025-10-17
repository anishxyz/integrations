"""Base action infrastructure."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Callable, Literal

if TYPE_CHECKING:  # pragma: no cover
    from ..provider import BaseProvider
    from agents import AgentBase, FunctionTool, RunContextWrapper
    from agents.function_schema import DocstringStyle
    from agents.tool import ToolErrorFunction
    from agents.util._types import MaybeAwaitable


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
