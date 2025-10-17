"""Action for creating Github gists."""

from __future__ import annotations

from typing import Any, Dict, Mapping, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CreateGist(BaseAction):
    """Create a gist with the given files."""

    provider: "GithubProvider"

    async def __call__(
        self,
        files: Mapping[str, str],
        *,
        description: str | None = None,
        public: bool | None = None,
    ) -> Any:
        payload: Dict[str, Any] = {
            "files": {name: {"content": content} for name, content in files.items()},
        }

        if description is not None:
            payload["description"] = description
        if public is not None:
            payload["public"] = public

        response = await self.provider.request("POST", "/gists", json=payload)
        return self.provider.process_httpx_response(response)
