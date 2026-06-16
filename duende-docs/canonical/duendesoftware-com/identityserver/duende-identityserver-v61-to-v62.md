---
title: Duende IdentityServer v6.1 to v6.2
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-v61-to-v62/
source_type: llms-full-txt
content_hash: sha256:9b41db0dacdf1939bbbec322f6e2d7c25e52c9e63c5be194ae129d606233f393
category: identityserver
doc_id: identityserver/duende-identityserver-v61-to-v62
---

This upgrade guide covers upgrading from Duende IdentityServer v6.1 to v6.2 ([release notes](https://github.com/DuendeSoftware/products/releases/tag/is%2F6.2.0)).

Duende IdentityServer 6.2 adds:

* Support for .NET 7.0
* A new option that can help filter unhandled exceptions out of the logs
* Bug fixes and ongoing maintenance

There are no changes to the data stores in this release.

## Step 1: Update NuGet package

[Section titled "Step 1: Update NuGet package"](#step-1-update-nuget-package)

In your IdentityServer host project, update the version of the NuGet. For example in your project file:

```xml
<PackageReference Include="Duende.IdentityServer" Version="6.1.0" />
```

would change to:

```xml
<PackageReference Include="Duende.IdentityServer" Version="6.2.0" />
```

## Step 2: Verify Data Protection Configuration

[Section titled "Step 2: Verify Data Protection Configuration"](#step-2-verify-data-protection-configuration)

IdentityServer depends on ASP.NET Data Protection. Data Protection encrypts and signs data using keys managed by ASP.NET. Those keys are isolated by application name, which by default is set to the content root path of the host. This prevents multiple applications from sharing encryption keys, which is necessary to protect your encryption against certain forms of attack. However, this means that if your content root path changes, the default settings for data protection will prevent you from using your old keys. Beginning in .NET 6, the content root path was normalized so that it ends with a directory separator. In .NET 7 that change was reverted. This means that your content root path might change if you upgrade from .NET 6 to .NET 7. This can be mitigated by explicitly setting the application name and removing the separator character. See [Microsoft's documentation for more information](https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/configuration/overview?view=aspnetcore-7.0#setapplicationname).

## Step 3: Done!

[Section titled "Step 3: Done!"](#step-3-done)

That's it. Of course, at this point you can and should test that your IdentityServer is updated and working properly.
