---
title: Duende IdentityServer v7.1 to v7.2
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-v71-to-v72/
source_type: llms-full-txt
content_hash: sha256:e1df924c7a32d09886d8bdbf7f48e29ad2b789cc7b06557090438a73e2b3f55d
category: identityserver
doc_id: identityserver/duende-identityserver-v71-to-v72
---

This upgrade guide covers upgrading from Duende IdentityServer v7.1 to v7.2 ([release notes](https://github.com/DuendeSoftware/products/releases/tag/is-7.2.0)).

Duende IdentityServer 7.2 adds:

* Do not issue `TokenIssuedFailureEvent` for `use_dpop_nonce` error
* Use `AsyncServiceScope` in Background Services
* Use query-safe URL fragment when returning an error
* Add an option for strict validation of assertion audiences
* General improvements to XML documentation and null reference exception handling
* Preview Features: Strict Audience Validation and Discovery Document Caching
* Bug fixes and ongoing maintenance

There are no changes to the data stores in this release.

## Step 1: Update NuGet package

[Section titled "Step 1: Update NuGet package"](#step-1-update-nuget-package)

In your IdentityServer host project, update the version of the NuGet. For example in your project file:

```xml
<PackageReference Include="Duende.IdentityServer" Version="7.1.0" />
```

would change to:

```xml
<PackageReference Include="Duende.IdentityServer" Version="7.2.0" />
```

## Step 2: Done!

[Section titled "Step 2: Done!"](#step-2-done)

That's it. Of course, at this point you can and should test that your IdentityServer is updated and working properly.
