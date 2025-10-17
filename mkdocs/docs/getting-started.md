# Getting Started

## Install

```bash
uv add "integrations @ git+https://github.com/anishxyz/integrations"
```

## Configure

Set provider env vars or pass settings into the container. Example GitHub token:

```bash
export GITHUB_TOKEN=ghp_example_token
```

## First Call

```python
import asyncio
from integrations import Integrations


async def main() -> None:
    integrations = Integrations()
    repo = await integrations.github.find_repository(
        owner="octocat",
        name="Hello-World",
    )
    print(repo["full_name"])


asyncio.run(main())
```

This works because `GithubSettings.token` reads `GITHUB_TOKEN`. Pass explicit overrides when you need something custom:

```python
integrations = Integrations(
    github={"token": "...", "user_agent": "integrations-demo"},
)
```
