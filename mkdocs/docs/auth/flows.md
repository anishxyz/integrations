# Flows

Flows encapsulate the steps required to turn user interactions into credentials. Every auth provider exposes its flows as lazily-instantiated descriptors so you only pay for what you actually run.

## Flow Basics

All flows subclass `BaseAuthFlow` (`authorize`, `exchange`, `refresh`). Providers attach flows with the `flow` descriptor:

```python
from integrations.auth import AuthProvider, flow


class MyAuthProvider(AuthProvider):
    custom = flow(lambda provider: MyCustomFlow(provider.app_credentials))
```

When you access `auth.my_provider.custom` the descriptor calls your factory, caches the instance, and always returns the same flow for that provider.

## OAuth2Flow

`OAuth2Flow` is the default option and powers the built-in GitHub implementation. It wraps Authlib’s `AsyncOAuth2Client` while enforcing a consistent data model:

- `authorize` returns a dict containing the authorization URL and resolved state.
- `exchange` swaps the callback data for an `OAuth2Token` subclass and automatically includes the client ID if required.
- `refresh` expects a `refresh_token` (or one embedded in stored credentials) and returns a new token model.
- `client` / `create_client` give direct access to an `AsyncOAuth2Client` with scopes, redirect URI, and token wiring set up from `OAuth2AppCredentials`.

Override `token_class` if your provider extends the default token payload or needs additional parsing.

## App Credentials

Flows receive immutable app credentials (`AppCredentials` subclasses) when they are constructed. Use these models to describe required URLs, client IDs, or extra Authlib options. The OAuth2 helpers provide `OAuth2AppCredentials`, and the GitHub package shows how to fine-tune defaults and environment variable aliases.

## Building Custom Flows

When OAuth2 is not enough, subclass `BaseAuthFlow` and register the new flow with `flow(...)`. Your flow gets the provider instance, which exposes `app_credentials` and helpers such as credential parsing. Return strongly typed models from `exchange` so bindings can reason about the payload—hook them up in [`sessions`](sessions.md) through custom bindings.
