---
title: OIDC Client Logging
source_url: https://docs.duendesoftware.com/identitymodel-oidcclient/oidc-client-logging/
source_type: llms-full-txt
content_hash: sha256:e54ed4b2eda36adda7996c85531afb5831095efd0e904bf7aaf1458a4d0e0eb9
category: identitymodel-oidcclient
doc_id: identitymodel-oidcclient/oidc-client-logging
---

> Learn how to configure and customize logging in OidcClient using Microsoft.Extensions.Logging.ILogger

`OidcClient` logs errors, warnings, and diagnostic information using `Microsoft.Extensions.Logging.ILogger`, the standard .NET logging library.

You can use any logging provider to store your logs however you like, by setting the `LoggerFactory` property on `OidcClientOptions`:

Program.cs

```csharp
using Duende.IdentityModel;
using Duende.IdentityModel.OidcClient;


var builder = Host.CreateApplicationBuilder(args);


builder.Services.AddSingleton(svc =>
{
    var loggerFactory = svc.GetRequiredService<ILoggerFactory>();
    var options = new OidcClientOptions
    {
        Authority = "https://demo.duendesoftware.com",
        ClientId = "interactive.public",
        Scope = "openid profile email offline_access",
        RedirectUri = "app://localhost/",
        PostLogoutRedirectUri = "app://localhost/",
        LoggerFactory = loggerFactory
    };
    return new OidcClient(options);
});


var app = builder.Build();
var client = app.Services.GetService<OidcClient>();
```

Using this approach, you can use other logging frameworks, like [Serilog](https://github.com/serilog/serilog-extensions-hosting) for example.

For general information on how to configure logging in .NET applications, see our [Logging Fundamentals](/general/logging/) guide.

## Log Levels

[Section titled "Log Levels"](#log-levels)

The `OidcClient` logs at the following levels:

* `Trace`
* `Debug`
* `Information`
* `Error`

You can set the log level in your `appsettings.json` by modifying the following snippet.

appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "Duende.IdentityModel.OidcClient": "Error"
    }
  }
}
```
