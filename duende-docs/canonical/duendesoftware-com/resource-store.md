---
title: Resource Store
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/resource-store/
source_type: llms-full-txt
content_hash: sha256:fa6a71a30f2ef28bc28e8edaa75fcbc57338f337dd3420093a33fe99efa35c43
doc_id: resource-store
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
    Task<IEnumerable<IdentityResource>> FindIdentityResourcesByScopeNameAsync(IEnumerable<string> scopeNames);


    /// <summary>
    /// Gets API scopes by scope name.
    /// </summary>
    Task<IEnumerable<ApiScope>> FindApiScopesByNameAsync(IEnumerable<string> scopeNames);


    /// <summary>
    /// Gets API resources by scope name.
    /// </summary>
    Task<IEnumerable<ApiResource>> FindApiResourcesByScopeNameAsync(IEnumerable<string> scopeNames);


    /// <summary>
    /// Gets API resources by API resource name.
    /// </summary>
    Task<IEnumerable<ApiResource>> FindApiResourcesByNameAsync(IEnumerable<string> apiResourceNames);


    /// <summary>
    /// Gets all resources.
    /// </summary>
    Task<Resources> GetAllResourcesAsync();
}
```
