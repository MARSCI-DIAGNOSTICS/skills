---
title: Conformance Report
source_url: https://docs.duendesoftware.com/identityserver/diagnostics/conformance-report/
source_type: llms-full-txt
content_hash: sha256:f1df3ea3079faf0293394c5df35eba38ee0bbd94b70e2312ceefa74c540afac2
doc_id: identityserver/diagnostics/conformance-report
---

> How to install, configure, and use the IdentityServer conformance report to assess OAuth 2.1 and FAPI 2.0 compliance.

Added in 8.0 (prerelease)

The conformance report assesses your IdentityServer deployment against [OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) and [FAPI 2.0 Security Profile](https://openid.net/specs/fapi-2_0-security-profile.html) specifications, generating an HTML report accessible via a protected endpoint.

## Installation

[Section titled "Installation"](#installation)

Install the NuGet package:

Terminal

```bash
dotnet add package Duende.IdentityServer.ConformanceReport --prerelease
```

## Setup

[Section titled "Setup"](#setup)

### 1. Register the Conformance Report

[Section titled "1. Register the Conformance Report"](#1-register-the-conformance-report)

Call `AddConformanceReport()` on the IdentityServer builder:

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddConformanceReport(options =>
    {
        options.Enabled = true;
    });
```

### 2. Map the Endpoint

[Section titled "2. Map the Endpoint"](#2-map-the-endpoint)

Add the conformance report endpoint to your middleware pipeline:

Program.cs

```csharp
app.MapConformanceReport();
```

### 3. Access the Report

[Section titled "3. Access the Report"](#3-access-the-report)

Navigate to: `https://your-server/_duende/conformance-report`

The endpoint requires an authenticated user by default (see [Authorization](#authorization) below).

## Configuration Options

[Section titled "Configuration Options"](#configuration-options)

`ConformanceReportOptions` controls the conformance report feature:

* **`Enabled`** Enable or disable the conformance report endpoint. Defaults to `false`.

* **`EnableOAuth21Assessment`** Include OAuth 2.1 profile assessment in the report. Defaults to `true`.

* **`EnableFapi2SecurityAssessment`** Include FAPI 2.0 Security Profile assessment in the report. Defaults to `true`.

* **`PathPrefix`** URL path prefix for the conformance endpoint (no leading slash). Defaults to `"_duende"`.

* **`ConfigureAuthorization`** Authorization policy for the HTML report endpoint. Defaults to require an authenticated user.

* **`AuthorizationPolicyName`** ASP.NET Core authorization policy name used internally. Defaults to `"ConformanceReport"`.

* **`HostCompanyName`** Optional company name shown in the report header. Defaults to `null`.

* **`HostCompanyLogoUrl`** Optional company logo URL shown in the report header. Defaults to `null`.

## Authorization

[Section titled "Authorization"](#authorization)

By default, the report endpoint requires an authenticated user. Customize the policy using `ConfigureAuthorization`:

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddConformanceReport(options =>
    {
        options.Enabled = true;


        // Require a specific role
        options.ConfigureAuthorization = policy => policy.RequireRole("Admin");


        // Or require multiple conditions
        // options.ConfigureAuthorization = policy => policy
        //     .RequireRole("Admin")
        //     .RequireClaim("department", "IT");


        // Or allow anonymous (development/testing only)
        // options.ConfigureAuthorization = policy =>
        //     policy.RequireAssertion(_ => builder.Environment.IsDevelopment());
    });
```

Caution

If you set `ConfigureAuthorization = null`, you must manually register an ASP.NET Core authorization policy with the name specified in `AuthorizationPolicyName` (default: `"ConformanceReport"`). Otherwise, the endpoint will fail at runtime with a "policy not found" error.

## Understanding the Report

[Section titled "Understanding the Report"](#understanding-the-report)

The HTML report displays:

* **Server Configuration** -- a matrix of server-level conformance rules and their status
* **Client Configurations** -- a matrix of per-client conformance rules and their status
* **Rule Legend** -- explanation of each rule identifier
* **Notes** -- detailed messages for warnings and failures

### Status Indicators

[Section titled "Status Indicators"](#status-indicators)

| Symbol  | Meaning                                                  |
| ------- | -------------------------------------------------------- |
| Pass    | Requirement is met                                       |
| Fail    | Requirement is not met (configuration is non-conformant) |
| Warning | Recommended practice is not followed                     |
| N/A     | Rule is not applicable to this configuration             |

## Requirements

[Section titled "Requirements"](#requirements)

The conformance report uses `IClientStore.GetAllClientsAsync` to enumerate all clients for assessment. Custom `IClientStore` implementations must implement this method (added in v8.0). See the [upgrade guide](/identityserver/upgrades/v7_4-to-v8_0/#iclientstoregetallclientsasync-now-required) for details.

## Full Example

[Section titled "Full Example"](#full-example)

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddInMemoryClients(Config.Clients)
    .AddConformanceReport(options =>
    {
        options.Enabled = true;
        options.EnableOAuth21Assessment = true;
        options.EnableFapi2SecurityAssessment = true;
        options.HostCompanyName = "Acme Corp";
        options.ConfigureAuthorization = policy => policy.RequireRole("ComplianceTeam");
    });


// ...


app.MapConformanceReport();
app.UseIdentityServer();
```
