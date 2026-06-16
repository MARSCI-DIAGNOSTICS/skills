---
title: Resource Store
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/resource-store/
source_type: llms-full-txt
content_hash: sha256:2a854d48ea4541b238b8b7f27e62433ef636add62c0f4ba53d8396ff689adb18
doc_id: identityserver/reference/stores/resource-store
---

> Documentation for the IResourceStore interface which dynamically loads identity resources, API scopes, and API resources for authorization decisions.

#### Duende.IdentityServer.Stores.IResourceStore

[Section titled "Duende.IdentityServer.Stores.IResourceStore"](#duendeidentityserverstoresiresourcestore)

Used to dynamically load resource configuration.

```csharp
/// <summary>
/// Resource retrieval
/// </summary>
public interface IResourceStore
{
    /// <summary>
    /// Gets identity resources by scope name.
    /// </summary>
    Task<IEnumerable<IdentityResource>> FindIdentityResourcesByScopeNameAsync(IEnumerable<string> scopeNames, CancellationToken ct);


    /// <summary>
    /// Gets API scopes by scope name.
    /// </summary>
    Task<IEnumerable<ApiScope>> FindApiScopesByNameAsync(IEnumerable<string> scopeNames, CancellationToken ct);


    /// <summary>
    /// Gets API resources by scope name.
    /// </summary>
    Task<IEnumerable<ApiResource>> FindApiResourcesByScopeNameAsync(IEnumerable<string> scopeNames, CancellationToken ct);


    /// <summary>
    /// Gets API resources by API resource name.
    /// </summary>
    Task<IEnumerable<ApiResource>> FindApiResourcesByNameAsync(IEnumerable<string> apiResourceNames, CancellationToken ct);


    /// <summary>
    /// Gets all resources.
    /// </summary>
    Task<Resources> GetAllResourcesAsync(CancellationToken ct);
}
```
