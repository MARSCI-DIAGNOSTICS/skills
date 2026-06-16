---
title: Packaging and Builds
source_url: https://docs.duendesoftware.com/packaging-and-builds/
source_type: llms-full-txt
content_hash: sha256:68e67d56d3e9500e54b085e4a06b3729e1528b346eb1fd9c0068c84079b9990c
doc_id: packaging-and-builds
---

> A guide to Duende IdentityServer packages, templates, UI components, and source code accessibility

## Product

[Section titled "Product"](#product)

The licensed and supported libraries can be accessed via NuGet:

* [Duende IdentityServer](https://www.nuget.org/packages/Duende.IdentityServer)
* [Duende IdentityServer EntityFramework Integration](https://www.nuget.org/packages/Duende.IdentityServer.EntityFramework)
* [Duende IdentityServer ASP.NET Identity Integration](https://www.nuget.org/packages/Duende.IdentityServer.AspNetIdentity)

## Templates

[Section titled "Templates"](#templates)

Contains Duende templates for the `dotnet` CLI to help jump-start your Duende-powered solutions.

You can install the templates using the following command:

Terminal

```bash
dotnet new install Duende.Templates
```

[Templates ](https://www.nuget.org/packages/Duende.Templates)NuGet Package for IdentityServer Templates

[Source Code ](https://github.com/DuendeSoftware/IdentityServer.Templates)Source code for IdentityServer Templates

Running the command `dotnet new list duende` should give you a list of the following templates

```bash
Template Name                                               Short Name            Language  Tags
----------------------------------------------------------  --------------------  --------  -------------------------
Duende BFF Host using a Remote API                          duende-bff-remoteapi  [C#]      Web/Duende/BFF
Duende BFF using a Local API                                duende-bff-localapi   [C#]      Web/Duende/BFF
Duende BFF with Blazor autorender                           duende-bff-blazor     [C#]      Web/Duende/BFF
Duende IdentityServer Empty                                 duende-is-empty       [C#]      Web/Duende/IdentityServer
Duende IdentityServer Quickstart UI (UI assets only)        duende-is-ui          [C#]      Web/IdentityServer
Duende IdentityServer with ASP.NET Core Identity            duende-is-aspid       [C#]      Web/Duende/IdentityServer
Duende IdentityServer with Entity Framework Stores          duende-is-ef          [C#]      Web/Duende/IdentityServer
Duende IdentityServer with In-Memory Stores and Test Users  duende-is-inmem       [C#]      Web/Duende/IdentityServer
Duende IdentityServer                                       duende-is             [C#]      Web/Duende/IdentityServer
```

Note

You may have a previous version of Duende templates (`Duende.Templates`) installed on your machine. To uninstall the previous template package, and install the latest version, use the following command:

Terminal

```bash
dotnet new uninstall Duende.Templates
dotnet new install Duende.Templates
```

## Template Descriptions

[Section titled "Template Descriptions"](#template-descriptions)

In this section, we'll discuss what each IdentityServer template offers and why you would choose to start with it. While there are similarities across templates, there are nuances that can make for better starting points depending on your particular use case.

We'll start with the simplest templates and then move to the most feature-rich ones. Many of these templates build on each other's work, so moving from one to another is straightforward.

Note

All templates currently target .NET 8.0, but you can alter the target framework after creating the project to target higher framework versions.

All templates are provided as a starting point for your customization. Using the templates, you assume development responsibility for the choices, alterations, and inevitable deployment of your IdentityServer instance.

### Duende IdentityServer Empty

[Section titled "Duende IdentityServer Empty"](#duende-identityserver-empty)

You want to run the following command to start using the **Duende IdentityServer Empty** template.

```bash
dotnet new duende-is-empty
```

Once created, this template has three essential files: `Config`, `HostingExtensions`, and `Program`.

You can modify the `Config` file to add clients, scopes, and claims, as all configurations are from in-memory objects.

```csharp
public static class Config
{
    public static IEnumerable<IdentityResource> IdentityResources =>
        new IdentityResource[]
        {
            new IdentityResources.OpenId()
        };


    public static IEnumerable<ApiScope> ApiScopes =>
        new ApiScope[]
            { };


    public static IEnumerable<Client> Clients =>
        new Client[]
            { };
}
```

This template doesn't include user interface elements, so it doesn't support OpenID Connect unless you add those UI elements. You can do so by running the UI-only template of `duende-is-ui`.

```bash
dotnet new duende-is-ui --project <name of web app>
```

The executed command will add Razor Pages to your web project. You will need to add Razor Pages to your `HostingExtensions` file.

```csharp
using Serilog;


internal static class HostingExtensions
{
    public static WebApplication ConfigureServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddRazorPages();


        builder.Services.AddIdentityServer()
            .AddInMemoryIdentityResources(Config.IdentityResources)
            .AddInMemoryApiScopes(Config.ApiScopes)
            .AddInMemoryClients(Config.Clients)
            .AddLicenseSummary();


        return builder.Build();
    }


    public static WebApplication ConfigurePipeline(this WebApplication app)
    {
        app.UseSerilogRequestLogging();


        if (app.Environment.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }


        app.UseStaticFiles();
        app.UseRouting();


        app.UseIdentityServer();
        app.UseAuthorization();
        app.MapRazorPages().RequireAuthorization();


        return app;
    }
}
```

### Duende IdentityServer with In-Memory Stores and Test Users

[Section titled "Duende IdentityServer with In-Memory Stores and Test Users"](#duende-identityserver-with-in-memory-stores-and-test-users)

The `duende-is-inmem` template is similar to the `duende-is-empty` and `duende-is-ui` templates combined into a single project template.

```bash
dotnet new duende-is-inmem
```

This template differs from others in that we have defined some starting clients, scopes, and claims for common development scenarios and a speedier development experience.

Config.cs

```csharp
public static class Config
{
    public static IEnumerable<IdentityResource> IdentityResources =>
        new IdentityResource[]
        {
            new IdentityResources.OpenId(),
            new IdentityResources.Profile(),
        };


    public static IEnumerable<ApiScope> ApiScopes =>
        new ApiScope[]
        {
            new ApiScope("scope1"),
            new ApiScope("scope2"),
        };


    public static IEnumerable<Client> Clients =>
        new Client[]
        {
            // m2m client credentials flow client
            new Client
            {
                ClientId = "m2m.client",
                ClientName = "Client Credentials Client",


                AllowedGrantTypes = GrantTypes.ClientCredentials,
                ClientSecrets = { new Secret("511536EF-F270-4058-80CA-1C89C192F69A".Sha256()) },


                AllowedScopes = { "scope1" }
            },


            // interactive client using code flow + pkce
            new Client
            {
                ClientId = "interactive",
                ClientSecrets = { new Secret("49C1A7E1-0C79-4A89-A3D6-A37998FB86B0".Sha256()) },


                AllowedGrantTypes = GrantTypes.Code,


                RedirectUris = { "https://localhost:44300/signin-oidc" },
                FrontChannelLogoutUri = "https://localhost:44300/signout-oidc",
                PostLogoutRedirectUris = { "https://localhost:44300/signout-callback-oidc" },


                AllowOfflineAccess = true,
                AllowedScopes = { "openid", "profile", "scope2" }
            },
        };
}
```

This template is a great starting point for proof of concepts and a learning tool for developers experiencing OAuth 2.0 and OpenID Connect in the .NET space for the first time.

### Duende IdentityServer with Entity Framework Stores

[Section titled "Duende IdentityServer with Entity Framework Stores"](#duende-identityserver-with-entity-framework-stores)

For developers looking to quickly go to a production-like environment, starting with the `duende-is-ef` template is a great starting point.

```bash
dotnet new duende-is-ef
```

This template stores all operational and configuration data of the IdentityServer instance in your chosen data storage, utilizing EF Core's ability to target multiple database engines.

The template targets SQLite by default, but we have included scripts to easily swap out and regenerate migrations for your database.

[Read more about the Entity Framework Core setup here.](/identityserver/data/ef/)

### Duende IdentityServer

[Section titled "Duende IdentityServer"](#duende-identityserver)

The Duende IdentityServer template is our most feature-rich offering and a great starting point for developers who want a simple yet effective UI/UX experience.

```bash
dotnet new duende-is
```

The template is built on the Entity Framework Core template but provides an administrative UI for managing clients, scopes, and claims against a database storage engine. It also has a diagnostics dashboard showing system information, including the licensing tier and features currently used in your IdentityServer deployment.

#### Third-party Dependencies

[Section titled "Third-party Dependencies"](#third-party-dependencies)

This template includes several third-party dependencies:

* [Serilog](https://serilog.net/)
* [Bootstrap 5](https://getbootstrap.com)
* [Bootstrap 5 tags](https://github.com/lekoala/bootstrap5-tags)
* [JQuery](https://jquery.org)
* [Entity Framework Core](https://learn.microsoft.com/en-us/ef/core/)

### Duende IdentityServer with ASP.NET Core Identity

[Section titled "Duende IdentityServer with ASP.NET Core Identity"](#duende-identityserver-with-aspnet-core-identity)

The **Duende IdentityServer with ASP.NET Core Identity** template integrates with ASP.NET Identity to provide you with an instance of Duende IdentityServer that has a user store powered by the Microsoft library.

[Please read our ASP.NET Identity documentation](/identityserver/aspnet-identity/), to learn more about this integration.

### BFF Templates

[Section titled "BFF Templates"](#bff-templates)

For Duende BFF template description, refer the [Duende BFF project templates](/bff/getting-started/templates/).
