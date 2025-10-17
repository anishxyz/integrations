# Providers

Providers are runtime adapters that expose a given service's API through typed
actions. They combine a Pydantic settings model, transport helpers, and an
action surface that the `Integrations` container wires together—you interact
with providers through `integrations.<provider>`.

## Settings and environment loading

Every provider ships a `ProviderSettings` subclass that drives validation and
environment-driven configuration.

```python
from integrations.providers.slack import SlackSettings

settings = SlackSettings()  # pulls from SLACK_* env vars by default
settings.token  # -> resolves aliases like SLACK_BOT_TOKEN
```

`ProviderSettings` extends `pydantic_settings.BaseSettings`, so aliases declared
with `Field(validation_alias=...)` or `AliasChoices` automatically map
environment variables into structured data. Providers keep these models small
and explicit—when the container hydrates a provider it passes these settings
along, whether they come from environment variables, overrides, or explicit
configuration.

## Container hydration

The container instantiates providers on demand. Pass configuration as keyword
arguments to `Integrations(...)`, or rely on environment values when
`auto_configure=True`.

```python
from integrations import Integrations

integrations = Integrations(slack={"token": "xoxb-..."})
await integrations.slack.send_channel_message(channel="#team", text="Hello")
```

Providers that need HTTP helpers stack `HttpxClientMixin` on the base class.
The mixin exposes `request(...)`, `httpx_client()`, and response-processing
hooks so actions can stay focused on the payload rather than client setup.
See [Actions](actions.md) for registering and extending action surfaces.

## Registering providers

Providers register themselves on import by calling `register_provider(...)`
inside their package `__init__`. The registry maps a `ProviderKey` (or string
alias) to the provider class. Once registered, the `Integrations` container can
hydrate the provider automatically.

```python
from integrations.core import (
    BaseProvider,
    ProviderKey,
    ProviderSettings,
    RawHttpRequestAction,
    action,
    register_provider,
)


class DemoSettings(ProviderSettings):
    api_key: str


class DemoProvider(BaseProvider[DemoSettings]):
    settings_class = DemoSettings

    raw_request = action(RawHttpRequestAction)


register_provider(ProviderKey("demo"), DemoProvider)
```

Third-party packages can follow the same pattern—importing them is enough for
`available_providers()` and the container to see the new entry.

Once the module that registers the provider is imported, the container can
hydrate it like any other first-party integration:

```python
from integrations import Integrations

import demo_provider_package  # ensures register_provider(...) runs

integrations = Integrations(demo={"api_key": "demo-123"})
await integrations.demo.raw_request(
    method="GET",
    url="/v1/resources",
)
```

## Building a first-party provider

First-party providers live under `src/integrations/providers/<provider>/` and
follow a consistent structure:

- `<provider>_settings.py`: define the `ProviderSettings` subclass and map env
  aliases via `SettingsConfigDict`.
- `<provider>_provider.py`: extend `BaseProvider`, declare typed action
  attributes, and assign descriptors via `action(...)`.
- `actions/`: house one action per file so dependencies stay scoped.
- `__init__.py`: register the provider by importing `register_provider` and the
  provider class, then calling `register_provider(ProviderKey.<PROVIDER>, ...)`.

With that in place, the provider becomes available through the container and can
participate in overrides, auto-configuration, and introspection. See the
[Integrations container](integrations-container.md) documentation for
container-specific behavior.
