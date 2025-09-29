# Providers Catalog
> **Stats**: 10 providers, 197 actions.

This document is the single source of truth for every provider bundled with the Integrations SDK and the actions they expose. Update it whenever a provider or action is added, renamed, or removed.

## Table of Contents
- [Asana](#asana)
- [Github](#github)
- [Gmail](#gmail)
- [Google Calendar](#google-calendar)
- [Google Drive](#google-drive)
- [Google Docs](#google-docs)
- [Google Sheets](#google-sheets)
- [Slack](#slack)
- [Hubspot](#hubspot)
- [Notion](#notion)

---

## Asana

- **Provider class**: [`AsanaProvider`](src/integrations/providers/asana/asana_provider.py)
- **Settings class**: [`AsanaSettings`](src/integrations/providers/asana/asana_settings.py)
- **Default base URL**: `https://app.asana.com/api/1.0`

### Actions

- [`create_task`](src/integrations/providers/asana/actions/tasks/create_task.py)
  - Create a task in an Asana workspace or project.
- [`update_task`](src/integrations/providers/asana/actions/tasks/update_task.py)
  - Update an existing Asana task.
- [`create_subtask`](src/integrations/providers/asana/actions/tasks/create_subtask.py)
  - Create a subtask under an Asana task.
- [`create_project`](src/integrations/providers/asana/actions/projects/create_project.py)
  - Create a project in an Asana workspace.
- [`create_section`](src/integrations/providers/asana/actions/sections/create_section.py)
  - Create a section within an Asana project.
- [`create_task_from_template`](src/integrations/providers/asana/actions/tasks/create_task_from_template.py)
  - Instantiate a task from a template.
- [`create_project_from_template`](src/integrations/providers/asana/actions/projects/create_project_from_template.py)
  - Instantiate a project from a template.
- [`duplicate_task`](src/integrations/providers/asana/actions/tasks/duplicate_task.py)
  - Duplicate an Asana task.
- [`add_tag_to_task`](src/integrations/providers/asana/actions/tasks/add_tag_to_task.py)
  - Attach a tag to an Asana task.
- [`remove_tag_from_task`](src/integrations/providers/asana/actions/tasks/remove_tag_from_task.py)
  - Remove a tag from an Asana task.
- [`attach_file`](src/integrations/providers/asana/actions/tasks/attach_file.py)
  - Upload an attachment to an Asana task.
- [`create_comment`](src/integrations/providers/asana/actions/tasks/create_comment.py)
  - Create a comment (story) on an Asana task.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Execute a raw Asana API request.
- [`find_project`](src/integrations/providers/asana/actions/projects/find_project.py)
  - Retrieve an Asana project by GID.
- [`find_section_in_project`](src/integrations/providers/asana/actions/sections/find_section_in_project.py)
  - Locate a section within an Asana project.
- [`find_task_comments`](src/integrations/providers/asana/actions/tasks/find_task_comments.py)
  - List comments (stories) on an Asana task.
- [`find_tasks_in_workspace`](src/integrations/providers/asana/actions/tasks/find_tasks_in_workspace.py)
  - List tasks in an Asana workspace.
- [`find_user`](src/integrations/providers/asana/actions/users/find_user.py)
  - Find an Asana user by GID or email.
- [`find_task`](src/integrations/providers/asana/actions/tasks/find_task.py)
  - Retrieve an Asana task by GID.
- [`find_or_create_project`](src/integrations/providers/asana/actions/projects/find_or_create_project.py)
  - Find a project by name or create it if missing.

---

## Github

- **Provider class**: [`GithubProvider`](src/integrations/providers/github/github_provider.py)
- **Settings class**: [`GithubSettings`](src/integrations/providers/github/github_settings.py)
- **Default base URL**: `https://api.github.com`

### Actions

- [`list_repositories`](src/integrations/providers/github/actions/repositories/list_repositories.py)
  - List repositories for the authenticated user.
- [`find_repository`](src/integrations/providers/github/actions/repositories/find_repository.py)
  - Fetch a repository by owner/name.
- [`create_repository`](src/integrations/providers/github/actions/repositories/create_repository.py)
  - Create a repository for the authenticated user or org.
- [`create_repository_from_template`](src/integrations/providers/github/actions/repositories/create_repository_from_template.py)
  - Generate a repository from an existing template.
- [`create_branch`](src/integrations/providers/github/actions/branches/create_branch.py)
  - Create a branch pointing at a given commit SHA.
- [`delete_branch`](src/integrations/providers/github/actions/branches/delete_branch.py)
  - Delete a branch from a repository.
- [`find_branch`](src/integrations/providers/github/actions/branches/find_branch.py)
  - Retrieve details about a branch if it exists.
- [`create_or_update_file`](src/integrations/providers/github/actions/files/create_or_update_file.py)
  - Create or update a file within a repository.
- [`create_issue`](src/integrations/providers/github/actions/issues/create_issue.py)
  - Open an issue in a repository.
- [`update_issue`](src/integrations/providers/github/actions/issues/update_issue.py)
  - Update an existing issue.
- [`add_labels_to_issue`](src/integrations/providers/github/actions/issues/add_labels_to_issue.py)
  - Add labels to an issue without removing existing ones.
- [`create_comment`](src/integrations/providers/github/actions/issues/create_comment.py)
  - Create a comment on an issue or pull request.
- [`find_issue`](src/integrations/providers/github/actions/issues/find_issue.py)
  - Fetch an issue by number.
- [`find_or_create_issue`](src/integrations/providers/github/actions/issues/find_or_create_issue.py)
  - Find an issue by title or create it if missing.
- [`create_pull_request`](src/integrations/providers/github/actions/pull_requests/create_pull_request.py)
  - Create a pull request and optionally merge it.
- [`update_pull_request`](src/integrations/providers/github/actions/pull_requests/update_pull_request.py)
  - Update pull request metadata.
- [`submit_review`](src/integrations/providers/github/actions/pull_requests/submit_review.py)
  - Submit a pull request review.
- [`find_pull_request`](src/integrations/providers/github/actions/pull_requests/find_pull_request.py)
  - Fetch a pull request by number.
- [`find_or_create_pull_request`](src/integrations/providers/github/actions/pull_requests/find_or_create_pull_request.py)
  - Find a pull request by head/base or create one.
- [`create_gist`](src/integrations/providers/github/actions/gists/create_gist.py)
  - Create a gist with supplied files.
- [`get_authenticated_user`](src/integrations/providers/github/actions/users/get_authenticated_user.py)
  - Fetch details about the authenticated user.
- [`find_user`](src/integrations/providers/github/actions/users/find_user.py)
  - Fetch public profile information for a user.
- [`set_profile_status`](src/integrations/providers/github/actions/users/set_profile_status.py)
  - Update the authenticated user's profile status.
- [`check_organization_membership`](src/integrations/providers/github/actions/organizations/check_organization_membership.py)
  - Check if a user belongs to an organization.
- [`find_organization`](src/integrations/providers/github/actions/organizations/find_organization.py)
  - Fetch details about an organization by login.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Send a raw Github API request with the configured client.

---

## Gmail

- **Provider class**: [`GmailProvider`](src/integrations/providers/gmail/gmail_provider.py)
- **Settings class**: [`GmailSettings`](src/integrations/providers/gmail/gmail_settings.py)
- **Default base URL**: `https://gmail.googleapis.com/gmail/v1`

### Actions

- [`send_email`](src/integrations/providers/gmail/actions/compose/send_email.py)
  - Send an email using the authenticated Gmail account.
- [`send_email_using_alias`](src/integrations/providers/gmail/actions/compose/send_email_using_alias.py)
  - Send an email using one of the configured Gmail aliases.
- [`create_draft`](src/integrations/providers/gmail/actions/compose/create_draft.py)
  - Create an email draft in Gmail.
- [`add_label_to_email`](src/integrations/providers/gmail/actions/labels/add_label_to_email.py)
  - Apply labels to an email message.
- [`remove_label_from_email`](src/integrations/providers/gmail/actions/labels/remove_label_from_email.py)
  - Remove labels from an email message.
- [`move_email`](src/integrations/providers/gmail/actions/labels/move_email.py)
  - Move an email by adjusting its labels.
- [`star_email`](src/integrations/providers/gmail/actions/flags/star_email.py)
  - Star an email message.
- [`unstar_email`](src/integrations/providers/gmail/actions/flags/unstar_email.py)
  - Remove the star from an email message.
- [`trash_email`](src/integrations/providers/gmail/actions/mailbox/trash_email.py)
  - Move an email message to the trash.
- [`untrash_email`](src/integrations/providers/gmail/actions/mailbox/untrash_email.py)
  - Restore an email message from the trash.
- [`archive_email`](src/integrations/providers/gmail/actions/mailbox/archive_email.py)
  - Archive an email message.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Execute an arbitrary Gmail API request.

---

## Google Calendar

- **Provider class**: [`GoogleCalendarProvider`](src/integrations/providers/google_calendar/google_calendar_provider.py)
- **Settings class**: [`GoogleCalendarSettings`](src/integrations/providers/google_calendar/google_calendar_settings.py)
- **Default base URL**: `https://www.googleapis.com/calendar/v3`

### Actions

- [`add_attendees_to_event`](src/integrations/providers/google_calendar/actions/events/add_attendees_to_event.py)
  - Invite attendees to an existing Google Calendar event.
- [`delete_event`](src/integrations/providers/google_calendar/actions/events/delete_event.py)
  - Delete a Google Calendar event.
- [`quick_add_event`](src/integrations/providers/google_calendar/actions/events/quick_add_event.py)
  - Create an event by parsing natural language text.
- [`update_event`](src/integrations/providers/google_calendar/actions/events/update_event.py)
  - Update selected fields on a Google Calendar event.
- [`retrieve_event_by_id`](src/integrations/providers/google_calendar/actions/events/retrieve_event_by_id.py)
  - Retrieve an event by its identifier.
- [`find_busy_periods`](src/integrations/providers/google_calendar/actions/availability/find_busy_periods.py)
  - Find busy periods across one or more calendars.
- [`get_calendar_information`](src/integrations/providers/google_calendar/actions/calendars/get_calendar_information.py)
  - Retrieve metadata for a Google Calendar.
- [`create_calendar`](src/integrations/providers/google_calendar/actions/calendars/create_calendar.py)
  - Create a new Google Calendar.
- [`create_detailed_event`](src/integrations/providers/google_calendar/actions/events/create_detailed_event.py)
  - Create a detailed Google Calendar event with explicit start and end.
- [`move_event_to_another_calendar`](src/integrations/providers/google_calendar/actions/events/move_event_to_another_calendar.py)
  - Move an event from one calendar to another.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Execute a raw Google Calendar API request.
- [`find_events`](src/integrations/providers/google_calendar/actions/events/find_events.py)
  - Find events that match optional filters.
- [`find_calendars`](src/integrations/providers/google_calendar/actions/calendars/find_calendars.py)
  - List calendars accessible to the user.
- [`find_or_create_event`](src/integrations/providers/google_calendar/actions/events/find_or_create_event.py)
  - Find an event or create it when missing.

---

## Google Drive

- **Provider class**: [`GoogleDriveProvider`](src/integrations/providers/google_drive/google_drive_provider.py)
- **Settings class**: [`GoogleDriveSettings`](src/integrations/providers/google_drive/google_drive_settings.py)
- **Default base URL**: `https://www.googleapis.com/drive/v3`

### Actions

- [`copy_file`](src/integrations/providers/google_drive/actions/files/copy_file.py)
  - Create a copy of an existing file.
- [`create_document_from_template`](src/integrations/providers/google_drive/actions/documents/create_document_from_template.py)
  - Copy an existing Google Doc template into a new document.
- [`export_file`](src/integrations/providers/google_drive/actions/files/export_file.py)
  - Export a Google Workspace file to a different format.
- [`create_folder`](src/integrations/providers/google_drive/actions/folders/create_folder.py)
  - Create a new empty folder.
- [`create_file_from_text`](src/integrations/providers/google_drive/actions/files/create_file_from_text.py)
  - Create a file from plain text content.
- [`upload_document`](src/integrations/providers/google_drive/actions/documents/upload_document.py)
  - Upload a file and convert it into a Google Doc.
- [`replace_file`](src/integrations/providers/google_drive/actions/files/replace_file.py)
  - Replace the binary contents of a file.
- [`add_file_sharing_preference`](src/integrations/providers/google_drive/actions/permissions/add_file_sharing_preference.py)
  - Add a sharing permission to a file.
- [`update_file_or_folder_metadata`](src/integrations/providers/google_drive/actions/files/update_file_or_folder_metadata.py)
  - Update metadata for a file or folder.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Execute a raw Google Drive API request (beta).
- [`retrieve_files`](src/integrations/providers/google_drive/actions/files/retrieve_files.py)
  - Retrieve files using custom query parameters.
- [`get_file_permissions`](src/integrations/providers/google_drive/actions/permissions/get_file_permissions.py)
  - List permissions on a file.
- [`find_folder`](src/integrations/providers/google_drive/actions/folders/find_folder.py)
  - Find a folder by name.
- [`find_or_create_folder`](src/integrations/providers/google_drive/actions/folders/find_or_create_folder.py)
  - Find a folder or create it if missing.
- [`delete_file_permanently`](src/integrations/providers/google_drive/actions/files/delete_file_permanently.py)
  - Permanently delete a file.
- [`upload_file`](src/integrations/providers/google_drive/actions/files/upload_file.py)
  - Upload new file content to Drive.
- [`move_file`](src/integrations/providers/google_drive/actions/files/move_file.py)
  - Move a file to another folder.
- [`remove_file_permission`](src/integrations/providers/google_drive/actions/permissions/remove_file_permission.py)
  - Remove a specific permission from a file.
- [`create_shared_drive`](src/integrations/providers/google_drive/actions/drives/create_shared_drive.py)
  - Create a new shared drive.
- [`create_shortcut`](src/integrations/providers/google_drive/actions/shortcuts/create_shortcut.py)
  - Create a shortcut to an existing file.
- [`update_file_or_folder_name`](src/integrations/providers/google_drive/actions/files/update_file_or_folder_name.py)
  - Rename a file or folder.
- [`delete_file`](src/integrations/providers/google_drive/actions/files/delete_file.py)
  - Move a file to the trash.
- [`retrieve_file_or_folder_by_id`](src/integrations/providers/google_drive/actions/files/retrieve_file_or_folder_by_id.py)
  - Retrieve a file or folder by its ID.
- [`find_file`](src/integrations/providers/google_drive/actions/files/find_file.py)
  - Find a file by name.
- [`find_document`](src/integrations/providers/google_drive/actions/documents/find_document.py)
  - Find a Google Doc by name using Drive search.
- [`find_or_create_file`](src/integrations/providers/google_drive/actions/files/find_or_create_file.py)
  - Find a file by name or create it if missing.
- [`find_or_create_document`](src/integrations/providers/google_drive/actions/documents/find_or_create_document.py)
  - Find a Google Doc or create it if missing.

---

## Google Docs

- **Provider class**: [`GoogleDocsProvider`](src/integrations/providers/google_docs/google_docs_provider.py)
- **Settings class**: [`GoogleDocsSettings`](src/integrations/providers/google_docs/google_docs_settings.py)
- **Default base URL**: `https://docs.googleapis.com/v1`

### Actions

- [`append_text_to_document`](src/integrations/providers/google_docs/actions/documents/append_text.py)
  - Append text to the end of a Google Doc.
- [`insert_text`](src/integrations/providers/google_docs/actions/documents/insert_text.py)
  - Insert text at a specific index in a Google Doc.
- [`format_text`](src/integrations/providers/google_docs/actions/documents/format_text.py)
  - Apply formatting to a text range in a Google Doc.
- [`update_document_properties`](src/integrations/providers/google_docs/actions/documents/update_document_properties.py)
  - Update document-level properties such as margins or background.
- [`find_and_replace_text`](src/integrations/providers/google_docs/actions/documents/find_and_replace_text.py)
  - Find and replace text across a Google Doc.
- [`insert_image`](src/integrations/providers/google_docs/actions/documents/insert_image.py)
  - Insert an inline image into a Google Doc.
- [`get_document_content`](src/integrations/providers/google_docs/actions/documents/get_document_content.py)
  - Retrieve the full content and metadata of a Google Doc.
- [`create_document_from_text`](src/integrations/providers/google_docs/actions/create/create_document_from_text.py)
  - Create a new Google Doc populated with text.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Execute a raw Google Docs API request (beta).

---

## Google Sheets

- **Provider class**: [`GoogleSheetsProvider`](src/integrations/providers/google_sheets/google_sheets_provider.py)
- **Settings class**: [`GoogleSheetsSettings`](src/integrations/providers/google_sheets/google_sheets_settings.py)
- **Default base URL**: `https://sheets.googleapis.com/v4/spreadsheets`

### Actions

- [`create_spreadsheet`](src/integrations/providers/google_sheets/actions/create_spreadsheet.py)
  - Create a new spreadsheet with optional initial sheets.
- [`create_spreadsheet_column`](src/integrations/providers/google_sheets/actions/create_spreadsheet_column.py)
  - Insert one or more columns in a worksheet.
- [`create_multiple_spreadsheet_rows`](src/integrations/providers/google_sheets/actions/create_multiple_spreadsheet_rows.py)
  - Append multiple rows to the end of a worksheet.
- [`create_spreadsheet_row`](src/integrations/providers/google_sheets/actions/create_spreadsheet_row.py)
  - Append a single row to a worksheet.
- [`create_spreadsheet_row_at_top`](src/integrations/providers/google_sheets/actions/create_spreadsheet_row_at_top.py)
  - Insert a row near the top of a worksheet and populate it.
- [`change_sheet_properties`](src/integrations/providers/google_sheets/actions/change_sheet_properties.py)
  - Update worksheet properties such as frozen rows or visibility.
- [`copy_range`](src/integrations/providers/google_sheets/actions/copy_range.py)
  - Copy data and formatting from one range to another.
- [`copy_worksheet`](src/integrations/providers/google_sheets/actions/copy_worksheet.py)
  - Copy a worksheet to another spreadsheet.
- [`clear_spreadsheet_rows`](src/integrations/providers/google_sheets/actions/clear_spreadsheet_rows.py)
  - Clear row contents without deleting the rows.
- [`delete_spreadsheet_rows`](src/integrations/providers/google_sheets/actions/delete_spreadsheet_rows.py)
  - Delete one or more rows from a worksheet.
- [`delete_sheet`](src/integrations/providers/google_sheets/actions/delete_sheet.py)
  - Delete a worksheet from the spreadsheet.
- [`format_spreadsheet_row`](src/integrations/providers/google_sheets/actions/format_spreadsheet_row.py)
  - Apply formatting to a spreadsheet row.
- [`format_cell_range`](src/integrations/providers/google_sheets/actions/format_cell_range.py)
  - Apply formatting to an arbitrary cell range.
- [`set_data_validation`](src/integrations/providers/google_sheets/actions/set_data_validation.py)
  - Set or clear data validation rules on a range.
- [`update_spreadsheet_row`](src/integrations/providers/google_sheets/actions/update_spreadsheet_row.py)
  - Update the values in a single spreadsheet row.
- [`update_spreadsheet_rows`](src/integrations/providers/google_sheets/actions/update_spreadsheet_rows.py)
  - Update the values in multiple rows at once.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Execute a raw Google Sheets API request.
- [`find_worksheet`](src/integrations/providers/google_sheets/actions/find_worksheet.py)
  - Locate a worksheet by its title.
- [`get_many_spreadsheet_rows`](src/integrations/providers/google_sheets/actions/get_many_spreadsheet_rows.py)
  - Retrieve many rows from a worksheet range.
- [`get_spreadsheet_by_id`](src/integrations/providers/google_sheets/actions/get_spreadsheet_by_id.py)
  - Fetch the raw spreadsheet metadata and sheets.
- [`find_or_create_worksheet`](src/integrations/providers/google_sheets/actions/find_or_create_worksheet.py)
  - Find a worksheet or create it if missing.
- [`create_worksheet`](src/integrations/providers/google_sheets/actions/create_worksheet.py)
  - Create a new worksheet inside the spreadsheet.
- [`create_conditional_formatting_rule`](src/integrations/providers/google_sheets/actions/create_conditional_formatting_rule.py)
  - Add a conditional formatting rule to a worksheet.
- [`rename_sheet`](src/integrations/providers/google_sheets/actions/rename_sheet.py)
  - Rename a worksheet.
- [`sort_range`](src/integrations/providers/google_sheets/actions/sort_range.py)
  - Sort a range by the specified columns.
- [`lookup_spreadsheet_rows`](src/integrations/providers/google_sheets/actions/lookup_spreadsheet_rows.py)
  - Find rows matching a lookup value.
- [`lookup_spreadsheet_row`](src/integrations/providers/google_sheets/actions/lookup_spreadsheet_row.py)
  - Find the first row matching a lookup value.
- [`find_or_create_row`](src/integrations/providers/google_sheets/actions/find_or_create_row.py)
  - Find a row or create it if none exists.
- [`get_data_range`](src/integrations/providers/google_sheets/actions/get_data_range.py)
  - Get the values for a specific range.
- [`get_row_by_id`](src/integrations/providers/google_sheets/actions/get_row_by_id.py)
  - Retrieve a row by its row number.

---

## Slack

- **Provider class**: [`SlackProvider`](src/integrations/providers/slack/slack_provider.py)
- **Settings class**: [`SlackSettings`](src/integrations/providers/slack/slack_settings.py)
- **Default base URL**: `https://slack.com/api`

### Actions

- [`send_channel_message`](src/integrations/providers/slack/actions/messages/send_channel_message.py)
  - Send a message to a Slack channel.
- [`send_direct_message`](src/integrations/providers/slack/actions/messages/send_direct_message.py)
  - Send a direct message to a Slack user.
- [`create_channel`](src/integrations/providers/slack/actions/conversations/create_channel.py)
  - Create a Slack channel.
- [`archive_channel`](src/integrations/providers/slack/actions/conversations/archive_channel.py)
  - Archive an existing Slack channel.
- [`invite_user_to_channel`](src/integrations/providers/slack/actions/conversations/invite_user_to_channel.py)
  - Invite users to a Slack channel.
- [`leave_channel`](src/integrations/providers/slack/actions/conversations/leave_channel.py)
  - Leave a Slack channel.
- [`delete_message`](src/integrations/providers/slack/actions/messages/delete_message.py)
  - Delete a message from a channel.
- [`get_message_by_timestamp`](src/integrations/providers/slack/actions/messages/get_message_by_timestamp.py)
  - Fetch a channel message by timestamp.
- [`retrieve_thread_messages`](src/integrations/providers/slack/actions/messages/retrieve_thread_messages.py)
  - Fetch messages that belong to a thread.
- [`add_reminder`](src/integrations/providers/slack/actions/reminders/add_reminder.py)
  - Create a reminder for a user or channel.
- [`delete_reminder`](src/integrations/providers/slack/actions/reminders/delete_reminder.py)
  - Delete an existing reminder.
- [`set_profile_status`](src/integrations/providers/slack/actions/profile/set_profile_status.py)
  - Set the calling user's Slack status.
- [`clear_profile_status`](src/integrations/providers/slack/actions/profile/clear_profile_status.py)
  - Clear the calling user's Slack status.
- [`search_user_by_name`](src/integrations/providers/slack/actions/users/search_user_by_name.py)
  - Search for Slack users by name.
- [`find_conversation_members`](src/integrations/providers/slack/actions/conversations/find_conversation_members.py)
  - List members of a Slack conversation.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Send a raw Slack API request with the configured client.

---

## Hubspot

- **Provider class**: [`HubspotProvider`](src/integrations/providers/hubspot/hubspot_provider.py)
- **Settings class**: [`HubspotSettings`](src/integrations/providers/hubspot/hubspot_settings.py)
- **Default base URL**: `https://api.hubapi.com`

### Actions

- [`create_contact`](src/integrations/providers/hubspot/actions/contacts/create_contact.py)
  - Create a HubSpot contact record.
- [`update_contact`](src/integrations/providers/hubspot/actions/contacts/update_contact.py)
  - Update an existing HubSpot contact.
- [`create_or_update_contact`](src/integrations/providers/hubspot/actions/contacts/create_or_update_contact.py)
  - Create or update a contact using a unique identifier.
- [`get_contact`](src/integrations/providers/hubspot/actions/contacts/get_contact.py)
  - Retrieve a contact by its HubSpot ID.
- [`find_contact`](src/integrations/providers/hubspot/actions/contacts/find_contact.py)
  - Search contacts using CRM filters and queries.
- [`find_or_create_contact`](src/integrations/providers/hubspot/actions/contacts/find_or_create_contact.py)
  - Find a contact or create it if none match.
- [`create_company`](src/integrations/providers/hubspot/actions/companies/create_company.py)
  - Create a company record in HubSpot.
- [`update_company`](src/integrations/providers/hubspot/actions/companies/update_company.py)
  - Update an existing company.
- [`get_company`](src/integrations/providers/hubspot/actions/companies/get_company.py)
  - Retrieve a company by ID.
- [`find_company`](src/integrations/providers/hubspot/actions/companies/find_company.py)
  - Search HubSpot companies.
- [`find_or_create_company`](src/integrations/providers/hubspot/actions/companies/find_or_create_company.py)
  - Find a company or create it if none match.
- [`create_deal`](src/integrations/providers/hubspot/actions/deals/create_deal.py)
  - Create a deal record.
- [`update_deal`](src/integrations/providers/hubspot/actions/deals/update_deal.py)
  - Update an existing deal.
- [`get_deal`](src/integrations/providers/hubspot/actions/deals/get_deal.py)
  - Retrieve a deal by ID.
- [`find_deal`](src/integrations/providers/hubspot/actions/deals/find_deal.py)
  - Search HubSpot deals.
- [`find_or_create_deal`](src/integrations/providers/hubspot/actions/deals/find_or_create_deal.py)
  - Find a deal or create it if none match.
- [`create_custom_object`](src/integrations/providers/hubspot/actions/custom_objects/create_custom_object.py)
  - Create a record for a custom object type.
- [`update_custom_object`](src/integrations/providers/hubspot/actions/custom_objects/update_custom_object.py)
  - Update an existing custom object record.
- [`get_custom_object`](src/integrations/providers/hubspot/actions/custom_objects/get_custom_object.py)
  - Retrieve a custom object by type and ID.
- [`find_custom_object`](src/integrations/providers/hubspot/actions/custom_objects/find_custom_object.py)
  - Search custom object records.
- [`find_or_create_custom_object`](src/integrations/providers/hubspot/actions/custom_objects/find_or_create_custom_object.py)
  - Find a custom object or create it if none match.
- [`create_line_item`](src/integrations/providers/hubspot/actions/line_items/create_line_item.py)
  - Create a line item record.
- [`find_or_create_line_item`](src/integrations/providers/hubspot/actions/line_items/find_or_create_line_item.py)
  - Find a line item or create it if none match.
- [`create_engagement`](src/integrations/providers/hubspot/actions/engagements/create_engagement.py)
  - Create a HubSpot engagement (notes, tasks, calls, etc.).
- [`remove_associations`](src/integrations/providers/hubspot/actions/associations/remove_associations.py)
  - Remove associations between CRM objects.
- [`upload_file`](src/integrations/providers/hubspot/actions/files/upload_file.py)
  - Upload a binary file to HubSpot's file manager.
- [`create_form_submission`](src/integrations/providers/hubspot/actions/forms/create_form_submission.py)
  - Submit a HubSpot form payload.
- [`remove_email_subscription`](src/integrations/providers/hubspot/actions/subscriptions/remove_email_subscription.py)
  - Unsubscribe an email address from communication preferences.
- [`create_cos_blog_post`](src/integrations/providers/hubspot/actions/cos/create_cos_blog_post.py)
  - Publish a blog post via HubSpot CMS.
- [`create_product`](src/integrations/providers/hubspot/actions/products/create_product.py)
  - Create a product record.
- [`update_product`](src/integrations/providers/hubspot/actions/products/update_product.py)
  - Update an existing product.
- [`get_product`](src/integrations/providers/hubspot/actions/products/get_product.py)
  - Retrieve a product by ID.
- [`get_file_public_url`](src/integrations/providers/hubspot/actions/files/get_file_public_url.py)
  - Generate a public URL for a stored file.
- [`get_owner_by_email`](src/integrations/providers/hubspot/actions/owners/get_owner_by_email.py)
  - Retrieve a HubSpot owner by email.
- [`get_owner_by_id`](src/integrations/providers/hubspot/actions/owners/get_owner_by_id.py)
  - Retrieve a HubSpot owner by ID.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Send a raw HubSpot API request (beta).

---

## Notion

- **Provider class**: [`NotionProvider`](src/integrations/providers/notion/notion_provider.py)
- **Settings class**: [`NotionSettings`](src/integrations/providers/notion/notion_settings.py)
- **Default base URL**: `https://api.notion.com/v1`

### Actions

- [`archive_database_item`](src/integrations/providers/notion/actions/archive_database_item.py)
  - Archive a database item.
- [`create_database_item`](src/integrations/providers/notion/actions/create_database_item.py)
  - Create an item within a database.
- [`update_database_item`](src/integrations/providers/notion/actions/update_database_item.py)
  - Update the properties of a database item.
- [`create_page`](src/integrations/providers/notion/actions/create_page.py)
  - Create a standalone page.
- [`add_content_to_page`](src/integrations/providers/notion/actions/add_content_to_page.py)
  - Append blocks to an existing page.
- [`move_page`](src/integrations/providers/notion/actions/move_page.py)
  - Move a page to a different parent.
- [`restore_database_item`](src/integrations/providers/notion/actions/restore_database_item.py)
  - Restore a previously archived database item.
- [`retrieve_page`](src/integrations/providers/notion/actions/retrieve_page.py)
  - Retrieve a page by its identifier.
- [`retrieve_database`](src/integrations/providers/notion/actions/retrieve_database.py)
  - Retrieve database metadata.
- [`add_comment`](src/integrations/providers/notion/actions/add_comment.py)
  - Add a comment to a page or block.
- [`raw_request`](src/integrations/core/actions/raw_http_request.py)
  - Send a raw API request using Notion's configured client.
