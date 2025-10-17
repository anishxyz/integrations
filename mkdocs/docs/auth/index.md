# Auth Overview

The auth subsystem keeps provider-specific credential logic out of your application code. `AuthManager` owns the lifecycle: it wires auth providers, runs flows, persists credentials, and finally hydrates an `Integrations` container once the user is ready.

## Happy Path

- **Bootstrap the manager**

```python
from integrations.auth import AuthManager


auth = AuthManager()
```

By default the manager instantiates the first-party auth providers and an in-memory credential store. Pass provider configs or a custom store when you need something different.
 
- **Run the provider flow** (optional when you already have tokens)

```python
flow = auth.github.oauth2

step = await flow.authorize(state="run-123")
# redirect user to step["authorization_url"]

token = await flow.exchange(code="oauth-code", subject="user-123")
await auth.store_credentials("github", "user-123", token)
```

Flows produce provider-specific `UserCredentials` models. Persist them with `store_credentials` so future sessions can load them automatically.

- **Build a session and use integrations**

```python
async with auth.session(subject="user-123") as integrations:
    issue = await integrations.github.find_or_create_issue(
        owner="octocat",
        repo="hello-world",
        title="Docs shipped",
    )
```

`session(...)` scopes the work to a subject, loads any stored credentials (unless you disable `auto_load_credentials`), runs each provider binding, and returns a ready-to-use `Integrations` container. When the context manager exits nothing is persisted automatically—call `store_credentials` when you want to keep new tokens.

Need more than the basics? Dive into [Flows](./flows.md), the [Sessions deep dive](./sessions.md), or [Credential storage](./storage.md).
