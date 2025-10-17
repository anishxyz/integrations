# Actions

Providers expose async callables for common workflows. Built-ins talk to HTTP APIs today, but actions stay transport-agnostic.

## Call Actions

```python
from integrations import Integrations


integrations = Integrations()
result = await integrations.slack.send_channel_message(
    channel="#ops",
    text="deploy finished",
)
```

Use `provider.actions` if you need discovery at runtime.

```python
from integrations import Integrations


integrations = Integrations()
for name in integrations.github.actions:
    print(name)
```

## Register Actions

Actions extend `BaseAction` and register on providers via the `action()`
descriptor. The descriptor instantiates the action once per provider, injects
the provider instance, and optionally derives name/description metadata from the
class. Review the [Providers](providers.md) guide for how providers are
hydrated.

```python
from integrations.core import (
    BaseAction,
    BaseProvider,
    HttpxClientMixin,
    ProviderSettings,
    action,
)


class ChatSettings(ProviderSettings):
    api_token: str


class PostMessage(BaseAction):
    async def __call__(self, channel: str, text: str) -> dict:
        response = await self.provider.request(
            "POST",
            "/chat.postMessage",
            json={"channel": channel, "text": text},
        )
        return self.provider.process_httpx_response(response)


class ChatProvider(HttpxClientMixin, BaseProvider[ChatSettings]):
    post_message: PostMessage
    post_message = action(PostMessage, description="Send a chat message.")
```

When an action exposes reusable behavior, move that logic into a
provider-scoped base action under `src/integrations/providers/<provider>/actions/`.

## Raw Requests

Every HTTP provider publishes `raw_request` for one-off endpoints.

```python
from integrations import Integrations


integrations = Integrations()
payload = await integrations.github.raw_request(
    "GET",
    "/repos/octocat/Hello-World",
    params={"per_page": 10},
)
```

When a provider opts into the HTTPX mixin, it handles auth headers, base URLs, timeouts, and JSON parsing for you.

## Agent Tools

Actions can become OpenAI function tools with one line.

```python
from integrations import Integrations


integrations = Integrations()
tool = integrations.google_drive.upload_file.as_tool()
```

Install `openai-agents` to activate this bridge. See the
[OpenAI Agents](../extras/openai-agents.md) guide for wiring these tools into
chat completions.
