"""Create a codespace in a repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CreateCodespace(BaseAction):
    """Create a codespace for the authenticated user within a repository."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repo: str,
        *,
        ref: str | None = None,
        location: str | None = None,
        geo: str | None = None,
        client_ip: str | None = None,
        machine: str | None = None,
        devcontainer_path: str | None = None,
        multi_repo_permissions_opt_out: bool | None = None,
        working_directory: str | None = None,
        idle_timeout_minutes: int | None = None,
        display_name: str | None = None,
        retention_period_minutes: int | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {}
        if ref is not None:
            payload["ref"] = ref
        if location is not None:
            payload["location"] = location
        if geo is not None:
            payload["geo"] = geo
        if client_ip is not None:
            payload["client_ip"] = client_ip
        if machine is not None:
            payload["machine"] = machine
        if devcontainer_path is not None:
            payload["devcontainer_path"] = devcontainer_path
        if multi_repo_permissions_opt_out is not None:
            payload["multi_repo_permissions_opt_out"] = multi_repo_permissions_opt_out
        if working_directory is not None:
            payload["working_directory"] = working_directory
        if idle_timeout_minutes is not None:
            payload["idle_timeout_minutes"] = idle_timeout_minutes
        if display_name is not None:
            payload["display_name"] = display_name
        if retention_period_minutes is not None:
            payload["retention_period_minutes"] = retention_period_minutes

        response = await self.provider.request(
            "POST",
            f"/repos/{owner}/{repo}/codespaces",
            json=payload or None,
        )
        return self.provider.process_httpx_response(response)
