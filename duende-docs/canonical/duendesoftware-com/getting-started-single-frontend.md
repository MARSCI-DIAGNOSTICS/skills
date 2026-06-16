---
title: Getting Started - Single Frontend
source_url: https://docs.duendesoftware.com/getting-started-single-frontend/
source_type: llms-full-txt
content_hash: sha256:db896629cc56497785fbb9c04660f027ff7b6cda8fe2367b1b5da25469bdd5d0
doc_id: getting-started-single-frontend
---

> A guide on how to create a BFF application with a single frontend.

Duende.BFF (Backend for Frontend) is a library that helps you build secure, modern web applications by acting as a security gateway between your frontend and backend APIs. This guide will walk you through setting up a simple BFF application with a single frontend.

Note

Duende.BFF V4 introduced a new way of configuring the BFF, which automatically configures the BFF using recommended practices. If you're upgrading from V3, please refer to the [upgrade guide](/bff/upgrading/bff-v3-to-v4/).

When in single frontend mode, an implicit default frontend is automatically registered. This ensures all the management routes and OpenID Connect-handling routes are available for your frontend.

When you call `.AddFrontend()` to add a new frontend, the system switches to multi-frontend mode. If you wish to have a default frontend in multi-frontend mode, you'll need to explicitly add it. See [multi-frontend support](/bff/fundamentals/multi-frontend/) for more information on this topic.

## Prerequisites

