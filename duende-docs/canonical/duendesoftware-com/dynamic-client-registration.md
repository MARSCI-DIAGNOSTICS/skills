---
title: Dynamic Client Registration
source_url: https://docs.duendesoftware.com/dynamic-client-registration/
source_type: llms-full-txt
content_hash: sha256:33688bb11b9646965e6ffab8563e19823ded39bb67c02dcae47e14e3573cbe5f
doc_id: dynamic-client-registration
---

> Documentation for OpenID Connect Dynamic Client Registration library extension method for HttpClient that enables client registration and response handling

The client library for [OpenID Connect Dynamic Client Registration](https://openid.net/specs/openid-connect-registration-1_0.html) is provided as an extension method for [`System.Net.Http.HttpClient`](https://learn.microsoft.com/en-us/dotnet/api/system.net.http.httpclient).

The following code sends a registration request:

```csharp
var client = new HttpClient();


var response = await client.RegisterClientAsync(new DynamicClientRegistrationRequest
{
    Address = Endpoint,
    Document = new DynamicClientRegistrationDocument
    {
        RedirectUris = { redirectUri },
        ApplicationType = "native"
    }
});
```

Note

The `DynamicClientRegistrationDocument` class has strongly typed properties for all standard registration parameters as defines by the specification. If you want to add custom parameters, it is recommended to derive from this class and add your own properties.

The response is of type `RegistrationResponse` and has properties for the standard response parameters. You also have access to the raw response and to a parsed JSON document (via the `Raw` and `Json` properties).

Before using the response, you should always check the `IsError` property to make sure the request was successful:

```csharp
if (response.IsError) throw new Exception(response.Error);


var clientId = response.ClientId;
var secret = response.ClientSecret;
```
