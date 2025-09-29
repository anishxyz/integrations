"""Action for creating Github gists."""

from __future__ import annotations

from typing import Any, Dict, Mapping

from .....core import BaseAction


class CreateGist(BaseAction):
    """Create a gist with the given files."""

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
