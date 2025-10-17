# OpenAI Agents Integration

Convert any action into an OpenAI-compatible tool with `as_tool` and wire it into the [`openai-agents`](https://github.com/openai/openai-agents-python) SDK.

## Prerequisites

```bash
uv add "integrations[agents] @ git+https://github.com/anishxyz/integrations"
```

Load your environment (tokens, etc.) before constructing the container.

## Build Tools

```python
from agents import Agent, Runner
from integrations import Integrations

integrations = Integrations()
repo_tool = integrations.github.find_repository.as_tool(
    name="find_github_repo",
    description="Find a GitHub repository by owner/name.",
)

agent = Agent(
    name="repo assistant",
    instructions="Answer questions with GitHub data.",
    tools=[repo_tool],
)

result = await Runner.run(agent, input="Find openai/openai-python")
print(result.final_output)
```

`as_tool` accepts optional overrides (`description`, `name`, `docstring_style`, etc.) if you want to tweak the surfaced schema. The action remains the source of truth for parameter validation and execution.

> Configure any required provider settings (for example `GITHUB_TOKEN`) before running the agent so the action can reach the upstream API.

## Custom Providers

You can expose your own providers to agents too:

```python
from integrations import BaseAction, BaseProvider, Integrations, ProviderSettings, action


class WeatherSettings(ProviderSettings):
    default_conditions: str = "clear skies"


class GetForecast(BaseAction):
    async def __call__(self, city: str) -> str:
        return f"{city}: {self.provider.settings.default_conditions}"


class WeatherProvider(BaseProvider[WeatherSettings]):
    settings_class = WeatherSettings
    forecast = action(GetForecast, description="Get today's forecast.")


integrations = Integrations(weather=WeatherProvider())
weather_tool = integrations.weather.forecast.as_tool(name="get_weather")
```

Every action stays async, reusable outside of agents, and can still use provider helpers like HTTP clients when needed.
