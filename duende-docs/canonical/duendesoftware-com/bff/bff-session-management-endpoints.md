---
title: BFF Session Management Endpoints
source_url: https://docs.duendesoftware.com/bff/bff-session-management-endpoints/
source_type: llms-full-txt
content_hash: sha256:2c9a09444bd6de2e74fb5eb2a68c1ed806d2fcd63c700e78ea1c622c1a842302
last_fetched: '2025-12-16T19:17:19Z'
category: bff
doc_id: bff/bff-session-management-endpoints
---

> Overview of Duende.BFF endpoints for session management operations including login, logout, and user information retrieval

Duende.BFF adds endpoints for performing typical session-management operations such as triggering login and logout and getting information about the currently logged-on user. These endpoint are meant to be called by the frontend.

In addition, Duende.BFF adds an implementation of the OpenID Connect back-channel notification endpoint to overcome the restrictions of third party cookies in front-channel notification in modern browsers.

You enable the endpoints by adding the relevant services into the ASP.NET Core service provider:

Program.cs

```csharp
// Add BFF services to DI - also add server-side session management
builder.Services.AddBff(options =>
{
    // default value
    options.ManagementBasePath = "/bff";
};
```

Starting with BFF v4, the BFF automatically wires up the management endpoints. If you disable this behavior (using `AutomaticallyRegisterBffMiddleware`, this is how you can map the management endpoints:

Program.cs

```csharp
var app = builder.Build();


// Preprocessing pipeline, which would have been automatically added to start of the request the pipeline.
app.UseBffPreProcessing();


// Your logic, such as:
app.UseRouting();
app.UseBff();


// post processing pipeline that would have been automatically added to the end of the request pipeline.
app.UseBffPostProcessing();


app.Run();
```

The *UsePreprocessing* method adds all handling for multiple frontend support. Alternatively, you can call these methods direct:

```csharp
app.UseBffFrontendSelection();
app.UseBffPathMapping();
app.UseBffOpenIdCallbacks();~
```

`UseBffPostProcessing` adds all BFF management endpoints and handlers for proxying `index.html`. You can also map each endpoint individually by calling the various `MapBffManagementXxxEndpoint` methods, for example `endpoints.MapBffManagementLoginEndpoint()`.

The following pages describe the default behavior of the management endpoints. See the [extensibility](/bff/extensibility) section for information about how to customize the behavior of the endpoints.

Note

In V3 and below, only the method `MapBffManagementEndpoints` exists.
