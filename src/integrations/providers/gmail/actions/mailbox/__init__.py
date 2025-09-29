"""Mailbox lifecycle actions."""

from .archive_email import ArchiveEmail
from .trash_email import TrashEmail
from .untrash_email import UntrashEmail

__all__ = [
    "ArchiveEmail",
    "TrashEmail",
    "UntrashEmail",
]
