"""Gmail provider implementation."""

from __future__ import annotations

from typing import Dict

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddLabelToEmail,
    ArchiveEmail,
    CreateDraft,
    MoveEmail,
    RemoveLabelFromEmail,
    SendEmail,
    SendEmailUsingAlias,
    StarEmail,
    TrashEmail,
    UnstarEmail,
    UntrashEmail,
)
from .gmail_settings import GmailSettings


class GmailProvider(HttpxClientMixin, BaseProvider[GmailSettings]):
    """Provider exposing a set of high-level Gmail actions."""

    settings_class = GmailSettings

    send_email: SendEmail
    send_email_using_alias: SendEmailUsingAlias
    create_draft: CreateDraft
    add_label_to_email: AddLabelToEmail
    remove_label_from_email: RemoveLabelFromEmail
    move_email: MoveEmail
    star_email: StarEmail
    unstar_email: UnstarEmail
    trash_email: TrashEmail
    untrash_email: UntrashEmail
    archive_email: ArchiveEmail
    raw_request: RawHttpRequestAction

    send_email = action(
        SendEmail,
        description="Send an email using the authenticated Gmail account.",
    )
    send_email_using_alias = action(
        SendEmailUsingAlias,
        description="Send an email using one of the configured Gmail aliases.",
    )
    create_draft = action(
        CreateDraft,
        description="Create an email draft in Gmail.",
    )
    add_label_to_email = action(
        AddLabelToEmail,
        description="Apply labels to an email message.",
    )
    remove_label_from_email = action(
        RemoveLabelFromEmail,
        description="Remove labels from an email message.",
    )
    move_email = action(
        MoveEmail,
        description="Move an email by adjusting its labels.",
    )
    star_email = action(
        StarEmail,
        description="Star an email message.",
    )
    unstar_email = action(
        UnstarEmail,
        description="Remove the star from an email message.",
    )
    trash_email = action(
        TrashEmail,
        description="Move an email message to the trash.",
    )
    untrash_email = action(
        UntrashEmail,
        description="Restore an email message from the trash.",
    )
    archive_email = action(
        ArchiveEmail,
        description="Archive an email message.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Execute an arbitrary Gmail API request.",
    )

    def httpx_headers(self) -> Dict[str, str]:
        settings = self.settings
        token = settings.token
        if not token:
            raise ValueError("Gmail authorization is required")

        scheme = settings.authorization_scheme or "Bearer"
        authorization = f"{scheme} {token}".strip()

        headers: Dict[str, str] = {
            "Authorization": authorization,
            "Accept": "application/json",
        }
        # Gmail API accepts JSON payloads for the actions we expose.
        headers.setdefault("Content-Type", "application/json")
        return headers
