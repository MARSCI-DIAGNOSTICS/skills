---
title: Server-Side Sessions
source_url: https://docs.duendesoftware.com/bff/fundamentals/session/server-side-sessions/
source_type: llms-full-txt
content_hash: sha256:9f4e1f0e527968238a507bd53ad0e254227abe91aa00dca6b64eafa06c5ba92d
doc_id: server-side-sessions
---

> Learn how to implement and configure server-side sessions in BFF to manage user session data storage and enable session revocation capabilities

By default, ASP.NET Core's cookie handler will store all user session data in a protected cookie. This works very well unless cookie size or revocation becomes an issue.

Duende.BFF includes all the plumbing to store your sessions server-side. The cookie will then only be used to transmit the session ID between the browser and the BFF host. This has the following advantages

* the cookie size will be very small and constant - regardless how much data (e.g. token or claims) is stored in the authentication session
* the session can be also revoked outside the context of a browser interaction, for example when receiving a back-channel logout notification from the upstream OpenID Connect provider

## Configuring Server-Side Sessions

[Section titled "Configuring Server-Side Sessions"](#configuring-server-side-sessions)

Server-side sessions can be enabled in the application's startup:

```csharp
builder.Services.AddBff()
    .AddServerSideSessions();
```

The default implementation stores the session in-memory. This is useful for testing, but for production you typically want a more robust storage mechanism. We provide an implementation of the session store built with EntityFramework (EF) that can be used with any database with an EF provider (e.g. Microsoft SQL Server). You can also use a custom store. See [extensibility](/bff/extensibility/sessions/#user-session-store) for more information.

## Using Entity Framework for the Server-Side Session Store

[Section titled "Using Entity Framework for the Server-Side Session Store"](#using-entity-framework-for-the-server-side-session-store)

To use the EF session store, install the `Duende.BFF.EntityFramework` NuGet package:

```bash
dotnet add package Duende.BFF.EntityFramework
```

Next, you can register the session store by calling `AddEntityFrameworkServerSideSessions`, like this:

```csharp
var cn = _configuration.GetConnectionString("db");


builder.Services.AddBff()
    .AddEntityFrameworkServerSideSessions(options=>
    {
        options.UseSqlServer(cn);
    });
```

The method of `AddEntityFrameworkServerSideSessions` registers the `SessionDbContext` along with a `UserSessionStore` as transient dependencies.

For developers looking to take advantage of DbContext pooling or have more fine-grained control over their DbContext creation registration and creation process, you can use the `AddEntityFrameworkServerSideSessionsServices` method instead. This method registers all the required services for server-side session except for the `SessionDbContext`, which will now be managed by the DbContext pooling mechanism.

```csharp
var cn = _configuration.GetConnectionString("db");


builder.Services.AddDbContextPool<SessionDbContext>(opt =>
{
    // configure your db context pool options here


    options.UseSqlServer(cn);
});


builder.Services.AddBff()
    .AddEntityFrameworkServerSideSessionsServices<SessionDbContext, IBffServicesBuilder>()
```

Note, you'll still need to let the server side session store know about the `SessionDbContext` by calling `AddEntityFrameworkServerSideSessions` with the `SessionDbContext` implementation as a generic argument.

### Entity Framework Migrations

[Section titled "Entity Framework Migrations"](#entity-framework-migrations)

Most data stores that you might use with Entity Framework use a schema to define the structure of their data. `Duende.BFF.EntityFramework` doesn't make any assumptions about the underlying datastore, how (or indeed even if) it defines its schema, or how schema changes are managed by your organization. For these reasons, Duende does not directly support database creation, schema changes, or data migration by publishing database scripts.

You are expected to manage your database in the way your organization sees fit. Using EF migrations is one possible approach to that, which Duende facilitates by publishing entity classes in each version of `Duende.BFF.EntityFramework`. An example project that uses those entities to create migrations is [here](https://github.com/DuendeSoftware/products/tree/main/bff/migrations/UserSessionDb).

To quickly create Entity Framework migrations, run the following command in the project directory that has access to Entity Framework Core's tools:

```bash
dotnet ef migrations add UserSessions -o Migrations -c SessionDbContext
```

The project must also reference the `Duende.BFF.EntityFramework` NuGet package and the `Microsoft.EntityFrameworkCore.Design` NuGet package, along with a specific database provider and its corresponding configuration, including the connection string.

## Session Store Cleanup

[Section titled "Session Store Cleanup"](#session-store-cleanup)

Added in v1.2.0.

Abandoned sessions will remain in the store unless something removes the stale entries.

* V4

  If you wish to have such sessions cleaned up periodically, then you can add the session cleanup host and configure the `SessionCleanupInterval` options:

  Program.cs

  ```csharp
  builder.Services.AddBff(options => {
        options.SessionCleanupInterval = TimeSpan.FromMinutes(5);
    })
    .AddServerSideSessions();
  ```

  This requires an implementation of [`IUserSessionStoreCleanup`](/bff/extensibility/sessions#user-session-store-cleanup) in the ASP.NET Core service provider.

  If using Entity Framework Core, then the `IUserSessionStoreCleanup` implementation is provided for you when you use `AddEntityFrameworkServerSideSessions`. You can then add the `SessionCleanupBackgroundProcess`:

  Program.cs

  ```csharp
  var cn = _configuration.GetConnectionString("db");


  builder.Services.AddBff()
    .AddEntityFrameworkServerSideSessions(options =>
    {
        options.UseSqlServer(cn);
    })
    .AddSessionCleanupBackgroundProcess();
  ```

  Note

  In V4, we changed how you enable session cleanup. We no longer automatically register the session cleanup hosted service. This has to be done manually. In a load-balanced environment, you can choose to run the cleanup job on all instances the BFF. However, you can also decide to spin up a separate host that's responsible for background jobs such as this cleanup job.

* V3

  If you wish to have such sessions cleaned up periodically, then you can configure the `EnableSessionCleanup` and `SessionCleanupInterval` options:

  Program.cs

  ```csharp
  builder.Services.AddBff(options => {
        options.EnableSessionCleanup = true;
        options.SessionCleanupInterval = TimeSpan.FromMinutes(5);
    })
    .AddServerSideSessions();
  ```

  This requires an implementation of [`IUserSessionStoreCleanup`](/bff/extensibility/sessions#user-session-store-cleanup) in the ASP.NET Core service provider.

  If using Entity Framework Core, then the `IUserSessionStoreCleanup` implementation is provided for you when you use `AddEntityFrameworkServerSideSessions`. Just enable session cleanup:

  Program.cs

  ```csharp
  var cn = _configuration.GetConnectionString("db");


  builder.Services.AddBff(options =>
    {
        options.EnableSessionCleanup = true;
    })
    .AddEntityFrameworkServerSideSessions(options =>
    {
        options.UseSqlServer(cn);
    });
  ```
