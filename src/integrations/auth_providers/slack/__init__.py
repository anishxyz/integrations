"""Slack auth provider registration."""

from ...auth.auth_provider_key import AuthProviderKey
from ...auth.auth_registry import register_auth_provider
from .slack_auth_provider import (
    SlackAppCredentials,
    SlackAuthProvider,
    SlackUserCredentials,
)

register_auth_provider(AuthProviderKey.SLACK, SlackAuthProvider)

__all__ = ["SlackAuthProvider", "SlackAppCredentials", "SlackUserCredentials"]
