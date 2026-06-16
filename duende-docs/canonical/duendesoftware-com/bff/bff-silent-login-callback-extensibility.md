---
title: BFF Silent Login Callback Extensibility
source_url: https://docs.duendesoftware.com/bff/bff-silent-login-callback-extensibility/
source_type: llms-full-txt
content_hash: sha256:0f610f8eea6a483059f9fc2943a59795f28a62ba486c59d5ec631a299d2e672b
category: bff
doc_id: bff/bff-silent-login-callback-extensibility
---

The BFF silent login callback endpoint can be customized by implementing the `ISilentLoginCallbackEndpoint`.

Caution

In BFF V3, the `ISilentLoginCallbackEndpoint` interface is called `ISilentLoginCallbackService` instead.

## Request Processing

[Section titled "Request Processing"](#request-processing)

* V4

  You can customize the behavior of the silent login callback endpoint by implementing the `ProcessRequestAsync` method of the `ISilentLoginCallbackEndpoint` interface. The [default implementation](https://github.com/DuendeSoftware/products/tree/releases/bff/4.0.x/bff/src/Bff/Endpoints/Internal/DefaultSilentLoginCallbackEndpoint.cs) can serve as a starting point for your own implementation.

  If you want to extend the default behavior of the silent login callback endpoint, you can instead add a custom endpoint and call the original endpoint implementation:

  Program.cs

  ```csharp
  var bffOptions = app.Services.GetRequiredService<IOptions<BffOptions>>().Value;


  app.MapGet(bffOptions.SilentLoginCallbackPath, async (HttpContext context, CancellationToken ct) =>
  {
    // Custom logic before calling the original endpoint implementation
    var endpointProcessor = context.RequestServices.GetRequiredService<ISilentLoginCallbackEndpoint>();
    await endpointProcessor.ProcessRequestAsync(context, ct);
    // Custom logic after calling the original endpoint implementation
  });
  ```

* V3

  `ProcessRequestAsync` is the top-level function called in the endpoint service `DefaultSilentLoginCallbackService`, and can be used to add arbitrary logic to the endpoint.

  For example, you could take whatever actions you need before normal processing of the request like this:

  ```csharp
  public override Task ProcessRequestAsync(HttpContext context, CancellationToken ct)
  {
    // Custom logic here


    return base.ProcessRequestAsync(context);
  }
  ```
