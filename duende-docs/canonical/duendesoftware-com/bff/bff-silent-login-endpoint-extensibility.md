---
title: BFF Silent Login Endpoint Extensibility
source_url: https://docs.duendesoftware.com/bff/bff-silent-login-endpoint-extensibility/
source_type: llms-full-txt
content_hash: sha256:f8d412b9b83cb365cab9014aed4194422ae4cdbaba6c441506a8f258280fc2af
category: bff
doc_id: bff/bff-silent-login-endpoint-extensibility
---

The BFF silent login endpoint can be customized by implementing the `ISilentLoginEndpoint`.

Caution

In BFF V3, the `ISilentLoginEndpoint` interface is called `ISilentLoginService` instead.

Danger

The silent login endpoint has been marked as obsolete in BFF V4 and will be removed in a future version. To handle silent login in the future, pass the `prompt=none` parameter on to the login endpoint instead.

## Request Processing

[Section titled "Request Processing"](#request-processing)

* V4

  You can customize the behavior of the silent login endpoint by implementing the `ProcessRequestAsync` method of the `ISilentLoginEndpoint` interface. The [default implementation](https://github.com/DuendeSoftware/products/tree/releases/bff/4.0.x/bff/src/Bff/Endpoints/Internal/DefaultSilentLoginEndpoint.cs) can serve as a starting point for your own implementation.

  If you want to extend the default behavior of the silent login endpoint, you can instead add a custom endpoint and call the original endpoint implementation:

  Program.cs

  ```csharp
  var bffOptions = app.Services.GetRequiredService<IOptions<BffOptions>>().Value;


  app.MapGet(bffOptions.SilentLoginPath, async (HttpContext context, CancellationToken ct) =>
  {
    // Custom logic before calling the original endpoint implementation
    var endpointProcessor = context.RequestServices.GetRequiredService<ISilentLoginEndpoint>();
    await endpointProcessor.ProcessRequestAsync(context, ct);
    // Custom logic after calling the original endpoint implementation
  });
  ```

* V3

  `ProcessRequestAsync` is the top-level function called in the endpoint service `DefaultSilentLoginService`, and can be used to add arbitrary logic to the endpoint.

  For example, you could take whatever actions you need before normal processing of the request like this:

  ```csharp
  public override Task ProcessRequestAsync(HttpContext context, CancellationToken ct)
  {
    // Custom logic here


    return base.ProcessRequestAsync(context);
  }
  ```
