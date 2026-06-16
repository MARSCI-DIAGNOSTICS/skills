---
title: Getting Started - Multiple Frontends
source_url: https://docs.duendesoftware.com/getting-started-multiple-frontends/
source_type: llms-full-txt
content_hash: sha256:c35eaaba471c32395df20bf6eb41fc009059ac65b1b24640b926fcfde0338b40
doc_id: getting-started-multiple-frontends
---

> A guide on how to create a BFF application with multiple frontends.

Duende.BFF (Backend for Frontend) supports multiple frontends in a single BFF host. This is useful for scenarios where you want to serve several SPAs or frontend apps from the same backend, each with their own authentication and API proxying configuration.

Note

Multi-frontend support is available in Duende.BFF v4 and later. The v3-style of wiring up BFF is not supported for this scenario.

## Prerequisites

[Section titled "Prerequisites"](#prerequisites)

* .NET 8.0 or later
* Multiple frontend applications (e.g., React, Angular, Vue, or plain JavaScript)

## Setting Up A BFF Project For Multiple Frontends

[Section titled "Setting Up A BFF Project For Multiple Frontends"](#setting-up-a-bff-project-for-multiple-frontends)

### 1. Create A New ASP.NET Core Project

[Section titled "1. Create A New ASP.NET Core Project"](#1-create-a-new-aspnet-core-project)

Terminal

```bash
dotnet new web -n MyMultiBffApp
cd MyMultiBffApp
```

### 2. Add The Duende.BFF NuGet Package

[Section titled "2. Add The Duende.BFF NuGet Package"](#2-add-the-duendebff-nuget-package)

Terminal

```bash
dotnet add package Duende.BFF
```

### 3. OpenID Connect Configuration

[Section titled "3. OpenID Connect Configuration"](#3-openid-connect-configuration)

Configure OpenID Connect authentication for your BFF host. This is similar to the single frontend setup, but applies to all frontends unless overridden per frontend.

Program.cs

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

### 4. Configure BFF In `Program.cs`

[Section titled "4. Configure BFF In Program.cs"](#4-configure-bff-in-programcs)

* Static

  Register multiple frontends directly in code using `AddFrontends`:

  Program.cs

  ```csharp
  builder.Services.AddBff()
    .AddFrontends(
        new BffFrontend(BffFrontendName.Parse("default-frontend"))
            .WithCdnIndexHtmlUrl(new Uri("https://localhost:5005/static/index.html")),
        new BffFrontend(BffFrontendName.Parse("admin-frontend"))
            .WithCdnIndexHtmlUrl(new Uri("https://localhost:5005/admin/index.html"))
    );


  // ...existing code for authentication, authorization, etc.
  ```

* From Config

  You can also load frontend configuration from an `IConfiguration` source, such as a JSON file:

  Example `bffconfig.json`:

  ```json
  {
    "defaultOidcSettings": null,
    "defaultCookieSettings": null,
    "frontends": {
      "from_config": {
        "cdnIndexHtmlUrl": "https://localhost:5005/static/index.html",
        "matchingPath": "/from-config",
        "oidc": {
          "clientId": "bff.multi-frontend.config"
        },
        "remoteApis": [
          {
            "matchingPath": "/api/client-token",
            "targetUri": "https://localhost:5010",
            "tokenRequirement": "Client"
          }
        ]
      }
    }
  }
  ```

  Load and use the configuration in `Program.cs`:

  Program.cs

  ```csharp
  var bffConfig = new ConfigurationBuilder()
    .AddJsonFile("bffconfig.json")
    .Build();


  builder.Services.AddBff()
    .LoadConfiguration(bffConfig);


  // ...existing code for authentication, authorization, etc.
  ```

### 5. Remote API Proxying

[Section titled "5. Remote API Proxying"](#5-remote-api-proxying)

You can configure remote API proxying in two ways:

* **Single YARP proxy for all frontends:** You can set up a single YARP proxy for all frontends, as shown in the [Single Frontend Guide](/bff/getting-started/single-frontend/#5-adding-remote-apis).

* **Direct proxying per frontend:** You can configure remote APIs for each frontend individually:

  Program.cs

  ```csharp
  builder.Services.AddBff()
      .AddFrontends(
          new BffFrontend(BffFrontendName.Parse("default-frontend"))
              .WithCdnIndexUrl(new Uri("https://localhost:5005/static/index.html"))
              .WithRemoteApis(
                  new RemoteApi("/api/user-token", new Uri("https://localhost:5010"))
              )
      );
  ```

This allows each frontend to have its own set of proxied remote APIs.

### 6. Server Side Sessions

[Section titled "6. Server Side Sessions"](#6-server-side-sessions)

Server side session configuration is the same as in the single frontend scenario. See the [Single Frontend Guide](/bff/getting-started/single-frontend/#6-adding-server-side-sessions) for details.
