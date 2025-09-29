"""Exports for Gmail actions."""

from .gmail_base_action import GmailBaseAction
from .compose import CreateDraft, SendEmail, SendEmailUsingAlias
from .flags import StarEmail, UnstarEmail
from .labels import AddLabelToEmail, MoveEmail, RemoveLabelFromEmail
from .mailbox import ArchiveEmail, TrashEmail, UntrashEmail

__all__ = [
    "GmailBaseAction",
    "AddLabelToEmail",
    "ArchiveEmail",
    "CreateDraft",
    "MoveEmail",
    "RemoveLabelFromEmail",
    "SendEmail",
    "SendEmailUsingAlias",
    "StarEmail",
    "TrashEmail",
    "UnstarEmail",
    "UntrashEmail",
]
