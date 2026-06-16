---
title: Client Store
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/client-store/
source_type: llms-full-txt
content_hash: sha256:d42a4581bcbd1197b2e00c7375f0bafeb179abbf8a6c96412c49b31a84e8c743
doc_id: client-store
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
    /// <returns>The client</returns>
    Task<Client> FindClientByIdAsync(string clientId);
}
```
