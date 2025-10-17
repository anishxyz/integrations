# Integrations Container

`Integrations` orchestrates provider instantiation, lazy registration, and
environment-aware configuration. Providers appear as attributes on the container
(`integrations.slack`, `integrations.github`, etc.) and expose their actions
directly.

## Auto-configuration

By default the container attempts to hydrate any registered provider using
environment variables and the defaults defined on its `ProviderSettings`.

```python
from integrations import Integrations

integrations = Integrations(auto_configure=True)
```

If `auto_configure` stays `True`, every provider registered in the global
registry is instantiated. Providers whose settings cannot validate (for example,
because a required token is missing) are skipped until you supply credentials.

Disable auto-configuration when you want explicit control over which providers
load:

```python
integrations = Integrations(auto_configure=False)
integrations.register("slack", {"token": "xoxb-..."})
```

You can also pass provider configs to the constructor (`Integrations(slack=...)`)
to seed the container up front.

## Overrides

Overrides let you swap a provider (or just a subset of its settings) for the
duration of a scope. The override manager is both async- and sync-aware; prefer
the async form when you are already inside an event loop.

```python
from integrations import Integrations, provider_override

integrations = Integrations()

async with integrations.overrides(
    github=provider_override({"token": "ghp-runtime"}, merge=True),
) as runtime:
    await runtime.github.create_issue(...)
```

Use `merge=True` (the default when you omit `merge`) to patch into existing
settings; pass `merge=False` to replace the provider entirely. When an override
adds a provider that was not previously registered, it is removed after exiting
the context.

## Manual registration and lookup

The container stores providers by their canonical key. Use `.register()` to add
or replace an entry at runtime, and `.get(...)` or dictionary-style access to
fetch instances.

```python
integrations.register("notion", {"token": "secret_..."})
notion = integrations["notion"]
```

For details on how providers are implemented and registered, see the
[Providers](providers.md) guide.
