# Integrations SDK
> **Provider catalog:** 10 providers, 204 actions — see [CATALOG.md](CATALOG.md).

- Lightweight Python toolkit for container-managed provider integrations.
- Providers declare Pydantic settings and async actions; the container wires them together.
- Built for flexible auth flows: app-level credentials at startup, user tokens per request, and combinations of both.

## Highlights
- **Integrations-first wiring**: Instantiate providers by passing settings or typed `ProviderKey` entries; reach them at `integrations.github` without manual plumbing.
- **Environment-ready configuration**: Settings inherit from `BaseSettings`, so env vars and aliases load automatically.
- **Action-based interface**: Implement async `BaseAction` classes and attach them with `action()` for a consistent surface.
- **Scoped overrides**: Swap tokens or entire configs with `integrations.overrides(...)`, choosing whether to merge or replace defaults.

## Installation
Install directly from GitHub while the package is being prepared for PyPI:

```bash
uv add "integrations @ git+https://github.com/anishxyz/integrations"
```

## Quick Start
- Define provider settings and pass them into the container.
- Access providers as attributes or via typed keys.
- Call async actions exposed by each provider.
- `Integrations()` auto-loads providers whose env vars validate; set `auto_configure=False` to opt out.

```python
from integrations import Integrations, ProviderKey
from integrations.providers import GithubSettings

integrations = Integrations(
    github=GithubSettings(token="ghp_example-token"),
)

# typed_integrations = Integrations(
#     **{ProviderKey.GITHUB: GithubSettings(token="ghp_example-token")}
# )

async def main() -> None:
    repos = await integrations.github.list_repositories(per_page=50)
    user = await integrations.github.get_authenticated_user()
```

## Load Settings from Environment
```python
import os
from integrations import Integrations
from integrations.providers import GithubSettings

os.environ["GITHUB_TOKEN"] = "ghp_env-token"

integrations = Integrations(github=GithubSettings())
assert integrations.github.settings.token == "ghp_env-token"
```

`GithubSettings` uses `SettingsConfigDict(populate_by_name=True)` plus `Field(validation_alias=AliasChoices("GITHUB_TOKEN", "GITHUB_PAT"))`, so either token variable works. Custom providers can follow the same pattern: set an `env_prefix` (if you want one) or declare aliases per field with `Field`/`AliasChoices`.

## Override Provider Configuration
```python
async def list_with_user_token(integrations, user_token):
    # merge=True keeps existing provider defaults (base_url, user_agent, etc.)
    async with integrations.overrides(github={"token": user_token}, merge=True):
        return await integrations.github.list_repositories(visibility="private")

# Replace settings instead of merging
async def list_with_fresh_settings(integrations):
    async with integrations.overrides(github={"token": "override"}, merge=False):
        return await integrations.github.get_authenticated_user()
```

## Register a Custom Provider
```python
from integrations import BaseAction, BaseProvider, Integrations, ProviderSettings, action, register_provider

class TodoSettings(ProviderSettings):
    api_key: str
    base_url: str = "https://api.todo.example"

class ListTasks(BaseAction):
    async def __call__(self):
        async with self.provider.httpx_client() as client:
            resp = await client.get("/tasks")
            resp.raise_for_status()
            return resp.json()

class TodoProvider(BaseProvider[TodoSettings]):
    settings_class = TodoSettings
    list_tasks = action(ListTasks)

register_provider("todo", TodoProvider)

integrations = Integrations(todo=TodoSettings(api_key="secret"))
tasks = await integrations.todo.list_tasks()
```

## Testing
```bash
uv run pytest
```

## OpenAI Agents Integration
To combine your providers with the OpenAI Agents SDK, install the extra:

```bash
uv add "integrations[agents] @ git+https://github.com/anishxyz/integrations"
```

Then turn any action into an Agents tool and wire it into an agent:

```python
weather_tool = integrations.weather.forecast.as_tool(name="get_weather")

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[weather_tool],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.
```
