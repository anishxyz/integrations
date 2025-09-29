"""Asana provider implementation."""

from __future__ import annotations

from typing import Any, Dict


from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddTagToTask,
    AttachFile,
    CreateComment,
    CreateProject,
    CreateProjectFromTemplate,
    CreateSection,
    CreateSubtask,
    CreateTask,
    CreateTaskFromTemplate,
    DuplicateTask,
    FindOrCreateProject,
    FindProject,
    FindSectionInProject,
    FindTask,
    FindTaskComments,
    FindTasksInWorkspace,
    FindUser,
    RemoveTagFromTask,
    UpdateTask,
)
from .asana_settings import AsanaSettings


class AsanaProvider(HttpxClientMixin, BaseProvider[AsanaSettings]):
    """Provider exposing Asana REST API actions."""

    settings_class = AsanaSettings

    create_task: CreateTask
    update_task: UpdateTask
    create_subtask: CreateSubtask
    create_project: CreateProject
    create_section: CreateSection
    create_task_from_template: CreateTaskFromTemplate
    create_project_from_template: CreateProjectFromTemplate
    duplicate_task: DuplicateTask
    add_tag_to_task: AddTagToTask
    remove_tag_from_task: RemoveTagFromTask
    attach_file: AttachFile
    create_comment: CreateComment
    raw_request: RawHttpRequestAction
    find_project: FindProject
    find_section_in_project: FindSectionInProject
    find_task_comments: FindTaskComments
    find_tasks_in_workspace: FindTasksInWorkspace
    find_user: FindUser
    find_task: FindTask
    find_or_create_project: FindOrCreateProject

    create_task = action(
        CreateTask,
        description="Create a task in Asana.",
    )
    update_task = action(
        UpdateTask,
        description="Update an existing Asana task.",
    )
    create_subtask = action(
        CreateSubtask,
        description="Create a subtask under an Asana task.",
    )
    create_project = action(
        CreateProject,
        description="Create an Asana project.",
    )
    create_section = action(
        CreateSection,
        description="Create a section within an Asana project.",
    )
    create_task_from_template = action(
        CreateTaskFromTemplate,
        description="Instantiate a task from a template.",
    )
    create_project_from_template = action(
        CreateProjectFromTemplate,
        description="Instantiate a project from a template.",
    )
    duplicate_task = action(
        DuplicateTask,
        description="Duplicate an Asana task.",
    )
    add_tag_to_task = action(
        AddTagToTask,
        description="Attach a tag to an Asana task.",
    )
    remove_tag_from_task = action(
        RemoveTagFromTask,
        description="Remove a tag from an Asana task.",
    )
    attach_file = action(
        AttachFile,
        description="Upload an attachment to a task.",
    )
    create_comment = action(
        CreateComment,
        description="Create a comment (story) on a task.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Execute an arbitrary Asana API request.",
    )
    find_project = action(
        FindProject,
        description="Find a project by GID.",
    )
    find_section_in_project = action(
        FindSectionInProject,
        description="Locate a section within an Asana project.",
    )
    find_task_comments = action(
        FindTaskComments,
        description="List comments (stories) on a task.",
    )
    find_tasks_in_workspace = action(
        FindTasksInWorkspace,
        description="List tasks in a workspace.",
    )
    find_user = action(
        FindUser,
        description="Find a user by GID or email.",
    )
    find_task = action(
        FindTask,
        description="Retrieve a task by GID.",
    )
    find_or_create_project = action(
        FindOrCreateProject,
        description="Find a project by name or create it if missing.",
    )

    def httpx_headers(self) -> Dict[str, str]:
        token = self.settings.token
        if not token:
            raise ValueError("Asana access token is required")

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        user_agent = self.settings.user_agent
        if user_agent:
            headers["User-Agent"] = user_agent

        return headers

    def postprocess_httpx_payload(self, payload: Any, **_: Any) -> Any:
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload
