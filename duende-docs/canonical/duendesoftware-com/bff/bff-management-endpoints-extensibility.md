---
title: BFF Management Endpoints Extensibility
source_url: https://docs.duendesoftware.com/bff/bff-management-endpoints-extensibility/
source_type: llms-full-txt
content_hash: sha256:0a8fcfb6eecc6fb40e430f0dc9f4136fb22410ba171c1cf4c2976f42dea88151
last_fetched: '2025-12-16T19:17:18Z'
category: bff
doc_id: bff/bff-management-endpoints-extensibility
---

The behavior of each [management endpoint](/bff/fundamentals/session/management) is defined in a service. When you add Duende.BFF to the service container, a default implementation for every management endpoint gets registered.

You can add your own implementation by overriding the default after calling `AddBff()`.

* V4

  The following endpoints are registered in the service container:

  ```csharp
  // management endpoints
  builder.Services.AddTransient<ILoginEndpoint, DefaultLoginEndpoint>();
  builder.Services.AddTransient<ISilentLoginEndpoint, DefaultSilentLoginEndpoint>();
  builder.Services.AddTransient<ISilentLoginCallbackEndpoint, DefaultSilentLoginCallbackEndpoint>();
  builder.Services.AddTransient<ILogoutEndpoint, DefaultLogoutEndpoint>();
  builder.Services.AddTransient<IUserEndpoint, DefaultUserEndpoint>();
  builder.Services.AddTransient<IBackchannelLogoutEndpoint, DefaultBackchannelLogoutEndpoint>();
  builder.Services.AddTransient<IDiagnosticsEndpoint, DefaultDiagnosticsEndpoint>();
  ```

  The management endpoint services all inherit from the `IBffEndpoint`, which provides a general-purpose mechanism to add custom logic to the endpoints.

  IBffEndpoint.cs

  ```csharp
  public interface IBffEndpoint
  {
    Task ProcessRequestAsync(HttpContext context, CancellationToken ct);
  }
  ```

  You can customize the behavior of the endpoints by implementing the appropriate interface. The [default implementations](https://github.com/DuendeSoftware/products/tree/releases/bff/4.0.x/bff/src/Bff/Endpoints/Internal) can serve as a starting point for your own implementation.

  If you want to extend the default behavior of a management endpoint, you can add a custom endpoint and call the original endpoint implementation:

  Program.cs

  ```csharp
  var bffOptions = app.Services.GetRequiredService<IOptions<BffOptions>>().Value;


  app.MapGet(bffOptions.LoginPath, async (HttpContext context, CancellationToken ct) =>
  {
    // Custom logic before calling the original endpoint implementation
    var endpointProcessor = context.RequestServices.GetRequiredService<ILoginEndpoint>();
    await endpointProcessor.ProcessRequestAsync(context, ct);
    // Custom logic after calling the original endpoint implementation
  });
  ```

* V3

  ```csharp
  // management endpoints
  builder.Services.AddTransient<ILoginService, DefaultLoginService>();
  builder.Services.AddTransient<ISilentLoginService, DefaultSilentLoginService>();
  builder.Services.AddTransient<ISilentLoginCallbackService, DefaultSilentLoginCallbackService>();
  builder.Services.AddTransient<ILogoutService, DefaultLogoutService>();
  builder.Services.AddTransient<IUserService, DefaultUserService>();
  builder.Services.AddTransient<IBackchannelLogoutService, DefaultBackchannelLogoutService>();
  builder.Services.AddTransient<IDiagnosticsService, DefaultDiagnosticsService>();
  ```

  The management endpoint services all inherit from the `IBffEndpointService`, which provides a general-purpose mechanism to add custom logic to the endpoints.

  IBffEndpointService.cs

  ```csharp
  public interface IBffEndpointService
  {
    Task ProcessRequestAsync(HttpContext context);
  }
  ```

  You can customize the behavior of the endpoints either by implementing the appropriate interface or by extending the default implementation of that interface. In many cases, extending the default implementation is preferred, as this allows you to keep most of the default behavior by calling the base *ProcessRequestAsync* from your derived class.

  Several of the default endpoint service implementations also define virtual methods that can be overridden to customize their behavior with more granularity.
