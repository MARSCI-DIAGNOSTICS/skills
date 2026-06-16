---
title: Clients
source_url: https://docs.duendesoftware.com/identityserver/samples/clients/
source_type: llms-full-txt
content_hash: sha256:25205c9ca7d22055da7f9f8402cc7819f9cbc9d922a242525d6dcbc178062ca0
category: identityserver
doc_id: identityserver/clients
---

> Learn about configuring and managing client applications that can request tokens from IdentityServer

[Clients](/identityserver/overview/terminology/#client) represent applications that can request tokens from your IdentityServer.

The details vary, but you typically define the following common settings for a client:

* a unique client ID
* a secret if needed
* the allowed interactions with the token service (called a grant type)
* a network location where identity and/or access token gets sent to (called a redirect URI)
* a list of scopes (aka resources) the client is allowed to access

## Defining A Client For Server To Server Communication

[Section titled "Defining A Client For Server To Server Communication"](#defining-a-client-for-server-to-server-communication)

In this scenario no interactive user is present - a service (i.e. the client) wants to communicate with an API (i.e. the resource that supports the scope):

```csharp
public class Clients
{
    public static IEnumerable<Client> Get()
    {
        return new List<Client>
        {
            new Client
            {
                ClientId = "service.client",
                ClientSecrets = { new Secret("secret".Sha256()) },


                AllowedGrantTypes = GrantTypes.ClientCredentials,
                AllowedScopes = { "api1", "api2.read_only" }
            }
        };
    }
}
```

## Defining An Interactive Application: Authentication And Delegated API Access

[Section titled "Defining An Interactive Application: Authentication And Delegated API Access"](#defining-an-interactive-application-authentication-and-delegated-api-access)

Interactive applications (e.g. web applications or native desktop/mobile applications) use the authorization code flow. This flow gives you the best security because the access tokens are transmitted via back-channel calls only (and gives you access to refresh tokens):

```csharp
var interactiveClient = new Client
{
    ClientId = "interactive",


    AllowedGrantTypes = GrantTypes.Code,
    AllowOfflineAccess = true,
    ClientSecrets = { new Secret("secret".Sha256()) },


    RedirectUris =           { "http://localhost:21402/signin-oidc" },
    PostLogoutRedirectUris = { "http://localhost:21402/" },
    FrontChannelLogoutUri =    "http://localhost:21402/signout-oidc",


    AllowedScopes =
    {
        IdentityServerConstants.StandardScopes.OpenId,
        IdentityServerConstants.StandardScopes.Profile,
        IdentityServerConstants.StandardScopes.Email,


        "api1", "api2.read_only"
    },
};
```

## Defining Clients In `appsettings.json`

[Section titled "Defining Clients In appsettings.json"](#defining-clients-in-appsettingsjson)

The `AddInMemoryClients` extensions method also supports adding clients from the ASP.NET Core configuration file. This allows you to define static clients directly from the appsettings.json file:

appsettings.json

```json
{
  "IdentityServer": {
    "Clients": [
      {
        "Enabled": true,
        "ClientId": "local-dev",
        "ClientName": "Local Development",
        "ClientSecrets": [
          {
            "Value": "<Insert Sha256 hash of the secret encoded as Base64 string>"
          }
        ],
        "AllowedGrantTypes": [
          "client_credentials"
        ],
        "AllowedScopes": [
          "api1"
        ]
      }
    ]
  }
}
```

Then pass the configuration section to the `AddInMemoryClients` method:

Program.cs

```csharp
AddInMemoryClients(configuration.GetSection("IdentityServer:Clients"))
```
