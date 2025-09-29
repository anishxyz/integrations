"""Slack provider package."""

from ...core import ProviderKey, register_provider
from .slack_provider import SlackProvider
from .slack_settings import SlackSettings

register_provider(ProviderKey.SLACK, SlackProvider)

__all__ = ["SlackProvider", "SlackSettings"]
