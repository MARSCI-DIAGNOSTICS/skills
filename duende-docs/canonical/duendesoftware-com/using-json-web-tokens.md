---
title: Using JSON Web Tokens (JWTs)
source_url: https://docs.duendesoftware.com/using-json-web-tokens/
source_type: llms-full-txt
content_hash: sha256:09b6c5d3b3f54d74fc2c398b47b8a7e4a476be4a72e80149630b4273934af0a8
doc_id: using-json-web-tokens
---

> Guide for validating JWT bearer tokens in ASP.NET Core applications using the JWT authentication handler

On ASP.NET Core, you typically use the [JWT authentication handler](https://www.nuget.org/packages/Microsoft.AspNetCore.Authentication.JwtBearer) for validating JWT bearer tokens.

## Validating A JWT

[Section titled "Validating A JWT"](#validating-a-jwt)

First you need to add a reference to the authentication handler in your API project:

```xml
<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" />
```

If all you care about is making sure that an access token comes from your trusted IdentityServer, the following snippet shows the typical JWT validation configuration for ASP.NET Core:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        // base-address of your identityserver
        options.Authority = "https://demo.duendesoftware.com";


        // audience is optional, make sure you read the following paragraphs
        // to understand your options
        options.TokenValidationParameters.ValidateAudience = false;


        // it's recommended to check the type header to avoid "JWT confusion" attacks
        options.TokenValidationParameters.ValidTypes = new[] { "at+jwt" };
    });
```

## Adding Audience Validation

[Section titled "Adding Audience Validation"](#adding-audience-validation)

Simply making sure that the token is coming from a trusted issuer is not good enough for most cases. In more complex systems, you will have multiple resources and multiple clients. Not every client might be authorized to access every resource.

In OAuth there are two complementary mechanisms to embed more information about the "functionality" that the token is for - `audience` and `scope` (see [defining resources](/identityserver/fundamentals/resources/api-resources/) for more information).

If you designed your APIs around the concept of [API resources](/identityserver/fundamentals/resources/api-resources/), your IdentityServer will emit the `aud` claim by default (`api1` in this example):

```text
{
    "typ": "at+jwt",
    "kid": "123"
}.
{
    "aud": "api1",


    "client_id": "mobile_app",
    "sub": "123",
    "scope": "read write delete"
}
```

If you want to express in your API, that only access tokens for the `api1` audience (aka API resource name) are accepted, change the above code snippet to:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = "https://demo.duendesoftware.com";
        options.Audience = "api1";


        options.TokenValidationParameters.ValidTypes = new[] { "at+jwt" };
    });
```

Dynamic Proof-of-Possession (DPoP) validation

You can make use of the [JwtBearer Extensions](/identityserver/apis/aspnetcore/confirmation/#validating-dpop) to validate Dynamic Proof-of-Possession (DPoP) access tokens in ASP.NET Core.
