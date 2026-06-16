---
title: Token Management
source_url: https://docs.duendesoftware.com/identityserver/token-management/
source_type: llms-full-txt
content_hash: sha256:57d90089f09fae947d2b0ec0fd6346339347d1cc70b27dc9facc8489531c7f94
category: identityserver
doc_id: identityserver/token-management
---

> Learn how to manage access tokens in interactive applications, including requesting refresh tokens, caching, and automatic token refresh using Duende.AccessTokenManagement.

Welcome to this Quickstart for Duende IdentityServer!

The previous quickstart introduced [API access](/identityserver/quickstarts/3-api-access/) with interactive applications, but by far the most complex task for a typical client is to manage the access token.

In addition to the written steps below a YouTube video is available:

[YouTube video player](https://www.youtube.com/embed/W8jtc2Ou1d4)

Given that the access token has a finite lifetime, you typically want to

* request a refresh token in addition to the access token at login time
* cache those tokens
* use the access token to call APIs until it expires
* use the refresh token to get a new access token
* repeat the process of caching and refreshing with the new token

ASP.NET Core has built-in facilities that can help you with some of those tasks (like caching or sessions), but there is still quite some work left to do. [Duende.AccessTokenManagement](/accesstokenmanagement) can help. It provides abstractions for storing tokens, automatic refresh of expired tokens, etc.

## Requesting A Refresh Token

[Section titled "Requesting A Refresh Token"](#requesting-a-refresh-token)

To allow the *web* client to request a refresh token set the *AllowOfflineAccess* property to true in the client configuration.

Update the *Client* in *src/IdentityServer/Config.cs* as follows:

```csharp
new Client
{
    ClientId = "web",
    ClientSecrets = { new Secret("secret".Sha256()) },


    AllowedGrantTypes = GrantTypes.Code,


    // where to redirect to after login
    RedirectUris = { "https://localhost:5002/signin-oidc" },


    // where to redirect to after logout
    PostLogoutRedirectUris = { "https://localhost:5002/signout-callback-oidc" },
    AllowOfflineAccess = true,


    AllowedScopes =
    {
        IdentityServerConstants.StandardScopes.OpenId,
        IdentityServerConstants.StandardScopes.Profile,
        "verification",
        "api1"
    }
}
```

To get the refresh token the *offline\_access* scope has to be requested by the client.

In *src/WebClient/Program.cs* add the scope to the scope list:

```csharp
options.Scope.Add("offline_access");
```

When running the solution the refresh token should now be visible under *Properties* on the landing page of the client.

## Automatically Refreshing An Access Token

[Section titled "Automatically Refreshing An Access Token"](#automatically-refreshing-an-access-token)

In the WebClient project add a reference to the NuGet package `Duende.AccessTokenManagement.OpenIdConnect` and in *Program.cs* add the needed types to dependency injection:

Program.cs

```csharp
builder.Services.AddOpenIdConnectAccessTokenManagement();
```

In *CallApi.cshtml.cs* update the method body of `OnGet` as follows:

CallApi.cshtml.cs

```csharp
public async Task OnGet()
{
    var tokenInfo = await HttpContext.GetUserAccessTokenAsync();
    var client = new HttpClient();
    client.SetBearerToken(tokenInfo.AccessToken!);


    var content = await client.GetStringAsync("https://localhost:6001/identity");


    var parsed = JsonDocument.Parse(content);
    var formatted = JsonSerializer.Serialize(parsed, new JsonSerializerOptions { WriteIndented = true });


    Json = formatted;
}
```

There are two changes here that utilize the AccessTokenManagement NuGet package:

* An object called tokenInfo containing all stored tokens is returned by the *GetUserAccessTokenAsync* extension method. This will make sure the access token is *automatically refreshed* using the refresh token if needed.
* The *SetBearerToken* extension method on HttpClient is used for convenience to place the access token in the needed HTTP header.

## Using A Named HttpClient

[Section titled "Using A Named HttpClient"](#using-a-named-httpclient)

On each call to OnGet in *CallApi.cshtml.cs* a new HttpClient is created in the code above. Recommended however is to use the [HttpClientFactory](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory) pattern so that instances can be reused.

`Duende.AccessTokenManagement.OpenIdConnect` builds on top of *HttpClientFactory* to create HttpClient instances that automatically retrieve the needed access token and refresh if needed.

In the client in *Program.cs* under the call to *AddOpenIdConnectAccessTokenManagement* register the HttpClient:

Program.cs

```csharp
builder.Services.AddUserAccessTokenHttpClient("apiClient", configureClient: client =>
{
    client.BaseAddress = new Uri("https://localhost:6001");
});
```

Now the *OnGet* method in *CallApi.cshtml.cs* can be even more straightforward:

```csharp
  public class CallApiModel(IHttpClientFactory httpClientFactory) : PageModel
  {
      public string Json = string.Empty;


      public async Task OnGet()
      {
          var client = httpClientFactory.CreateClient("apiClient");


          var content = await client.GetStringAsync("https://localhost:6001/identity");


          var parsed = JsonDocument.Parse(content);
          var formatted = JsonSerializer.Serialize(parsed, new JsonSerializerOptions { WriteIndented = true });


          Json = formatted;
      }
  }
```

Note that:

* The httpClientFactory is injected using a primary constructor. The type was registered when *AddOpenIdConnectAccessTokenManagement* was called in *Program.cs*.
* The client is created using the factory passing in the name of the client that was registered in *program.cs*.
* No additional code is needed. The client will automatically retrieve the access token and refresh it if needed.
