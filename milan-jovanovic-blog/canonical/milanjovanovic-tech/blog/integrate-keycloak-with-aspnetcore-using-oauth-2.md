---
title: "Integrate Keycloak with ASP.NET Core Using OAuth 2.0"
slug: integrate-keycloak-with-aspnetcore-using-oauth-2
date: 2026-02-07
author: Milan Jovanovic
description: "Step-by-step guide to integrating Keycloak with ASP.NET Core using OAuth 2.0 Authorization Code flow with PKCE, configuring Swagger UI as an OAuth client, and implementing JWT validation."
tags:
  - aspnet-core
  - authentication
  - oauth
  - docker
source_url: https://www.milanjovanovic.tech/blog/integrate-keycloak-with-aspnetcore-using-oauth-2
doc_id: milanjovanovic-tech-blog-integrate-keycloak-with-aspnetcore-using-oauth-2
---

# Integrate Keycloak with ASP.NET Core Using OAuth 2.0

Authentication is one of those things that's easy to get wrong and expensive to fix later. Rather than building custom authentication systems, developers can leverage Keycloak, an open-source identity and access management solution that handles user authentication, authorization, and identity brokering out of the box.

This guide demonstrates integrating Keycloak with ASP.NET Core using OAuth 2.0, configuring Swagger UI as an OAuth client, and implementing JWT validation in a .NET backend.

## Running Keycloak as a Container

The quickest approach uses Docker. Create a `docker-compose.yml` file:

```yaml
services:
  keycloak:
    image: quay.io/keycloak/keycloak:26.5.2
    container_name: keycloak
    environment:
      - KC_BOOTSTRAP_ADMIN_USERNAME=admin
      - KC_BOOTSTRAP_ADMIN_PASSWORD=admin
    ports:
      - '8080:8080'
    command: start-dev
```

Start the container with `docker compose up -d`, then access the admin console at `http://localhost:8080` using credentials `admin`/`admin`.

## Setting Up a Realm and Client

### Creating a Realm

1. Click **Manage Realms** in the top-left corner
2. Click **Create realm**
3. Enter a name (e.g., `keycloak-demo`) and click **Create**

### Creating a Public Client

Since Swagger UI runs in the browser, create a public client without a client secret:

1. Go to **Clients** -> **Create client**
2. Set **Client ID** to `demo-api`
3. Leave **Client type** as `OpenID Connect`
4. Click **Next**
5. Disable **Client authentication** (public client)
6. Check **Standard flow** (Authorization Code)
7. Choose **PKCE Method**: S256 (SHA-256)
8. Click **Next**
9. Configure redirect URIs:
   - **Valid redirect URIs**: `https://localhost:5001/*`
   - **Web origins**: `https://localhost:5001`
10. Click **Save**

### Creating a Test User

1. Go to **Users** -> **Add user**
2. Fill in user details
3. Leave **Email Verified** checked
4. Click **Create**
5. Go to the **Credentials** tab
6. Click **Set password** and create a password (disable "Temporary")

## The Authorization Code Flow

The Authorization Code flow is the recommended OAuth 2.0 approach for browser-based applications. PKCE (Proof Key for Code Exchange) adds security by having clients generate a random secret (code verifier) and its hash (code challenge) sent during authorization.

The sequence involves:

1. User clicks "Authorize" in Swagger UI
2. Browser redirects to Keycloak's authorization endpoint
3. User logs in at Keycloak
4. Keycloak redirects back with an authorization code
5. Swagger UI exchanges the code for tokens
6. Swagger UI attaches the access token to API requests
7. API validates the token signature and claims

## Configuring Swagger UI with OAuth 2.0

Install Swashbuckle:

```bash
dotnet add package Swashbuckle.AspNetCore
```

Configure Swagger in `Program.cs`:

