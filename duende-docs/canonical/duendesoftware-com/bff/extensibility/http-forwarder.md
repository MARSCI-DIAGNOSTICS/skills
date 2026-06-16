---
title: HTTP Forwarder
source_url: https://docs.duendesoftware.com/bff/extensibility/http-forwarder/
source_type: llms-full-txt
content_hash: sha256:d4aa27f9373c346b7f3d576290bdfeaadbad5e63978e9ff1b12426c8e34d6717
doc_id: bff/extensibility/http-forwarder
---

> Learn how to customize the HTTP forwarding behavior in BFF by providing custom HTTP clients and request/response transformations

You can customize the HTTP forwarder behavior in two ways

* provide a customized HTTP client for outgoing calls
* provide custom request/response transformation

## Custom HTTP Clients

[Section titled "Custom HTTP Clients"](#custom-http-clients)

By default, Duende.BFF will create and cache an HTTP client per configured route or local path.

This invoker is set up like this:

```csharp
var client = new HttpMessageInvoker(new SocketsHttpHandler
{
    UseProxy = false,
    AllowAutoRedirect = false,
    AutomaticDecompression = DecompressionMethods.None,
    UseCookies = false
});
```

If you want to customize the HTTP client you can implement the `IForwarderHttpClientFactory` interface, e.g.:

```csharp
public class MyInvokerFactory : IForwarderHttpClientFactory
{
    public HttpMessageInvoker CreateClient(ForwarderHttpClientContext context)
    {
        return Clients.GetOrAdd(localPath, (key) =>
        {
            return new HttpMessageInvoker(new SocketsHttpHandler
            {
                // this API needs a proxy
                UseProxy = true,
                Proxy = new WebProxy("https://myproxy"),


                AllowAutoRedirect = false,
                AutomaticDecompression = DecompressionMethods.None,
                UseCookies = false
            });
        });
    }
}
```

...and override our registration:

```csharp
services.AddSingleton<IForwarderHttpClientFactory, MyInvokerFactory>();
```

## Custom Transformations When Using Direct Forwarding

[Section titled "Custom Transformations When Using Direct Forwarding"](#custom-transformations-when-using-direct-forwarding)

The method MapRemoteBffApiEndpoint uses default transformations that:

* removes the cookie header from the forwarded request
* removes local path from the forwarded request
* Adds the access token to the original request

If you wish to change or extend this behavior, you can do this for a single mapped endpoint or for all mapped API endpoints.

### Changing The Transformer For A Single Mapped Endpoint

[Section titled "Changing The Transformer For A Single Mapped Endpoint"](#changing-the-transformer-for-a-single-mapped-endpoint)

This code block shows an example of how you can extend the default transformers with an additional custom transform.

```csharp
app.MapRemoteBffApiEndpoint("/local", new Uri("https://target/"), context => {


    // If you want to extend the existing behavior, then you must call the default builder:
    DefaultBffYarpTransformerBuilders.DirectProxyWithAccessToken("/local", context);


    // You can also add custom transformers, such as this one that adds an additional header
    context.AddRequestHeader("custom", "with value");


});
```

The default transform builder performs these transforms:

```csharp
context.AddRequestHeaderRemove("Cookie");
context.AddPathRemovePrefix(localPath);
context.AddBffAccessToken(localPath);
```

For more information, also see the [YARP documentation on transforms](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/transforms?view=aspnetcore-9.0)

### Changing The Default Transformer

[Section titled "Changing The Default Transformer"](#changing-the-default-transformer)

You can change the default transformer builder delegate by registering one in the services collection:

```csharp
BffYarpTransformBuilder builder = (localPath, context) => {


    // If you want to extend the existing behavior, then you must call the default builder:
    DefaultBffYarpTransformerBuilders.DirectProxyWithAccessToken(localpath, context);


    // You can also add custom transformers, such as this one that adds an additional header
    context.AddResponseHeader("added-by-custom-default-transform", "some-value");


};


services.AddSingleton<BffYarpTransformBuilder>(builder);
```

## Changing The Forwarder Request Configuration

[Section titled "Changing The Forwarder Request Configuration"](#changing-the-forwarder-request-configuration)

You an also modify the forwarder request configuration, either globally or per mapped path. This can be useful if you want to tweak things like activity timeouts.

```csharp
// Register a forwarder config globally:
services.AddSingleton(new ForwarderRequestConfig()
{
    ActivityTimeout = TimeSpan.FromMilliseconds(100)
});


// Or modify one on a per mapped route basis:
app.MapRemoteBffApiEndpoint("/local", new Uri("https://target/"),
    requestConfig: new ForwarderRequestConfig()
    {
        // 100 ms timeout, which is not too short that the normal process might fail,
        // but not too long that the test will take forever
        ActivityTimeout = TimeSpan.FromMilliseconds(100)
    });
```
