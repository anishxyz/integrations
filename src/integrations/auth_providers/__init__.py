"""Auth provider exports and registration."""

from ..auth.auth_registry import (
    available_auth_providers,
    get_auth_provider,
    register_auth_provider,
)
from .asana import (
    AsanaAppCredentials,
    AsanaAuthProvider,
    AsanaUserCredentials,
)
from .github import (
    GithubAppCredentials,
    GithubAuthProvider,
    GithubUserCredentials,
)
from .google import (
    GoogleAppCredentials,
    GoogleAuthProvider,
    GoogleUserCredentials,
)
from .hubspot import (
    HubspotAppCredentials,
    HubspotAuthProvider,
    HubspotUserCredentials,
)
from .notion import (
    NotionAppCredentials,
    NotionAuthProvider,
    NotionUserCredentials,
)
from .slack import (
    SlackAppCredentials,
    SlackAuthProvider,
    SlackUserCredentials,
)

__all__ = [
    "AsanaAuthProvider",
    "AsanaAppCredentials",
    "AsanaUserCredentials",
    "GithubAuthProvider",
    "GithubAppCredentials",
    "GithubUserCredentials",
    "GoogleAuthProvider",
    "GoogleAppCredentials",
    "GoogleUserCredentials",
    "HubspotAuthProvider",
    "HubspotAppCredentials",
    "HubspotUserCredentials",
    "NotionAuthProvider",
    "NotionAppCredentials",
    "NotionUserCredentials",
    "SlackAuthProvider",
    "SlackAppCredentials",
    "SlackUserCredentials",
    "register_auth_provider",
    "get_auth_provider",
    "available_auth_providers",
]
