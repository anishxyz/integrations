"""Action for creating or updating repository files."""

from __future__ import annotations

import base64
from typing import Any, Dict, Mapping, TYPE_CHECKING

from .....core import BaseAction

if TYPE_CHECKING:  # pragma: no cover - avoids runtime import cycle
    from ...github_provider import GithubProvider


class CreateOrUpdateFile(BaseAction):
    """Create or update file contents within a repository."""

    provider: "GithubProvider"

    async def __call__(
        self,
        owner: str,
        repository: str,
        path: str,
        *,
        message: str,
        content: str | bytes,
        branch: str | None = None,
        sha: str | None = None,
        committer: Mapping[str, str] | None = None,
        author: Mapping[str, str] | None = None,
    ) -> Any:
        if isinstance(content, str):
            raw_bytes = content.encode("utf-8")
        else:
            raw_bytes = content

        encoded_content = base64.b64encode(raw_bytes).decode("ascii")

        payload: Dict[str, Any] = {
            "message": message,
            "content": encoded_content,
        }

        if branch is not None:
            payload["branch"] = branch
        if sha is not None:
            payload["sha"] = sha
        if committer is not None:
            payload["committer"] = dict(committer)
        if author is not None:
            payload["author"] = dict(author)

        response = await self.provider.request(
            "PUT",
            f"/repos/{owner}/{repository}/contents/{path}",
            json=payload,
        )
        return self.provider.process_httpx_response(response)
