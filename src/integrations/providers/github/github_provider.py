"""Github provider implementation."""

from __future__ import annotations

from typing import Dict


from ...core import BaseProvider, HttpxClientMixin, RawHttpRequestAction, action
from .actions import (
    AddLabelsToIssue,
    CheckOrganizationMembership,
    CreateBranch,
    CreateComment,
    CreateGist,
    CreateIssue,
    CreateOrUpdateFile,
    CreatePullRequest,
    CreateRepository,
    CreateRepositoryFromTemplate,
    DeleteBranch,
    FindBranch,
    FindIssue,
    FindOrCreateIssue,
    FindOrCreatePullRequest,
    FindOrganization,
    FindPullRequest,
    FindRepository,
    FindUser,
    GetAuthenticatedUser,
    ListRepositories,
    SetProfileStatus,
    SubmitReview,
    UpdateIssue,
    UpdatePullRequest,
)
from .github_settings import GithubSettings


class GithubProvider(HttpxClientMixin, BaseProvider[GithubSettings]):
    """Github provider exposing actions for common workflows."""

    settings_class = GithubSettings

    # Repository, branch, and file actions
    list_repositories: ListRepositories
    find_repository: FindRepository
    create_repository: CreateRepository
    create_repository_from_template: CreateRepositoryFromTemplate
    create_branch: CreateBranch
    delete_branch: DeleteBranch
    find_branch: FindBranch
    create_or_update_file: CreateOrUpdateFile

    # Issue actions
    create_issue: CreateIssue
    update_issue: UpdateIssue
    add_labels_to_issue: AddLabelsToIssue
    create_comment: CreateComment
    find_issue: FindIssue
    find_or_create_issue: FindOrCreateIssue

    # Pull request actions
    create_pull_request: CreatePullRequest
    update_pull_request: UpdatePullRequest
    submit_review: SubmitReview
    find_pull_request: FindPullRequest
    find_or_create_pull_request: FindOrCreatePullRequest

    # Gist actions
    create_gist: CreateGist

    # User and organization actions
    get_authenticated_user: GetAuthenticatedUser
    find_user: FindUser
    set_profile_status: SetProfileStatus
    check_organization_membership: CheckOrganizationMembership
    find_organization: FindOrganization
    raw_request: RawHttpRequestAction

    list_repositories = action(
        ListRepositories,
        description="List repositories for the authenticated user.",
    )
    find_repository = action(
        FindRepository,
        description="Fetch a repository by owner/name.",
    )
    create_repository = action(
        CreateRepository,
        description="Create a repository for the authenticated user or org.",
    )
    create_repository_from_template = action(
        CreateRepositoryFromTemplate,
        description="Generate a repository from an existing template.",
    )
    create_branch = action(
        CreateBranch,
        description="Create a branch pointing at a given commit SHA.",
    )
    delete_branch = action(
        DeleteBranch,
        description="Delete a branch from a repository.",
    )
    find_branch = action(
        FindBranch,
        description="Retrieve details about a branch if it exists.",
    )
    create_or_update_file = action(
        CreateOrUpdateFile,
        description="Create or update a file within a repository.",
    )
    create_issue = action(
        CreateIssue,
        description="Open an issue in a repository.",
    )
    update_issue = action(
        UpdateIssue,
        description="Update an existing issue.",
    )
    add_labels_to_issue = action(
        AddLabelsToIssue,
        description="Add labels to an issue without removing existing ones.",
    )
    create_comment = action(
        CreateComment,
        description="Create a comment on an issue or pull request.",
    )
    find_issue = action(
        FindIssue,
        description="Fetch an issue by number.",
    )
    find_or_create_issue = action(
        FindOrCreateIssue,
        description="Find an issue by title or create it if missing.",
    )
    create_pull_request = action(
        CreatePullRequest,
        description="Create a pull request and optionally merge it.",
    )
    update_pull_request = action(
        UpdatePullRequest,
        description="Update pull request metadata.",
    )
    submit_review = action(
        SubmitReview,
        description="Submit a pull request review.",
    )
    find_pull_request = action(
        FindPullRequest,
        description="Fetch a pull request by number.",
    )
    find_or_create_pull_request = action(
        FindOrCreatePullRequest,
        description="Find a pull request by head/base or create one.",
    )
    create_gist = action(
        CreateGist,
        description="Create a gist with supplied files.",
    )
    get_authenticated_user = action(
        GetAuthenticatedUser,
        description="Fetch details about the authenticated user.",
    )
    find_user = action(
        FindUser,
        description="Fetch public profile information for a user.",
    )
    set_profile_status = action(
        SetProfileStatus,
        description="Update the authenticated user's profile status.",
    )
    check_organization_membership = action(
        CheckOrganizationMembership,
        description="Check if a user belongs to an organization.",
    )
    find_organization = action(
        FindOrganization,
        description="Fetch details about an organization by login.",
    )
    raw_request = action(
        RawHttpRequestAction,
        name="raw_request",
        description="Send a raw Github API request.",
    )

    def httpx_headers(self) -> Dict[str, str]:
        settings = self.settings
        token = settings.token
        if not token:
            raise ValueError("Github authorization is required")

        scheme = settings.authorization_scheme or "Bearer"
        authorization = f"{scheme} {token}".strip()

        return {
            "Authorization": authorization,
            "Accept": "application/vnd.github+json",
            "User-Agent": self.settings.user_agent,
            "X-GitHub-Api-Version": "2022-11-28",
        }
