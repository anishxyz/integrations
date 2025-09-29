"""Github provider package."""

from ...core import ProviderKey, register_provider
from .github_provider import GithubProvider
from .github_settings import GithubSettings

register_provider(ProviderKey.GITHUB, GithubProvider)

__all__ = ["GithubProvider", "GithubSettings"]
