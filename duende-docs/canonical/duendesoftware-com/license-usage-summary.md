---
title: License Usage Summary
source_url: https://docs.duendesoftware.com/identityserver/reference/models/license-usage-summary/
source_type: llms-full-txt
content_hash: sha256:722bf7b0284a6de8808682f476d9f4e348d9bb202e7172bc5f9ebe181e1e1ad1
doc_id: license-usage-summary
---

> Reference documentation for the LicenseUsageSummary class which provides detailed information about clients, issuers, and features used in Duende IdentityServer for self-auditing and license compliance.

## Duende.IdentityServer.Licensing.LicenseUsageSummary

[Section titled "Duende.IdentityServer.Licensing.LicenseUsageSummary"](#duendeidentityserverlicensinglicenseusagesummary)

Added in 7.1

The `LicenseUsageSummary` class allows developers to get a detailed summary of clients, issuers, and features used during the lifetime of an active .NET application for self-auditing purposes.

* **`LicenseEdition`**

  Indicates the current IdentityServer instance's license edition.

* **`ClientsUsed`**

  A `string` collection of clients used with the current IdentityServer instance.

* **`IssuersUsed`**

  A `string` collection of issuers used with the current IdentityServer instance.

* **`FeaturesUsed`**

  A `string` collection of features has been used since the IdentityServer instance ran.

## Register LicenseUsageSummary Services

[Section titled "Register LicenseUsageSummary Services"](#register-licenseusagesummary-services)

To make the `LicenseUsageSummary` class available in your application, you'll need to make sure it is registered in the service collection at startup. You can do this by calling the `AddLicenseSummary()` extension method when registering IdentityServer:

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddLicenseSummary();
```

## Using LicenseUsageSummary with .NET Lifetime Events

[Section titled "Using LicenseUsageSummary with .NET Lifetime Events"](#using-licenseusagesummary-with-net-lifetime-events)

In .NET, an [`IHost`](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.ihostapplicationlifetime) implementation allows developers to subscribe to application lifetime events, including **Application Started**, **Application Stopped**, and **Application Stopping**. IdentityServer tracks usage metrics internally and that information may be accessed by developers at any time during the application's lifetime from the application's service collection using the following code snippet.

```csharp
// from a valid services scope
app.Services.GetRequiredService<LicenseUsageSummary>();
```

For self-auditing purposes, we recommend using the `IHost` lifetime event `ApplicationStopping` as shown in the example below.

Note, `LicenseUsageSummary` is *`read-only`*.

```csharp
app.Lifetime.ApplicationStopping.Register(() =>
{
  var usage = app.Services.GetRequiredService<LicenseUsageSummary>();
  // Todo: Substitue a different logging mechanism
  Console.Write(Summary(usage));
});
```

Developers may also use common dependency injection techniques such as property or constructor injection.

```csharp
// An ASP.NET Core MVC Controller
public class MyController : Controller
{
    public MyController(LicenseUsageSummary summary)
    {
        // use the summary information
    }
}
```

Developers can use the license usage summary to determine if their organization is within their current licensing tier or if they need to make adjustments to stay within compliance of [Duende licensing terms](https://duendesoftware.com/products/identityserver).
