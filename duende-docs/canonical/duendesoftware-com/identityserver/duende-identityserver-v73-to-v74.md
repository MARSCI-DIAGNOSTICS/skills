---
title: Duende IdentityServer v7.3 to v7.4
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-v73-to-v74/
source_type: llms-full-txt
content_hash: sha256:10ab4ed66fbb8c1ae4a9821e1e6fbe7e49989735ef0b671d866e89e4e6748e48
category: identityserver
doc_id: identityserver/duende-identityserver-v73-to-v74
---

This upgrade guide covers upgrading from Duende IdentityServer v7.3 to v7.4 ([release notes](https://github.com/DuendeSoftware/products/releases/tag/is-7.4.0)).

IdentityServer 7.4 is a significant release that includes:

* Support for [.NET 10](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview)
* Support for OAuth 2.0 Authorization Server Metadata ([RFC 8414](https://www.rfc-editor.org/rfc/rfc8414.html))
* Add service for diagnostic data by [@josephdecock](https://github.com/josephdecock) in [#2252](https://github.com/DuendeSoftware/products/pull/2252)
* Trigger Back Channel Logout Earlier in Pipeline by [@bhazen](https://github.com/bhazen) in [#2258](https://github.com/DuendeSoftware/products/pull/2258)
* Enable Customizing ErrorMessage on Redirect to Error Page by [@bhazen](https://github.com/bhazen) in [#2263](https://github.com/DuendeSoftware/products/pull/2263)
* Better DCR Support for Public Clients by [@bhazen](https://github.com/bhazen) in [#2264](https://github.com/DuendeSoftware/products/pull/2264)
* New Callback option for path detection in Dynamic Providers
* Improved UI locales support
* Support for custom parameters in the Authorize Redirect Uri
* Identity package now persists session claims based on an interface
* Skipping front-channel logout iframe when unnecessary
* Set HTTP activity name on routing

There are no schema changes needed for IdentityServer 7.4. Small code changes may be required for some users to upgrade:

* Removed public unused class `Duende.IdentityServer.Models.DiscoveryDocument`
* Marked static properties referring to counters in `Telemetry.cs` as `readonly`

Note that `Duende.IdentityServer.EntityFramework.Storage` now depends on Entity Framework Core 9.x in the `net8.0` target framework, which should be fully supported on both .NET 8 and .NET 9. .NET 10 projects will use Entity Framework Core 10.x.

## Step 1: Update NuGet package

[Section titled "Step 1: Update NuGet package"](#step-1-update-nuget-package)

In your IdentityServer host project, update the version of the NuGet. For example, in your project file:

```xml
<PackageReference Include="Duende.IdentityServer" Version="7.3.0" />
```

would change to:

```xml
<PackageReference Include="Duende.IdentityServer" Version="7.4.7" />
```

## Step 2: Breaking Changes

[Section titled "Step 2: Breaking Changes"](#step-2-breaking-changes)

Small code changes may be required for some users to upgrade.

#### Removed public unused class `Duende.IdentityServer.Models.DiscoveryDocument`

[Section titled "Removed public unused class Duende.IdentityServer.Models.DiscoveryDocument"](#removed-public-unused-class-duendeidentityservermodelsdiscoverydocument)

In the process of internal code cleanup, we found that the `Duende.IdentityServer.Models.DiscoveryDocument` class was public but not used anywhere in the codebase.

If you were using this class in your codebase, you would need to replace it with your own implementation or use a different class that provides similar functionality. You can find the removed class in the [pull request](https://github.com/DuendeSoftware/products/pull/2128/files#diff-b9470315ba30a728f573d4fd52fae80da4f3f180b19d5e1b9b0bf3a9c7ce6841).

<https://github.com/DuendeSoftware/products/pull/2128>

#### Marked static properties referring to counters in `Telemetry.cs` as `readonly`

[Section titled "Marked static properties referring to counters in Telemetry.cs as readonly"](#marked-static-properties-referring-to-counters-in-telemetrycs-as-readonly)

In the process of internal code cleanup, these properties were updated to be marked as `readonly`. Code should not have been updating these properties as it would likely change the behavior of the telemetry emitted by IdentityServer.

Any code which was updating these properties should instead create its own counters for their specific scenario.

<https://github.com/DuendeSoftware/products/pull/2170>

## Step 3: Done!

[Section titled "Step 3: Done!"](#step-3-done)

That's it. Of course, at this point, you can and should test that your IdentityServer is updated and working properly.