```csharp
var keycloakAuthority = builder.Configuration["Keycloak:Authority"]!;
var keycloakClientId = builder.Configuration["Keycloak:ClientId"]!;

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Demo API",
        Version = "v1"
    });

    // Define the OAuth 2.0 security scheme
    options.AddSecurityDefinition(nameof(SecuritySchemeType.OAuth2), new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.OAuth2,
        Flows = new OpenApiOAuthFlows
        {
            AuthorizationCode = new OpenApiOAuthFlow
            {
                AuthorizationUrl = new Uri($"{keycloakAuthority}/protocol/openid-connect/auth"),
                TokenUrl = new Uri($"{keycloakAuthority}/protocol/openid-connect/token"),
                Scopes = new Dictionary<string, string>
                {
                    { "openid", "OpenID Connect scope" },
                    { "profile", "User profile" }
                }
            }
        }
    });

    // Apply security to all operations
    options.AddSecurityRequirement(doc => new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecuritySchemeReference(nameof(SecuritySchemeType.OAuth2), doc),
            []
        }
    });
});
```

Configure Swagger UI middleware:

```csharp
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.OAuthClientId(keycloakClientId);
        options.OAuthUsePkce(); // Proof Key for Code Exchange
    });
}
```

Configuration in `appsettings.Development.json`:

```json
{
  "Keycloak": {
    "Authority": "http://localhost:8080/realms/keycloak-demo",
    "ClientId": "demo-api",
    "Audience": "account",
    "Issuer": "http://localhost:8080/realms/keycloak-demo",
    "MetadataAddress": "http://keycloak:8080/realms/keycloak-demo/.well-known/openid-configuration"
  }
}
```

## Adding JWT Validation

Install the JWT Bearer authentication package:

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

Configure authentication in `Program.cs`:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.MetadataAddress = builder.Configuration["Keycloak:MetadataAddress"]!;
        options.Audience = builder.Configuration["Keycloak:Audience"];

        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidIssuer = builder.Configuration["Keycloak:Issuer"]
        };

        options.RequireHttpsMetadata = !builder.Environment.IsDevelopment();
    });

builder.Services.AddAuthorization();
```

Add middleware:

```csharp
app.UseAuthentication();
app.UseAuthorization();
```

Create a protected endpoint:

```csharp
app.MapGet("users/me", (ClaimsPrincipal user) =>
{
    return Results.Ok(new
    {
        UserId = user.FindFirstValue(ClaimTypes.NameIdentifier),
        Email = user.FindFirstValue(ClaimTypes.Email),
        Name = user.FindFirstValue("preferred_username"),
        Claims = user.Claims.Select(c => new { c.Type, c.Value })
    });
})
.RequireAuthorization();
```

## How JWT Validation Works

When a request reaches a protected endpoint:

1. Middleware extracts the `Authorization: Bearer <token>` header
2. JWT Handler fetches Keycloak's public keys from the JWKS endpoint (cached)
3. Signature validation confirms the token wasn't tampered with
4. Claims are extracted and the `ClaimsPrincipal` is populated
5. Authorization middleware checks endpoint requirements
6. Endpoint executes with access to `HttpContext.User`

The API never contacts Keycloak to validate individual tokens; it fetches signing keys once and validates tokens locally, making JWT-based authentication very fast.

## Production Considerations

For production deployments:

**1. HTTPS Everywhere**: Run Keycloak behind HTTPS with TLS certificates configured.

**2. Persistent Storage**: Replace the embedded H2 database with PostgreSQL or MySQL:

```yaml
environment:
  - KC_DB=postgres
  - KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
  - KC_DB_USERNAME=keycloak
  - KC_DB_PASSWORD=secret
```

**3. Require HTTPS Metadata**: Remove `RequireHttpsMetadata = false` in production.

## Summary

This integration provides:

- A containerized Keycloak instance
- A realm with a public OAuth 2.0 client
- Swagger UI functioning as an OAuth client with Authorization Code + PKCE
- JWT validation in ASP.NET Core
- Observability with OpenTelemetry tracing

The modular design allows extending Keycloak for additional authentication mechanisms (Google login, enterprise SSO, SAML) without changing API code.
