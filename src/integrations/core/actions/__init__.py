"""Base action primitives and registration helpers."""

from .base_action import BaseAction
from .registration import ActionFactory, action

__all__ = ["BaseAction", "ActionFactory", "action"]
