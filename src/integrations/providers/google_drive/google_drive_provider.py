"""Google Drive provider implementation."""

from __future__ import annotations

from typing import Any, Callable, Mapping, MutableMapping

import httpx

from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddFileSharingPreference,
    CopyFile,
    CreateDocumentFromTemplate,
    CreateFileFromText,
    CreateFolder,
    CreateSharedDrive,
    CreateShortcut,
    DeleteFile,
    DeleteFilePermanently,
    ExportFile,
    FindDocument,
    FindFile,
    FindFolder,
    FindOrCreateDocument,
    FindOrCreateFile,
    FindOrCreateFolder,
    GetFilePermissions,
    MoveFile,
    RemoveFilePermission,
    ReplaceFile,
    RetrieveFileOrFolderById,
    RetrieveFiles,
    UpdateFileOrFolderMetadata,
    UpdateFileOrFolderName,
    UploadDocument,
    UploadFile,
)
from .google_drive_settings import GoogleDriveSettings


class GoogleDriveProvider(HttpxClientMixin, BaseProvider[GoogleDriveSettings]):
    """Provider exposing Google Drive file and folder operations."""

    settings_class = GoogleDriveSettings

    copy_file: CopyFile
    export_file: ExportFile
    create_folder: CreateFolder
    create_file_from_text: CreateFileFromText
    replace_file: ReplaceFile
    add_file_sharing_preference: AddFileSharingPreference
    update_file_or_folder_metadata: UpdateFileOrFolderMetadata
    raw_request: RawHttpRequestAction
    retrieve_files: RetrieveFiles
    get_file_permissions: GetFilePermissions
    find_folder: FindFolder
    find_or_create_folder: FindOrCreateFolder
    delete_file_permanently: DeleteFilePermanently
    upload_file: UploadFile
    move_file: MoveFile
    remove_file_permission: RemoveFilePermission
    create_shared_drive: CreateSharedDrive
    create_shortcut: CreateShortcut
    update_file_or_folder_name: UpdateFileOrFolderName
    delete_file: DeleteFile
    retrieve_file_or_folder_by_id: RetrieveFileOrFolderById
    find_file: FindFile
    find_or_create_file: FindOrCreateFile
    upload_document: UploadDocument
    find_document: FindDocument
    find_or_create_document: FindOrCreateDocument
    create_document_from_template: CreateDocumentFromTemplate

    copy_file = action(
        CopyFile,
        description="Create a copy of a file.",
    )
    export_file = action(
        ExportFile,
        description="Export a Google Workspace file to another mime type.",
    )
    create_folder = action(
        CreateFolder,
        description="Create a new folder in Drive.",
    )
    create_file_from_text = action(
        CreateFileFromText,
        description="Create a new file from plain text content.",
    )
    replace_file = action(
        ReplaceFile,
        description="Replace the binary contents of a file.",
    )
    add_file_sharing_preference = action(
        AddFileSharingPreference,
        description="Add a sharing permission to a file.",
    )
    update_file_or_folder_metadata = action(
        UpdateFileOrFolderMetadata,
        description="Update metadata for a file or folder.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Execute a raw Google Drive API request (beta).",
    )
    retrieve_files = action(
        RetrieveFiles,
        description="Retrieve files with custom query parameters.",
    )
    get_file_permissions = action(
        GetFilePermissions,
        description="List permissions applied to a file.",
    )
    find_folder = action(
        FindFolder,
        description="Find a folder by name.",
    )
    find_or_create_folder = action(
        FindOrCreateFolder,
        description="Find a folder or create it if missing.",
    )
    delete_file_permanently = action(
        DeleteFilePermanently,
        description="Permanently delete a file.",
    )
    upload_file = action(
        UploadFile,
        description="Upload a new file to Drive.",
    )
    move_file = action(
        MoveFile,
        description="Move a file to another folder.",
    )
    remove_file_permission = action(
        RemoveFilePermission,
        description="Remove a specific file permission.",
    )
    create_shared_drive = action(
        CreateSharedDrive,
        description="Create a new shared drive.",
    )
    create_shortcut = action(
        CreateShortcut,
        description="Create a shortcut to an existing file.",
    )
    update_file_or_folder_name = action(
        UpdateFileOrFolderName,
        description="Rename a file or folder.",
    )
    delete_file = action(
        DeleteFile,
        description="Move a file to the trash.",
    )
    retrieve_file_or_folder_by_id = action(
        RetrieveFileOrFolderById,
        description="Retrieve a file or folder by ID.",
    )
    find_file = action(
        FindFile,
        description="Find a file by name.",
    )
    find_or_create_file = action(
        FindOrCreateFile,
        description="Find a file or create it if missing.",
    )
    upload_document = action(
        UploadDocument,
        description="Upload a document and convert it to a Google Doc.",
    )
    find_document = action(
        FindDocument,
        description="Find a Google Doc by name.",
    )
    find_or_create_document = action(
        FindOrCreateDocument,
        description="Find a Google Doc or create it if missing.",
    )
    create_document_from_template = action(
        CreateDocumentFromTemplate,
        description="Create a Google Doc from an existing template.",
    )

    def httpx_headers(self) -> dict[str, str]:
        settings = self.settings
        token = settings.token
        if not token:
            raise ValueError("Google Drive access token is required")

        scheme = settings.authorization_scheme or "Bearer"
        headers: dict[str, str] = {
            "Authorization": f"{scheme} {token}".strip(),
            "Accept": "application/json",
        }
        user_agent = settings.user_agent
        if user_agent:
            headers["User-Agent"] = user_agent
        return headers

    def process_httpx_response(
        self,
        response: httpx.Response,
        *,
        require_json: bool = True,
        unwrap_data: bool = True,
        empty_value: Any | None = None,
        fallback: Callable[[httpx.Response], Any] | Any | None = None,
    ) -> MutableMapping[str, Any]:
        if fallback is None:

            def fallback(resp: httpx.Response) -> dict[str, str]:
                return {"value": resp.text}

        payload = super().process_httpx_response(
            response,
            require_json=require_json,
            unwrap_data=unwrap_data,
            empty_value={} if empty_value is None else empty_value,
            fallback=fallback,
        )
        if isinstance(payload, Mapping):
            error = payload.get("error")
            if isinstance(error, Mapping):
                message = error.get("message", "Google Drive API error")
                raise ValueError(message)
            return dict(payload)
        return {"value": payload}

    async def download_external(self, url: str) -> tuple[bytes, str | None]:
        from .actions.google_drive_base_action import _default_download_external

        return await _default_download_external(self, url)