[Section titled "Prerequisites"](#prerequisites)

* .NET 8.0 or later
* A frontend application (e.g., React, Angular, Vue, or plain JavaScript)

## Setting Up A BFF project

[Section titled "Setting Up A BFF project"](#setting-up-a-bff-project)

### 1. Create A New ASP.NET Core Project

[Section titled "1. Create A New ASP.NET Core Project"](#1-create-a-new-aspnet-core-project)

Create a new ASP.NET Core Web Application:

```sh
dotnet new web -n MyBffApp
cd MyBffApp
```

### 2. Add The Duende.BFF NuGet Package

[Section titled "2. Add The Duende.BFF NuGet Package"](#2-add-the-duendebff-nuget-package)

Install the Duende.BFF package:

```sh
dotnet add package Duende.BFF
```

### 3. Configure BFF In `Program.cs`

[Section titled "3. Configure BFF In Program.cs"](#3-configure-bff-in-programcs)

Add the following to your `Program.cs`:

* Duende BFF v4

  ```csharp
  builder.Services.AddBff()
      .ConfigureOpenIdConnect(options =>
      {
          options.Authority = "https://demo.duendesoftware.com";
          options.ClientId = "interactive.confidential";
          options.ClientSecret = "secret";
          options.ResponseType = "code";
          options.ResponseMode = "query";


          options.GetClaimsFromUserInfoEndpoint = true;
          options.SaveTokens = true;
          options.MapInboundClaims = false;


          options.Scope.Clear();
          options.Scope.Add("openid");
          options.Scope.Add("profile");


          // Add this scope if you want to receive refresh tokens
          options.Scope.Add("offline_access");
      })
      .ConfigureCookies(options =>
      {
          // Because we use an identity server that's configured on a different site
          // (duendesoftware.com vs localhost), we need to configure the SameSite property to Lax.
          // Setting it to Strict would cause the authentication cookie not to be sent after logging in.
          // The user would have to refresh the page to get the cookie.
          // Recommendation: Set it to 'strict' if your IDP is on the same site as your BFF.
          options.Cookie.SameSite = SameSiteMode.Lax;
      });


  builder.Services.AddAuthorization();


  var app = builder.Build();


  app.UseAuthentication();
  app.UseRouting();


  // adds antiforgery protection for local APIs
  app.UseBff();


  // adds authorization for local and remote API endpoints
  app.UseAuthorization();


  app.Run();
  ```

* Duende BFF v3

  ```csharp
  builder.Services.AddBff();


  // Configure the authentication
  builder.Services
      .AddAuthentication(options =>
      {
          options.DefaultScheme = "cookie";
          options.DefaultChallengeScheme = "oidc";
          options.DefaultSignOutScheme = "oidc";
      })
      .AddCookie("cookie", options =>
      {
          // Configure the cookie with __Host prefix for maximum security
          options.Cookie.Name = "__Host-blazor";


          // Because we use an identity server that's configured on a different site
          // (duendesoftware.com vs localhost), we need to configure the SameSite property to Lax.
          // Setting it to Strict would cause the authentication cookie not to be sent after logging in.
          // The user would have to refresh the page to get the cookie.
          // Recommendation: Set it to 'strict' if your IDP is on the same site as your BFF.
          options.Cookie.SameSite = SameSiteMode.Lax;
      })
      .AddOpenIdConnect("oidc", options =>
      {
          options.Authority = "https://demo.duendesoftware.com";
          options.ClientId = "interactive.confidential";
          options.ClientSecret = "secret";
          options.ResponseType = "code";
          options.ResponseMode = "query";


          options.GetClaimsFromUserInfoEndpoint = true;
          options.SaveTokens = true;
          options.MapInboundClaims = false;


          options.Scope.Clear();
          options.Scope.Add("openid");
          options.Scope.Add("profile");


          // Add this scope if you want to receive refresh tokens
          options.Scope.Add("offline_access");
      });


  builder.Services.AddAuthorization();




  var app = builder.Build();


  app.UseAuthentication();
  app.UseRouting();


  // adds antiforgery protection for local APIs
  app.UseBff();


  // adds authorization for local and remote API endpoints
  app.UseAuthorization();


  // login, logout, user, backchannel logout...
  app.MapBffManagementEndpoints();


  app.Run();
  ```

Make sure to replace the Authority, ClientID and ClientSecret with values from your identity provider. Also consider if the scopes are correct.

### 4. Adding Local APIs

[Section titled "4. Adding Local APIs"](#4-adding-local-apis)

If your browser-based application uses local APIs, you can add those directly to your BFF app. The BFF supports both controllers and minimal APIs to create local API endpoints.

It's important to mark up the APIs with .AsBffApiEndpoint(), because this adds CSRF protection.

* Minimal Apis

  Program.cs

  ```csharp
  // Adds authorization for local and remote API endpoints
  app.UseAuthorization();


  // Place your custom routes after the 'UseAuthorization()'
  app.MapGet("/hello-world", () => "hello-world")
    .AsBffApiEndpoint(); // Adds CSRF protection to the controller endpoints
  ```

* Controllers

  Program.cs

  ```csharp
  builder.Services.AddControllers();


  // ...


  app.UseAuthorization();


  // When mapping the api controllers, place this after // UseAuthorization()
  app.MapControllers()
    .RequireAuthorization()
    .AsBffApiEndpoint(); // This statement adds CSRF protection to the controller endpoints
  ```

  LocalApiController.cs

  ```csharp
  [Route("hello")]
  public class LocalApiController : ControllerBase
  {
    [Route("world")]
    [HttpGet]
    public IActionResult SelfContained()
    {
        return Ok("hello world");
    }
  }
  ```

### 5. Adding Remote APIs

[Section titled "5. Adding Remote APIs"](#5-adding-remote-apis)

If you also want to call remote api's from your browser based application, then you should proxy the calls through the BFF.

The BFF extends the capabilities of [Yarp](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/getting-started?view=aspnetcore-9.0) in order to achieve this.

Terminal

```bash
dotnet add package Duende.BFF.Yarp
```

* Direct forwarding

  Program.cs

  ```csharp
  builder.Services.AddBff()
    .AddRemoteApis(); // Adds the capabilities needed to perform proxying to remote APIs.


  // ...


  // Map any call (including child routes) from /api/remote to https://remote-api-address
  app.MapRemoteBffApiEndpoint("/api/remote", new Uri("https://remote-api-address"))
    .WithAccessToken(RequiredTokenType.Client);
  ```

* Yarp

  Program.cs

  ```csharp
  builder.Services.AddBff()
    .AddRemoteApis() // This adds the capabilities needed to perform proxying to remote api's.
    .AddYarpConfig(new RouteConfig() // This statement configures yarp.
    {
        RouteId = "route_id",
        ClusterId = "cluster_id",


        Match = new RouteMatch
        {
            Path = $"api/remote/{{**catch-all}}"
        }
    }, new ClusterConfig()
    {
        ClusterId = "cluster_id",


        Destinations = new Dictionary<string, DestinationConfig>(StringComparer.OrdinalIgnoreCase)
        {
            { "destination_1", new DestinationConfig { Address = "https://remote-api-address" } }
        }
    });




  // ...


  app.UseAuthorization();


  // Add the Yarp middleware that will proxy the requests.
  app.MapReverseProxy(proxyApp => {
    proxyApp.UseAntiforgeryCheck();
  });
  ```

  You can also use an `IConfiguration` instead of programmatically configuring the proxy.

### 6. Adding Server-Side Sessions

[Section titled "6. Adding Server-Side Sessions"](#6-adding-server-side-sessions)

* In-Memory

  By default, Duende.BFF uses an in-memory session store. This is suitable for development and testing, but not recommended for production as sessions will be lost when the application restarts.

  Program.cs

  ```csharp
  builder.Services.AddBff()
    .AddServerSideSessions(); // Uses in-memory session store by default


  // ...existing code for authentication, authorization, etc.
  ```

* Entity Framework

  For production scenarios, you can use Entity Framework to persist sessions in a database. First, add the NuGet package:

  Terminal

  ```bash
  dotnet add package Duende.BFF.EntityFramework
  ```

  Then configure the session store in your `Program.cs`:

  Program.cs

  ```csharp
  builder.Services.AddBff()
    .AddServerSideSessions()
    .AddEntityFrameworkServerSideSessions(options =>
    {
        options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"));
    });


  // ...existing code for authentication, authorization, etc.
  ```

  You will also need to run the Entity Framework migrations to create the necessary tables.
