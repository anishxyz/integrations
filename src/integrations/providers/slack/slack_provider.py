"""Slack provider implementation."""

from __future__ import annotations

from typing import Any, Dict

import httpx

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddReminder,
    ArchiveChannel,
    ClearProfileStatus,
    CreateChannel,
    DeleteMessage,
    DeleteReminder,
    FindConversationMembers,
    GetMessageByTimestamp,
    InviteUserToChannel,
    LeaveChannel,
    RetrieveThreadMessages,
    SearchUserByName,
    SendChannelMessage,
    SendDirectMessage,
    SetProfileStatus,
)
from .slack_settings import SlackSettings


class SlackProvider(HttpxClientMixin, BaseProvider[SlackSettings]):
    """Provider exposing Slack Web API operations."""

    settings_class = SlackSettings

    send_channel_message: SendChannelMessage
    send_direct_message: SendDirectMessage
    create_channel: CreateChannel
    archive_channel: ArchiveChannel
    invite_user_to_channel: InviteUserToChannel
    leave_channel: LeaveChannel
    delete_message: DeleteMessage
    get_message_by_timestamp: GetMessageByTimestamp
    retrieve_thread_messages: RetrieveThreadMessages
    add_reminder: AddReminder
    delete_reminder: DeleteReminder
    set_profile_status: SetProfileStatus
    clear_profile_status: ClearProfileStatus
    search_user_by_name: SearchUserByName
    find_conversation_members: FindConversationMembers
    raw_request: RawHttpRequestAction

    send_channel_message = action(
        SendChannelMessage,
        description="Send a message to a Slack channel.",
    )
    send_direct_message = action(
        SendDirectMessage,
        description="Send a direct message to a Slack user.",
    )
    create_channel = action(
        CreateChannel,
        description="Create a Slack channel.",
    )
    archive_channel = action(
        ArchiveChannel,
        description="Archive an existing Slack channel.",
    )
    invite_user_to_channel = action(
        InviteUserToChannel,
        description="Invite users to a Slack channel.",
    )
    leave_channel = action(
        LeaveChannel,
        description="Leave a Slack channel.",
    )
    delete_message = action(
        DeleteMessage,
        description="Delete a message from a channel.",
    )
    get_message_by_timestamp = action(
        GetMessageByTimestamp,
        description="Fetch a channel message by timestamp.",
    )
    retrieve_thread_messages = action(
        RetrieveThreadMessages,
        description="Fetch messages that belong to a thread.",
    )
    add_reminder = action(
        AddReminder,
        description="Create a reminder for a user or channel.",
    )
    delete_reminder = action(
        DeleteReminder,
        description="Delete an existing reminder.",
    )
    set_profile_status = action(
        SetProfileStatus,
        description="Set the calling user's Slack status.",
    )
    clear_profile_status = action(
        ClearProfileStatus,
        description="Clear the calling user's Slack status.",
    )
    search_user_by_name = action(
        SearchUserByName,
        description="Search for Slack users by name.",
    )
    find_conversation_members = action(
        FindConversationMembers,
        description="List members of a Slack conversation.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Send a raw Slack API request.",
    )

    def httpx_headers(self) -> Dict[str, str]:
        token = self.settings.token
        if not token:
            raise ValueError("Slack token is required")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

        user_agent = self.settings.user_agent
        if user_agent:
            headers["User-Agent"] = user_agent

        return headers

    def process_httpx_response(
        self,
        response: httpx.Response,
        *,
        require_json: bool = True,
        unwrap_data: bool = False,
        empty_value: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        payload = super().process_httpx_response(
            response,
            require_json=require_json,
            unwrap_data=unwrap_data,
            empty_value={} if empty_value is None else empty_value,
            **kwargs,
        )
        if isinstance(payload, dict) and payload.get("ok") is False:
            error = payload.get("error", "unknown_error")
            raise ValueError(f"Slack API error: {error}")
        return payload
