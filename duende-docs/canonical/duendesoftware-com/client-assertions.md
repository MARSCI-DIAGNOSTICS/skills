---
title: Client Assertions
source_url: https://docs.duendesoftware.com/accesstokenmanagement/advanced/client-assertions/
source_type: llms-full-txt
content_hash: sha256:fd7de28599f9b853b212f3806feb885a232ea86168ba4b55d307b9e01f8dea60
doc_id: client-assertions
---

> Learn how to use client assertions instead of shared secrets for token client authentication in Duende.AccessTokenManagement.

If your token client is using a client assertion instead of a shared secret, you can provide the assertion in two ways:

* Use the request parameter mechanism to pass a client assertion to the management
* Implement the `IClientAssertionService` interface to centralize client assertion creation

Here's a sample client assertion service using the Microsoft JWT library:

* V4

  ClientAssertionService.cs

  ```csharp
  using Duende.AccessTokenManagement;
  using Duende.IdentityModel;
  using Duende.IdentityModel.Client;
  using Microsoft.Extensions.Options;
  using Microsoft.IdentityModel.JsonWebTokens;
  using Microsoft.IdentityModel.Tokens;


  public class ClientAssertionService(IOptionsSnapshot<ClientCredentialsClient> options)
    : IClientAssertionService
  {
    public Task<ClientAssertion?> GetClientAssertionAsync(
    ClientCredentialsClientName? clientName = null, TokenRequestParameters? parameters = null)
    {
        if (clientName == "invoice")
        {
            var options1 = options.Get(clientName);


            var descriptor = new SecurityTokenDescriptor
            {
                Issuer = options1.ClientId!.ToString(),


                // Set the audience to the url of identity server. Do not use the tokenurl to build the autority.
                Audience = "https://--url-to-authority-here--",


                Expires = DateTime.UtcNow.AddMinutes(1),
                SigningCredentials = GetSigningCredential(),


                Claims = new Dictionary<string, object>
                {
                    { JwtClaimTypes.JwtId, Guid.NewGuid().ToString() },
                    { JwtClaimTypes.Subject, options.ClientId.ToString()! },
                    { JwtClaimTypes.IssuedAt, DateTimeOffset.UtcNow.ToUnixTimeSeconds() }
                },


                AdditionalHeaderClaims = new Dictionary<string, object>
                {
                    { JwtClaimTypes.TokenType, "client-authentication+jwt" }
                }
            };


            var handler = new JsonWebTokenHandler();
            var jwt = handler.CreateToken(descriptor);


            return Task.FromResult<ClientAssertion?>(new ClientAssertion
            {
                Type = OidcConstants.ClientAssertionTypes.JwtBearer,
                Value = jwt
            });
        }


        return Task.FromResult<ClientAssertion?>(null);
    }


    private SigningCredentials GetSigningCredential()
    {
        throw new NotImplementedException();
    }
  }
  ```

* V3

  ClientAssertionService.cs

  ```csharp
  using Duende.AccessTokenManagement;
  using Duende.IdentityModel;
  using Duende.IdentityModel.Client;
  using Microsoft.Extensions.Options;
  using Microsoft.IdentityModel.JsonWebTokens;
  using Microsoft.IdentityModel.Tokens;


  public class ClientAssertionService(IOptionsSnapshot<ClientCredentialsClient> options)
    : IClientAssertionService
  {
    public Task<ClientAssertion?> GetClientAssertionAsync(
    string? clientName = null, TokenRequestParameters? parameters = null)
    {
        if (clientName == "invoice")
        {
            var options1 = options.Get(clientName);


            var descriptor = new SecurityTokenDescriptor
            {
                Issuer = options1.ClientId,


                // Set the audience to the url of identity server. Do not use the tokenurl to build the autority.
                Audience = "https://--url-to-authority-here--",
                Expires = DateTime.UtcNow.AddMinutes(1),
                SigningCredentials = GetSigningCredential(),


                Claims = new Dictionary<string, object>
                {
                    { JwtClaimTypes.JwtId, Guid.NewGuid().ToString() },
                    { JwtClaimTypes.Subject, options1.ClientId! },
                    { JwtClaimTypes.IssuedAt, DateTime.UtcNow.ToEpochTime() }
                },


                AdditionalHeaderClaims = new Dictionary<string, object>
                {
                    { JwtClaimTypes.TokenType, "client-authentication+jwt" }
                }
            };


            var handler = new JsonWebTokenHandler();
            var jwt = handler.CreateToken(descriptor);


            return Task.FromResult<ClientAssertion?>(new ClientAssertion
            {
                Type = OidcConstants.ClientAssertionTypes.JwtBearer,
                Value = jwt
            });
        }


        return Task.FromResult<ClientAssertion?>(null);
    }


    private SigningCredentials GetSigningCredential()
    {
        throw new NotImplementedException();
    }
  }
  ```

Note

You need to explicitly set the `Audience` to the authorization server's issuer URL (usually the URL of identity server).

Don't set the audience to the `TokenUrl`. Setting the `Audience` value to the token endpoint leaves you vulnerable to these vulnerabilities: (CVE-2025-27370/CVE-2025-27371).
