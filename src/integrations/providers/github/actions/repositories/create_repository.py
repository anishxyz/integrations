"""Create repository action for Github."""

from __future__ import annotations

from typing import Any, Dict

from .....core import BaseAction


class CreateRepository(BaseAction):
    """Create a new repository for the authenticated user or organization."""

    async def __call__(
        self,
        name: str,
        *,
        owner: str | None = None,
        description: str | None = None,
        private: bool | None = None,
        homepage: str | None = None,
        is_template: bool | None = None,
        has_issues: bool | None = None,
        has_projects: bool | None = None,
        has_wiki: bool | None = None,
        auto_init: bool | None = None,
        gitignore_template: str | None = None,
        license_template: str | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {"name": name}

        if description is not None:
            payload["description"] = description
        if private is not None:
            payload["private"] = private
        if homepage is not None:
            payload["homepage"] = homepage
        if is_template is not None:
            payload["is_template"] = is_template
        if has_issues is not None:
            payload["has_issues"] = has_issues
        if has_projects is not None:
            payload["has_projects"] = has_projects
        if has_wiki is not None:
            payload["has_wiki"] = has_wiki
        if auto_init is not None:
            payload["auto_init"] = auto_init
        if gitignore_template is not None:
            payload["gitignore_template"] = gitignore_template
        if license_template is not None:
            payload["license_template"] = license_template

        url = f"/orgs/{owner}/repos" if owner is not None else "/user/repos"

        response = await self.provider.request("POST", url, json=payload)
        return self.provider.process_httpx_response(response)
