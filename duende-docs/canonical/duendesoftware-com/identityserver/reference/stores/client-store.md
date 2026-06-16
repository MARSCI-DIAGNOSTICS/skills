---
title: Client Store
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/client-store/
source_type: llms-full-txt
content_hash: sha256:df3706ad411413264aded89e5e65a1361acf1402171d579e2dbfd7c97db93be5
doc_id: identityserver/reference/stores/client-store
---

> Documentation for the IClientStore interface which is used to dynamically load client configuration by client ID.

#### Duende.IdentityServer.Stores.IClientStore

[Section titled "Duende.IdentityServer.Stores.IClientStore"](#duendeidentityserverstoresiclientstore)

Used to dynamically load client configuration.

```csharp
/// <summary>
/// Retrieval of client configuration
/// </summary>
public interface IClientStore
{
    /// <summary>
    /// Finds a client by id
    /// </summary>
    /// <param name="clientId">The client id</param>
    /// <param name="ct">The cancellation token.</param>
    /// <returns>The client</returns>
    Task<Client?> FindClientByIdAsync(string clientId, CancellationToken ct);


    /// <summary>
    /// Returns all clients for enumeration purposes (e.g., conformance assessment).
    /// </summary>
    /// <param name="ct">The cancellation token.</param>
    /// <returns>An async enumerable of all clients.</returns>
    IAsyncEnumerable<Client> GetAllClientsAsync(CancellationToken ct);
}
```

`GetAllClientsAsync` returns all configured clients as an async enumerable. Added in 8.0 (prerelease)

Used by the [conformance report](/identityserver/diagnostics/conformance-report/) and configuration validation features. Custom `IClientStore` implementations must implement this method -- see the [upgrade guide](/identityserver/upgrades/v7_4-to-v8_0/#iclientstoregetallclientsasync-now-required) for details.
