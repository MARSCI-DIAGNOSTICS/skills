---
title: SAML Service Provider Store
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/saml-service-provider-store/
source_type: llms-full-txt
content_hash: sha256:5dddf05d4d02a5b77045c63afdbf12b53c9e0855c793a0f0be510a0234d335f7
category: identityserver
doc_id: identityserver/reference/stores/saml-service-provider-store
---

> Documentation for the ISamlServiceProviderStore interface which retrieves SAML Service Provider configuration.

Added in 8.0 (prerelease)

The `ISamlServiceProviderStore` interface is the contract for a service that retrieves [SAML 2.0 Service Provider](/identityserver/saml/service-providers/) configuration by entity identifier. It is part of the SAML 2.0 Identity Provider feature added in v8.0 (Enterprise Edition).

#### Duende.IdentityServer.Stores.ISamlServiceProviderStore

[Section titled "Duende.IdentityServer.Stores.ISamlServiceProviderStore"](#duendeidentityserverstoresisamlserviceproviderstore)

```csharp
/// <summary>
/// Interface for retrieval of SAML Service Provider configuration.
/// </summary>
public interface ISamlServiceProviderStore
{
    /// <summary>
    /// Finds a SAML Service Provider by its entity identifier.
    /// </summary>
    /// <param name="entityId">The entity identifier of the Service Provider.</param>
    /// <param name="ct">The cancellation token.</param>
    /// <returns>The Service Provider, or null if not found.</returns>
    Task<SamlServiceProvider?> FindByEntityIdAsync(string entityId, CancellationToken ct);
}
```

#### Members

[Section titled "Members"](#members)

| Name                                                                                    | Description                                                                 |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `Task<SamlServiceProvider?> FindByEntityIdAsync(string entityId, CancellationToken ct)` | Retrieves a SAML Service Provider by its entity ID, or `null` if not found. |

For full details on the `SamlServiceProvider` model and how to register service providers, see the [SAML Service Providers](/identityserver/saml/service-providers/) page.
