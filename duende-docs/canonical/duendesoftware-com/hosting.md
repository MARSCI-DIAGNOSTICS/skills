---
title: Hosting
source_url: https://docs.duendesoftware.com/identityserver/fundamentals/hosting/
source_type: llms-full-txt
content_hash: sha256:3d6fcb66b945e6fa9294ed896d3473c653140918c274e89989fc3c56c10dedf0
doc_id: hosting
---

> Learn how to host and configure Duende IdentityServer in ASP.NET Core applications by adding services and middleware to the pipeline

You add the Duende IdentityServer engine to any ASP.NET Core application by adding the relevant services to the dependency injection (DI) system and adding the middleware to the processing pipeline.

Note

While technically you could share the ASP.NET Core host between Duende IdentityServer, clients or APIs, we recommend putting your IdentityServer into a separate application.

## Dependency Injection System

[Section titled "Dependency Injection System"](#dependency-injection-system)

You add the necessary services to the ASP.NET Core service provider by calling `AddIdentityServer` at application startup:

Program.cs

```csharp
var idsvrBuilder = builder.Services.AddIdentityServer(options =>
{
    // ...
});
```

Many of the fundamental configuration settings can be set on the options. See the [`IdentityServerOptions`](/identityserver/reference/options/) reference for more details.

The builder object has a number of extension methods to add additional services to the ASP.NET Core service provider. You can see the full list in the [reference](/identityserver/reference/di/) section, but very commonly you start by adding the configuration stores for clients and resources, e.g.:

Program.cs

```csharp
var idsvrBuilder = builder.Services.AddIdentityServer()
    .AddInMemoryClients(Config.Clients)
    .AddInMemoryIdentityResources(Config.IdentityResources)
    .AddInMemoryApiScopes(Config.ApiScopes)
```

The above is using the in-memory stores, but we also support EntityFramework-based implementations and custom stores. See [here](/identityserver/data) for more information.

Note

The `AddIdentityServer` extensions method also adds the required authentication services (it calls `AddAuthentication` internally). If you want to configure the authentication options, or be explicit about which services are registered, you can use the `AddAuthentication` (and `AddAuthorization`) extension method directly:

Program.cs

```csharp
builder.Services.AddAuthentication();
builder.Services.AddAuthorization();
```

## Request Pipeline

[Section titled "Request Pipeline"](#request-pipeline)

You need to add the Duende IdentityServer middleware to the pipeline by calling `UseIdentityServer`.

Since ordering is important in the pipeline, you typically want to put the IdentityServer middleware after the static files, but before the UI framework like MVC.

This would be a very typical minimal pipeline:

Program.cs

```csharp
var app = builder.Build();
app.UseStaticFiles();


app.UseRouting();
app.UseIdentityServer();
app.UseAuthorization();


app.MapDefaultControllerRoute();
```

Note

`UseIdentityServer` includes a call to `UseAuthentication`, so it's not necessary to have both.

However, IdentityServer does not include a call to `UseAuthorization`. You will need to add `UseAuthorization` (after `UseIdentityServer`/`UseAuthentication`) to include the authorization middleware into your pipeline. This will enable you to use various authorization features in your application.

If you use the Duende UI template and its various pages, the use of `UseAuthorization` is required.
