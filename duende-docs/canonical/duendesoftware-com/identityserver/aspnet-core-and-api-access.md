---
title: ASP.NET Core And API access
source_url: https://docs.duendesoftware.com/identityserver/aspnet-core-and-api-access/
source_type: llms-full-txt
content_hash: sha256:9a1063cbb3d3b43c8fcd3cc789466583d628b63e268bdc785df8e5dc69a801f0
category: identityserver
doc_id: identityserver/aspnet-core-and-api-access
---

> Learn how to combine user authentication with API access by requesting both identity and API scopes during the OpenID Connect login flow.

Welcome to Quickstart 3 for Duende IdentityServer!

The previous quickstarts introduced [API access](/identityserver/quickstarts/1-client-credentials/) and [user authentication](/identityserver/quickstarts/2-interactive/). This quickstart will bring the two together.

In addition to the written steps below a YouTube video is available:

[YouTube video player](https://www.youtube.com/embed/zHVmzgPUImc)

OpenID Connect and OAuth combine elegantly; you can achieve both user authentication and api access in a single exchange with the token service.

In Quickstart 2, the token request in the login process asked for only identity resources, that is, only scopes such as *profile* and *openid*. In this quickstart, you will add scopes for API resources to that request. *IdentityServer* will respond with two tokens:

1. the identity token, containing information about the authentication process and session, and
2. the access token, allowing access to APIs on behalf of the logged on user

Note

We recommend you do the quickstarts in order. If you'd like to start here, begin from a copy of the [reference implementation of Quickstart 2](https://github.com/DuendeSoftware/samples/tree/main/IdentityServer/v7/Quickstarts/2_InteractiveAspNetCore). Throughout this quickstart, paths are written relative to the base `_quickstart` directory created in part 1, which is the root directory of the reference implementation. You will also need to [install the IdentityServer templates](/identityserver/quickstarts/0-overview/#preparation).

## Modifying The Client Configuration

[Section titled "Modifying The Client Configuration"](#modifying-the-client-configuration)

The client configuration in IdentityServer requires one straightforward update. We should add the *api1* resource to the allowed scopes list so that the client will have permission to access it.

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


    AllowedScopes =
    {
        IdentityServerConstants.StandardScopes.OpenId,
        IdentityServerConstants.StandardScopes.Profile,
        "verification",
        "api1"
    }
}
```

## Modifying The Web client

[Section titled "Modifying The Web client"](#modifying-the-web-client)

Now configure the client to ask for access to api1 by requesting the *api1* scope. This is done in the OpenID Connect handler configuration in *src/WebClient/Program.cs*:

Program.cs

```csharp
builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = "Cookies";
    options.DefaultChallengeScheme = "oidc";
})
    .AddCookie("Cookies")
    .AddOpenIdConnect("oidc", options =>
    {
        options.Authority = "https://localhost:5001";


        options.ClientId = "web";
        options.ClientSecret = "secret";
        options.ResponseType = "code";


        options.Scope.Clear();
        options.Scope.Add("openid");
        options.Scope.Add("profile");
        options.Scope.Add("api1");
        options.Scope.Add("verification");
        options.ClaimActions.MapJsonKey("email_verified", "email_verified");
        options.GetClaimsFromUserInfoEndpoint = true;


        options.MapInboundClaims = false; // Don't rename claim types


        options.SaveTokens = true;
    });
```

Since *SaveTokens* is enabled, ASP.NET Core will automatically store the id and access tokens in the properties of the authentication cookie. If you run the solution and authenticate, you will see the tokens on the page that displays the cookie claims and properties created in quickstart 2.

## Using The Access Token

[Section titled "Using The Access Token"](#using-the-access-token)

Now you will use the access token to authorize requests from the *WebClient* to the *Api*.

Create a page that will

1. Retrieve the access token from the session using the *GetTokenAsync* method from *Microsoft.AspNetCore.Authentication*
2. Set the token in an *Authentication: Bearer* HTTP header
3. Make an HTTP request to the *API*
4. Display the results

Create the Page by running the following command from the *src/WebClient/Pages* directory:

```console
dotnet new page -n CallApi
```

Update *src/WebClient/Pages/CallApi.cshtml.cs* as follows:

```csharp
public class CallApiModel : PageModel
{
    public string Json = string.Empty;


    public async Task OnGet()
    {
        var accessToken = await HttpContext.GetTokenAsync("access_token");
        var client = new HttpClient();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);
        var content = await client.GetStringAsync("https://localhost:6001/identity");


        var parsed = JsonDocument.Parse(content);
        var formatted = JsonSerializer.Serialize(parsed, new JsonSerializerOptions { WriteIndented = true });


        Json = formatted;
    }
}
```

And update *src/WebClient/Pages/CallApi.cshtml* as follows:

```html
@page @model MyApp.Namespace.CallApiModel


<pre>@Model.Json</pre>
```

Also add a link to the new page in *src/WebClient/Shared/\_Layout.cshtml* with the following:

```html
<li class="nav-item">
    <a class="nav-link text-dark" asp-area="" asp-page="/CallApi">CallApi</a>
</li>
```

Make sure the *IdentityServer* and *Api* projects are running, start the *WebClient* and request */CallApi* after authentication.
