# Sessions Deep Dive

`AuthManager.session(...)` is the bridge between stored credentials and the runtime `Integrations` container. It resolves which auth providers should run, gathers credentials for the active subject, calls bindings, and returns a container primed with provider settings.

## Anatomy of a Session

```python
from integrations.auth.auth_provider_key import AuthProviderKey
from integrations.auth import AuthManager

auth = AuthManager()

async with auth.session(
    subject="user-123",
    providers=[AuthProviderKey.GITHUB],
    with_credentials={AuthProviderKey.GITHUB: {"access_token": "..."}},
    auto_load_credentials=True,
    overrides={"github": {"timeout": 30}},
) as integrations:
    ...
```

- `subject` identifies the actor. It can be a string or any JSON-serializable mapping.
- `providers` (optional) filters which bindings run. When omitted, every registered binding executes.
- `with_credentials` lets you bypass the credential store for specific providers. Supply typed `UserCredentials` or plain mappings and the provider will coerce them.
- `auto_load_credentials` (default `True`) controls whether the manager looks up stored credentials when `with_credentials` is missing. Set it to `False` when handling ephemeral flows.
- `overrides` feeds directly into the `Integrations` constructor. This is ideal for swapping transport configs temporarily without building a new container.

Behind the scenes, each auth provider exposes a mapping of bindings keyed by `AuthProviderKey`. For every binding that matches the filter, the manager:

1. Normalizes the provider key (string, enum, or alias).
2. Parses manual credentials (if provided) into the provider’s `UserCredentials` model.
3. Loads stored credentials when allowed.
4. Calls `binding.to_settings(...)` with the manager, subject, and both credential models.
5. Injects the resulting `ProviderSettings` into the `Integrations` container.

## Manual Persistence

Sessions intentionally avoid writing to the credential store. They consume whatever you load or inject and then hand you the integrations container. When a flow issues new tokens, call `store_credentials` yourself before the session ends.

## Nested Overrides

The integrations container also has its own `overrides(...)` context manager. Combine it with auth sessions to prototype changes quickly:

```python
async with auth.session(subject="user-123") as integrations:
    async with integrations.overrides(github={"retry_attempts": 0}):
        await integrations.github.health_check()
```

Once the overrides exit, the original provider instances are restored but credentials remain available for future sessions.
