---
title: Store
source_url: https://docs.duendesoftware.com/identityserver/reference/dcr/store/
source_type: llms-full-txt
content_hash: sha256:b3fe7f9ff1bdabccce43719045c49b11d3e1459865cc33406e7ebebb56b65ecd
doc_id: identityserver/reference/dcr/store
---

> Reference documentation for the Dynamic Client Registration (DCR) store interfaces and implementations used to manage client configurations in IdentityServer

## IClientConfigurationStore

[Section titled "IClientConfigurationStore"](#iclientconfigurationstore)

The `IClientConfigurationStore` interface defines the contract for a service that communication with the client configuration data store. It contains a single `AddAsync` method.

```csharp
public interface IClientConfigurationStore
```

### Members

[Section titled "Members"](#members)

| name        | description                               |
| ----------- | ----------------------------------------- |
| AddAsync(...) | Adds a client to the configuration store. |

## ClientConfigurationStore

[Section titled "ClientConfigurationStore"](#clientconfigurationstore)

The `ClientConfigurationStore` is the default implementation of the `IClientConfigurationStore`. It uses Entity Framework to communicate with the client configuration store, and is intended to be used when IdentityServer is configured to use the Entity Framework based configuration stores.
