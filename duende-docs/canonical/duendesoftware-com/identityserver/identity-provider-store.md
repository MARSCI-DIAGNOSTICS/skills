---
title: Identity Provider Store
source_url: https://docs.duendesoftware.com/identityserver/identity-provider-store/
source_type: llms-full-txt
content_hash: sha256:ea6f1e6c1e9c8902694b08ea5fe2b131fe7a76325373039b52c913782986462d
category: identityserver
doc_id: identityserver/identity-provider-store
---

> Documentation for the IIdentityProviderStore interface which dynamically loads identity provider configurations for external authentication.

#### Duende.IdentityServer.Stores.IIdentityProviderStore

[Section titled "Duende.IdentityServer.Stores.IIdentityProviderStore"](#duendeidentityserverstoresiidentityproviderstore)

Used to dynamically load [identity provider configuration](/identityserver/reference/models/idp/).

```csharp
/// <summary>
/// Interface to model storage of identity providers.
/// </summary>
public interface IIdentityProviderStore
{
    /// <summary>
    /// Gets all identity providers name.
    /// </summary>
    Task<IEnumerable<IdentityProviderName>> GetAllSchemeNamesAsync(CancellationToken ct);


    /// <summary>
    /// Gets the identity provider by scheme name.
    /// </summary>
    /// <param name="scheme"></param>
    /// <param name="ct">The cancellation token.</param>
    /// <returns></returns>
    Task<IdentityProvider?> GetBySchemeAsync(string scheme, CancellationToken ct);
}
```

The `IdentityProvider` is intended to be a base class to model arbitrary identity providers. The default implementation included in *Duende IdentityServer* will return a derived class for OpenID Connect providers, via the `OidcProvider` class.
