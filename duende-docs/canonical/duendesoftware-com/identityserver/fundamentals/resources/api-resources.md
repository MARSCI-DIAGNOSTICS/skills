---
title: API Resources
source_url: https://docs.duendesoftware.com/identityserver/fundamentals/resources/api-resources/
source_type: llms-full-txt
content_hash: sha256:4f76207dd76a21c1355120d6a0942e59b9d05055857d3c1e5c46d7e677c2ed57
doc_id: identityserver/fundamentals/resources/api-resources
---

> Learn how API Resources in Duende IdentityServer help organize and group scopes, manage token claims, and control access token properties

When the API/resource surface gets larger, a flat list of scopes might become hard to manage.

In Duende IdentityServer, the `ApiResource` class allows for some additional organization and grouping and isolation of scopes and providing some common settings.

Let's use the following scope definition as an example:

```csharp
public static IEnumerable<ApiScope> GetApiScopes()
{
    return new List<ApiScope>
    {
        // invoice API specific scopes
        new ApiScope(name: "invoice.read",   displayName: "Reads your invoices."),
        new ApiScope(name: "invoice.pay",    displayName: "Pays your invoices."),


        // customer API specific scopes
        new ApiScope(name: "customer.read",    displayName: "Reads you customers information."),
        new ApiScope(name: "customer.contact", displayName: "Allows contacting one of your customers."),


        // shared scopes
        new ApiScope(name: "manage",    displayName: "Provides administrative access."),
        new ApiScope(name: "enumerate", displayName: "Allows enumerating data.")
    };
}
```

With `ApiResource` you can now create two logical APIs and their corresponding scopes:

```csharp
public static readonly IEnumerable<ApiResource> GetApiResources()
{
    return new List<ApiResource>
    {
        new ApiResource("invoice", "Invoice API")
        {
            Scopes = { "invoice.read", "invoice.pay", "manage", "enumerate" }
        },


        new ApiResource("customer", "Customer API")
        {
            Scopes = { "customer.read", "customer.contact", "manage", "enumerate" }
        }
    };
}
```

Using the API resource grouping gives you the following additional features

* support for the JWT `aud` claim. The value(s) of the audience claim will be the name of the API resource(s)
* support for adding common user claims across all contained scopes
* support for introspection by assigning an API secret to the resource
* support for configuring the access token signing algorithm for the resource

Let's have a look at some example access tokens for the above resource configuration.

Client requests: *`invoice.read`* and *`invoice.pay`*:

```json
    {
        "typ": "at+jwt"
    }.
    {
        "client_id": "client",
        "sub": "123",


        "aud": "invoice",
        "scope": "invoice.read invoice.pay"
    }
```

Client requests: *`invoice.read`* and *`customer.read`*:

```json
    {
        "typ": "at+jwt"
    }.
    {
        "client_id": "client",
        "sub": "123",


        "aud": [ "invoice", "customer" ],
        "scope": "invoice.read customer.read"
    }
```

Client requests: *`manage`*:

```json
    {
        "typ": "at+jwt"
    }.
    {
        "client_id": "client",
        "sub": "123",


        "aud": [ "invoice", "customer" ],
        "scope": "manage"
    }
```

### Adding User Claims

[Section titled "Adding User Claims"](#adding-user-claims)

You can specify that an access token for an API resource (regardless of which scope is requested) should contain additional user claims.

```csharp
var customerResource = new ApiResource("customer", "Customer API")
    {
        Scopes = { "customer.read", "customer.contact", "manage", "enumerate" },


        // additional claims to put into access token
        UserClaims =
        {
            "department_id",
            "sales_region"
        }
    }
```

If a client now requested a scope belonging to the `customer` resource, the access token would contain the additional claims (if provided by your [profile service](/identityserver/reference/services/profile-service/)).

```json
    {
        "typ": "at+jwt"
    }.
    {
        "client_id": "client",
        "sub": "123",


        "aud": [ "invoice", "customer" ],
        "scope": "invoice.read customer.read",


        "department_id": 5,
        "sales_region": "south"
    }
```

### Setting A Signing Algorithm

[Section titled "Setting A Signing Algorithm"](#setting-a-signing-algorithm)

Your APIs might have certain requirements for the cryptographic algorithm used to sign the access tokens for that resource. An example could be regulatory requirements, or that you are starting to migrate your system to higher security algorithms.

The following sample sets `PS256` as the required signing algorithm for the `invoices` API:

```csharp
var invoiceApi = new ApiResource("invoice", "Invoice API")
    {
        Scopes = { "invoice.read", "invoice.pay", "manage", "enumerate" },


        AllowedAccessTokenSigningAlgorithms = { SecurityAlgorithms.RsaSsaPssSha256 }
    }
```

Note

Make sure that you have configured your IdentityServer for the required signing algorithm. See [here](/identityserver/fundamentals/key-management/) for more details.

### Resource Isolation

[Section titled "Resource Isolation"](#resource-isolation)

See [Resource Isolation](/identityserver/fundamentals/resources/isolation/) for more details on how to use the `resource` parameter to request a token with scopes for a specific resource.
