---
title: BFF Back-Channel Logout Endpoint Extensibility
source_url: https://docs.duendesoftware.com/bff/bff-back-channel-logout-endpoint-extensibility/
source_type: llms-full-txt
content_hash: sha256:b1312ea8b3aee266bb7f43ce0c348af1902af9a4661b42345ff8bba5c9791031
category: bff
doc_id: bff/bff-back-channel-logout-endpoint-extensibility
---

The back-channel logout endpoint has several extensibility points organized into two interfaces. The `IBackchannelLogoutEndpoint` is the top-level abstraction that processes requests to the endpoint. This service can be used to add custom request processing logic or to change how it validates incoming requests. When the back-channel logout endpoint receives a valid request, it revokes sessions using the `ISessionRevocationService`.

Caution

In BFF V3, the `IBackchannelLogoutEndpoint` interface is called `IBackchannelLogoutService` instead.

## Request Processing

[Section titled "Request Processing"](#request-processing)

* V4

  You can customize the behavior of the back-channel logout endpoint by implementing the `ProcessRequestAsync` method of the `IBackchannelLogoutEndpoint` interface. The [default implementation](https://github.com/DuendeSoftware/products/tree/releases/bff/4.0.x/bff/src/Bff/Endpoints/Internal/DefaultBackchannelLogoutEndpoint.cs) can serve as a starting point for your own implementation.

  If you want to extend the default behavior of the back-channel logout endpoint, you can instead add a custom endpoint and call the original endpoint implementation:

  Program.cs

  ```csharp
  var bffOptions = app.Services.GetRequiredService<IOptions<BffOptions>>().Value;


  app.MapGet(bffOptions.BackChannelLogoutPath, async (HttpContext context, CancellationToken ct) =>
  {
    // Custom logic before calling the original endpoint implementation
    var endpointProcessor = context.RequestServices.GetRequiredService<IBackchannelLogoutEndpoint>();
    await endpointProcessor.ProcessRequestAsync(context, ct);
    // Custom logic after calling the original endpoint implementation
  });
  ```

* V3

  `ProcessRequestAsync` is the top-level function called in the endpoint service `DefaultBackchannelLogoutService`, and can be used to add arbitrary logic to the endpoint.

  For example, you could take whatever actions you need before normal processing of the request like this:

  ```csharp
  public override Task ProcessRequestAsync(HttpContext context, CancellationToken ct)
  {
    // Custom logic here


    return base.ProcessRequestAsync(context);
  }
  ```

## Session Revocation

[Section titled "Session Revocation"](#session-revocation)

The back-channel logout service will call the registered session revocation service to revoke the user session when it receives a valid logout token. To customize the revocation process, implement the `ISessionRevocationService`.
