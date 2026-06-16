---
title: Duende IdentityServer v7.0 to v7.1
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-v70-to-v71/
source_type: llms-full-txt
content_hash: sha256:9dc3cf7c37ee0ef001f9b5cbe249ffb1ba0cecba031a32ff949af45f2258c565
category: identityserver
doc_id: identityserver/duende-identityserver-v70-to-v71
---

IdentityServer v7.1 includes support for .NET 9 and many other smaller fixes and enhancements. Please see our [release notes](https://github.com/DuendeSoftware/products/releases/tag/is%2F7.1.0) for complete details.

There are no schema changes needed for IdentityServer 7.1. There are two changes that may require small code changes for a minority of users:

* IdentityModel renamed Duende.IdentityModel
* `ClientConfigurationStore` now uses IConfigurationDbContext

## Step 1: Target Framework Optional

[Section titled "Step 1: Target Framework "Optional](#step-1-target-framework)

IdentityServer 7.1 supports both .NET 8 and 9. If you wish, you can update your .NET version as part of this upgrade.

For example in your project file:

```xml
<TargetFramework>net8.0</TargetFramework>
```

would change to:

```xml
<TargetFramework>net9.0</TargetFramework>
```

Any NuGet packages that you are using that target an older version of .NET should also be updated. For example, the version of `Microsoft.EntityFrameworkCore.SqlServer` or `Microsoft.AspNetCore.Authentication.Google` should be updated. Depending on what your IdentityServer host project is using, there may or may not be code changes based on those updated dependencies.

## Step 2: NuGet Packages

[Section titled "Step 2: NuGet Packages"](#step-2-nuget-packages)

In your IdentityServer host project, update the version of the Duende.IdentityServer package. For example in your project file:

```xml
<PackageReference Include="Duende.IdentityServer" Version="7.0.8" />
```

would change to:

```xml
<PackageReference Include="Duende.IdentityServer" Version="7.1.0" />
```

## Step 3: Interface Change Breaking

[Section titled "Step 3: Interface Change "Breaking](#step-3-interface-change)

#### IdentityModel renamed Duende.IdentityModel

[Section titled "IdentityModel renamed Duende.IdentityModel"](#identitymodel-renamed-duendeidentitymodel)

Our open source IdentityModel library has been renamed Duende.IdentityModel, and we now depend on Duende.IdentityModel instead of IdentityModel. Duende.IdentityModel is a drop-in replacement for IdentityModel with updated namespaces that include the Duende prefix. If you are using IdentityModel's types in your IdentityServer implementation, you will need to update references from IdentityModel to Duende.IdentityModel (replace "using IdentityModel" with "using Duende.IdentityModel").\_

#### ClientConfigurationStore now uses IConfigurationDbContext

[Section titled "ClientConfigurationStore now uses IConfigurationDbContext"](#clientconfigurationstore-now-uses-iconfigurationdbcontext)

The `ClientConfigurationStore` in the `Duende.Configuration.EntityFramework` package now depends on `IConfigurationDbContext` instead of `ConfigurationDbContext` to allow for customization. If you have a customized store that derives from the default store, you may need to update your constructors. Note that this only affects the Entity Framework based implementation of the configuration store used by the dynamic client registration configuration API.

## Step 4: Done!

[Section titled "Step 4: Done!"](#step-4-done)

That's it. Of course, at this point you can and should test that your IdentityServer is updated and working properly.
