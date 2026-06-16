---
title: BFF Diagnostics Endpoint Extensibility
source_url: https://docs.duendesoftware.com/bff/bff-diagnostics-endpoint-extensibility/
source_type: llms-full-txt
content_hash: sha256:0d7c85a9eb2ae6d8c7e1b59c0a58746469b3aa9163bc8915d30bddac4ac145ce
category: bff
doc_id: bff/bff-diagnostics-endpoint-extensibility
---

The BFF diagnostics endpoint can be customized by implementing the `IDiagnosticsEndpoint`.

Caution

In BFF V3, the `IDiagnosticsEndpoint` interface is called `IDiagnosticsService` instead.

## Request Processing

[Section titled "Request Processing"](#request-processing)

* V4

  You can customize the behavior of the diagnostics endpoint by implementing the `ProcessRequestAsync` method of the `IDiagnosticsEndpoint` interface. The [default implementation](https://github.com/DuendeSoftware/products/tree/releases/bff/4.0.x/bff/src/Bff/Endpoints/Internal/DefaultDiagnosticsEndpoint.cs) can serve as a starting point for your own implementation.

  If you want to extend the default behavior of the diagnostics endpoint, you can instead add a custom endpoint and call the original endpoint implementation:

  Program.cs

  ```csharp
  var bffOptions = app.Services.GetRequiredService<IOptions<BffOptions>>().Value;


  app.MapGet(bffOptions.DiagnosticsPath, async (HttpContext context, CancellationToken ct) =>
  {
    // Custom logic before calling the original endpoint implementation
    var endpointProcessor = context.RequestServices.GetRequiredService<IDiagnosticsEndpoint>();
    await endpointProcessor.ProcessRequestAsync(context, ct);
    // Custom logic after calling the original endpoint implementation
  });
  ```

* V3

  `ProcessRequestAsync` is the top-level function called in the endpoint service `DefaultDiagnosticsService`, and can be used to add arbitrary logic to the endpoint.

  For example, you could take whatever actions you need before normal processing of the request like this:

  ```csharp
  public override Task ProcessRequestAsync(HttpContext context, CancellationToken ct)
  {
    // Custom logic here


    return base.ProcessRequestAsync(context);
  }
  ```
