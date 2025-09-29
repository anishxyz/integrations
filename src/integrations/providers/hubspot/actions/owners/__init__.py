"""Owner HubSpot actions."""

from .get_owner_by_email import GetOwnerByEmail
from .get_owner_by_id import GetOwnerById

__all__ = [
    "GetOwnerByEmail",
    "GetOwnerById",
]
