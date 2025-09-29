import asyncio
from pathlib import Path

from agents import Agent, Runner
from dotenv import load_dotenv

from integrations import BaseAction, BaseProvider, Container, ProviderSettings, action


def _load_env_file(filename: str = ".env") -> None:
    """Load the closest ``filename`` using python-dotenv."""

    start = Path(__file__).resolve().parent
    for directory in (start, *start.parents):
        candidate = directory / filename
        if candidate.exists():
            load_dotenv(candidate)
            return


_load_env_file()


class WeatherSettings(ProviderSettings):
    """Settings backing the weather provider."""

    default_conditions: str = "sunny"


class GetForecast(BaseAction):
    """Return a canned weather forecast for the requested city."""

    async def __call__(self, city: str) -> str:
        return f"The weather in {city} is {self.provider.settings.default_conditions}."


class WeatherProvider(BaseProvider[WeatherSettings]):
    """Minimal provider exposing a single forecast action."""

    settings_class = WeatherSettings

    forecast = action(
        GetForecast,
        description="Retrieve today's forecast for a city.",
    )


container = Container(
    weather=WeatherProvider(WeatherSettings(default_conditions="sunny"))
)

weather_tool = container.weather.forecast.as_tool(name="get_weather")

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[weather_tool],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())
