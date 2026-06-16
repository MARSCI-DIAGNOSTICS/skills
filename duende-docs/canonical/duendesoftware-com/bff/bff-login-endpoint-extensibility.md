---
title: BFF Login Endpoint Extensibility
source_url: https://docs.duendesoftware.com/bff/bff-login-endpoint-extensibility/
source_type: llms-full-txt
content_hash: sha256:ddbf500a66454066d5a771884ed43abed6876553fc916db8e4af9a310d4bf591
category: bff
doc_id: bff/bff-login-endpoint-extensibility
---

The BFF login endpoint has extensibility points in two interfaces. The `ILoginEndpoint` is the top-level abstraction that processes requests to the endpoint. This service can be used to add custom request processing logic. The `IReturnUrlValidator` ensures that the `returnUrl` parameter passed to the login endpoint is safe to use.

Caution

In BFF V3, the `ILoginEndpoint` interface is called `ILoginService` instead.

## Request Processing

[Section titled "Request Processing"](#request-processing)

* V4

  You can customize the behavior of the login endpoint by implementing the `ProcessRequestAsync` method of the `ILoginEndpoint` interface. The [default implementation](https://github.com/DuendeSoftware/products/tree/releases/bff/4.0.x/bff/src/Bff/Endpoints/Internal/DefaultLoginEndpoint.cs) can serve as a starting point for your own implementation.

  If you want to extend the default behavior of the login endpoint, you can instead add a custom endpoint and call the original endpoint implementation:

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

  `ProcessRequestAsync` is the top-level function called in the endpoint service `DefaultLoginService`, and can be used to add arbitrary logic to the endpoint.

  For example, you could take whatever actions you need before normal processing of the request like this:

  ```csharp
  public override Task ProcessRequestAsync(HttpContext context, CancellationToken ct)
  {
    // Custom logic here


    return base.ProcessRequestAsync(context);
  }
  ```

## Return URL Validation

[Section titled "Return URL Validation"](#return-url-validation)

To prevent open redirector attacks, the `returnUrl` parameter to the login endpoint must be validated. You can customize this validation by implementing the `IReturnUrlValidator` interface. The default implementation enforces that return URLs are local.
