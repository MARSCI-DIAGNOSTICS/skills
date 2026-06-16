---
title: Grant Validation Result
source_url: https://docs.duendesoftware.com/identityserver/reference/models/grant-validation-result/
source_type: llms-full-txt
content_hash: sha256:21de8b249c55794d17d948e5675e38a67969c777682ffee7a000b45543b1fc5f
category: identityserver
doc_id: identityserver/reference/models/grant-validation-result
---

> Reference documentation for the GrantValidationResult class which models the outcome of grant validation for extension grants and resource owner password grants in Duende IdentityServer.

## Duende.IdentityServer.Validation.GrantValidationResult

[Section titled "Duende.IdentityServer.Validation.GrantValidationResult"](#duendeidentityservervalidationgrantvalidationresult)

The `GrantValidationResult` class models the outcome of grant validation for [extensions grants](/identityserver/tokens/extension-grants/) and [resource owner password grants](/identityserver/tokens/password-grant/).

It models either a successful validation result with claims (e.g. subject ID) or an invalid result with an error code and message, e.g.:

```csharp
public class ExtensionGrantValidator : IExtensionGrantValidator
{
    public Task ValidateAsync(ExtensionGrantValidationContext context)
    {
        // some validation steps


        if (success)
        {
            context.Result = new GrantValidationResult(
                subject: "818727",
                authenticationMethod: "custom",
                claims: extraClaims);
        }
        else
        {
            // custom error message
            context.Result = new GrantValidationResult(
                TokenRequestErrors.InvalidGrant,
                "invalid custom credential");
        }


        return Task.CompletedTask;
    }
}
```

It also allows passing additional custom values that will be included in the token response, e.g.:

```csharp
context.Result = new GrantValidationResult(
    subject: "818727",
    authenticationMethod: "custom",
    customResponse: new Dictionary<string, object>
    {
        { "some_data", "some_value" }
    });
```

This will result in the following token response:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 360,
  "some_data": "some_value"
}
```
