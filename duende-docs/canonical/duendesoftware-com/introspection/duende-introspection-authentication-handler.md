---
title: Duende Introspection Authentication Handler
source_url: https://docs.duendesoftware.com/introspection/duende-introspection-authentication-handler/
source_type: llms-full-txt
content_hash: sha256:f93a3d2903cb8d85246f0b512a8d0798e20eee0461d029a082856b8348a14472
category: introspection
doc_id: introspection/duende-introspection-authentication-handler
---

> An ASP.NET Core authentication handler for OAuth 2.0 token introspection.

The `Duende.AspNetCore.Authentication.OAuth2Introspection` library implements an ASP.NET Core authentication handler for OAuth 2.0 token introspection, as defined in [RFC 7662](https://datatracker.ietf.org/doc/html/rfc7662), "OAuth 2.0 Token Introspection".

## Use Case

[Section titled "Use Case"](#use-case)

Using this library, you can request information about access tokens from an authorization server, allowing your ASP.NET Core application to validate tokens and retrieve metadata about them. This enables you to use opaque tokens in your application, where the token itself does not carry any information about the user or the scopes granted, but instead relies on the authorization server to provide this information.

Tip

By default, you can also use this library to introspect JWT tokens. You can disable this behavior by setting `SkipTokensWithDots = true` in the [`OAuth2IntrospectionOptions`](/introspection/options/).

## Features

[Section titled "Features"](#features)

* Implements the OAuth 2.0 token introspection protocol
* Supports both opaque and JWT access token introspection
* Supports caching of introspection results to reduce load on the authorization server
* Provides a customizable authentication handler for ASP.NET Core
* Integrates seamlessly with ASP.NET Core's authentication middleware

## Installation

[Section titled "Installation"](#installation)

If you want to use the `Duende.AspNetCore.Authentication.OAuth2Introspection` library, you need to add the NuGet package to your ASP.NET Core project.

You can achieve this by running the following command in your terminal:

```bash
dotnet package add Duende.AspNetCore.Authentication.OAuth2Introspection
```

## Configuration

[Section titled "Configuration"](#configuration)

To configure the OAuth 2.0 token introspection handler in your ASP.NET Core application, you need to add it to the authentication services in your `Startup.cs` or `Program.cs` file.

Here's an example on how to set it up:

Program.cs

```csharp
using Duende.AspNetCore.Authentication.OAuth2Introspection;


builder.Services.AddAuthentication(OAuth2IntrospectionDefaults.AuthenticationScheme)
    .AddOAuth2Introspection(options =>
    {
        // Replace with your authorization server's URL
        options.Authority = "https://demo.duendesoftware.com";


        options.ClientId = "client_id_for_introspection_endpoint";
        options.ClientSecret = "client_secret_for_introspection_endpoint";
    });
```

More details on the available options can be found on the [options page](/introspection/options/).

### Configuring the Backchannel HTTP Client

[Section titled "Configuring the Backchannel HTTP Client"](#configuring-the-backchannel-http-client)

You can configure the HTTP client used by the introspection handler to make requests to the introspection endpoint, for example, when your ASP.NET Core application lives behind a proxy or requires specific HTTP client settings.

Program.cs

```csharp
builder.Services.AddHttpClient(OAuth2IntrospectionDefaults.BackchannelHttpClientName)
    .AddHttpMessageHandler(() =>
    {
        // Configure client/handler for the back channel HTTP Client here
        return new HttpClientHandler
        {
            UseProxy = true,
            Proxy = new WebProxy(WebProxyUri, true)
        };
    });
```

## License and Feedback

[Section titled "License and Feedback"](#license-and-feedback)

`Duende.AspNetCore.Authentication.OAuth2Introspection` is released as open source under the [Apache 2.0 license](https://github.com/DuendeSoftware/foss/blob/main/LICENSE). Bug reports and contributions are welcome at [the GitHub repository](https://github.com/DuendeSoftware/foss).

[GitHub Repository ](https://github.com/DuendeSoftware/foss/tree/main/introspection)View the source code for this library on GitHub.

[NuGet Package ](https://www.nuget.org/packages/Duende.AspNetCore.Authentication.OAuth2Introspection)View the package on NuGet.org.
