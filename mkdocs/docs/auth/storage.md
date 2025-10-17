# Credential Storage

Auth providers rely on a `CredentialStore` to keep user tokens around between flow runs. The default `InMemoryCredentialStore` is great for local development, while production environments should implement the same async contract against a real database or secrets manager.

## CredentialStore Protocol

```python
from integrations.auth.storage import CredentialStore, SubjectLike, StoredData


class MyStore(CredentialStore):
    async def get(self, provider: str, subject: SubjectLike) -> StoredData | None:
        ...

    async def set(self, provider: str, subject: SubjectLike, data: StoredData) -> None:
        ...

    async def delete(self, provider: str, subject: SubjectLike) -> None:
        ...
```

- `provider` is the normalized auth provider name (e.g. `"github"`).
- `subject` is either a string or JSON-serializable mapping that scopes credentials to a user, team, or service account.
- `StoredData` is a mapping of primitive values. The manager will coerce it back into the provider’s `UserCredentials` model before bindings run.

Implementations should be thread- and async-safe; the store may be accessed concurrently from multiple sessions.

## In-Memory Reference

`InMemoryCredentialStore` demonstrates the expected behavior:

- Uses an `asyncio.Lock` to serialize access.
- Deep-copies data in and out so callers cannot mutate internal state.
- Normalizes mapping subjects via `json.dumps(..., sort_keys=True)` to keep keys stable.

Swap it out by passing `credential_store=MyStore()` to `AuthManager(...)`.

## Persistence Tips

- Persist the provider name and subject alongside the credential payload so revocation becomes easy.
- Consider storing additional metadata (issued at, expires at) next to the raw token for auditing, but keep it outside the credential payload you return to the manager.
- Remember to call `delete_credentials` when the user disconnects, otherwise future sessions will keep using the stale token.
