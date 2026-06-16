---
title: Upgrading IdentityServer
source_url: https://docs.duendesoftware.com/identityserver/upgrading-identityserver/
source_type: llms-full-txt
content_hash: sha256:b4f4d929a0f0f3888b5f44c76bbcff15e92bea465137445a581a31f5a62648ed
category: identityserver
doc_id: identityserver/upgrading-identityserver
---

> Guide for upgrading between IdentityServer versions, including instructions for database migrations, breaking changes, and version-specific upgrade paths.

Upgrading to a new IdentityServer version is done by updating the NuGet package and handling any breaking changes. Some updates contain changes to the stores used by IdentityServer that requires database schema updates. If you are using our Entity Framework based stores we recommend using Entity Framework Migrations.

## Upgrading from version 7.4 to 8.0

[Section titled "Upgrading from version 7.4 to 8.0"](#upgrading-from-version-74-to-80)

Prerelease version

IdentityServer v8.0 is currently a prerelease version.

See [IdentityServer v7.4 to v8.0](/identityserver/upgrades/v7_4-to-v8_0/).

## Upgrading from version 7.3 to 7.4

[Section titled "Upgrading from version 7.3 to 7.4"](#upgrading-from-version-73-to-74)

See [IdentityServer v7.3 to v7.4](/identityserver/upgrades/v7_3-to-v7_4/).

## Upgrading from version 7.2 to 7.3

[Section titled "Upgrading from version 7.2 to 7.3"](#upgrading-from-version-72-to-73)

See [IdentityServer v7.2 to v7.3](/identityserver/upgrades/v7_2-to-v7_3/).

## Upgrading from version 7.1 to 7.2

[Section titled "Upgrading from version 7.1 to 7.2"](#upgrading-from-version-71-to-72)

See [IdentityServer v7.1 to v7.2](/identityserver/upgrades/v7_1-to-v7_2/).

## Upgrading from version 7.0 to 7.1

[Section titled "Upgrading from version 7.0 to 7.1"](#upgrading-from-version-70-to-71)

IdentityServer v7.1 includes support for **.NET 9** and many other smaller fixes and enhancements. There are no schema changes needed for IdentityServer 7.1. There are two changes that may require small code changes for a minority of users:

* *`IdentityModel`* package renamed to *`Duende.IdentityModel`* which may require code updates to referenced namespaces and types.
* `ClientConfigurationStore` now uses `IConfigurationDbContext`.

## Upgrading from version 6 to version 7

[Section titled "Upgrading from version 6 to version 7"](#upgrading-from-version-6-to-version-7)

We recommend upgrading incrementally through each minor version of the 6.x release before upgrading from 6.3 to 7.0. At each step, update the NuGet package, apply database schema changes (if any), and check for breaking changes that affect your implementation.

#### Upgrading from version 6.0

[Section titled "Upgrading from version 6.0"](#upgrading-from-version-60)

There are changes to the stores which requires database schema updates. If you use the Entity Framework based stores you need to apply the upgrade and database migrations from [6.0 - 6.1](/identityserver/upgrades/v6_0-to-v6_1/). Then continue with the [Upgrading from version 6.2](#upgrading-from-version-62) guide. If you are experienced with the Entity Framework Migrations Tooling you may also create a single migration from 6.0 to 7.0.

#### Upgrading from version 6.1

[Section titled "Upgrading from version 6.1"](#upgrading-from-version-61)

There no schema changes or other breaking changes between 6.1 and 6.2. Follow the [Upgrading from version 6.2](#upgrading-from-version-62) guide.

#### Upgrading from version 6.2

[Section titled "Upgrading from version 6.2"](#upgrading-from-version-62)

There are changes to the stores which requires database schema updates. If you use the Entity Framework based stores you need to apply the upgrade and database migrations from [6.2 - 6.3](/identityserver/upgrades/v6_2-to-v6_3/). If you are experienced with the Entity Framework Migrations Tooling you may also create a single migration from 6.2 to 7.0.

There were minor breaking changes in 6.3, most notably rotated refresh tokens are now deleted immediately on use by default. Review the [list in the upgrade guide](/identityserver/upgrades/v6_2-to-v6_3/#step-4-breaking-changes) to check if any of them affect your implementation.

Then continue with "Upgrading from version 6.3" below.

#### Upgrading from version 6.3

[Section titled "Upgrading from version 6.3"](#upgrading-from-version-63)

Follow the [upgrade guide version 6.3 - 7.0](/identityserver/upgrades/v6_3-to-v7_0/)

## Upgrading from IdentityServer4 to Duende IdentityServer

[Section titled "Upgrading from IdentityServer4 to Duende IdentityServer"](#upgrading-from-identityserver4-to-duende-identityserver)

See [IdentityServer4 to Duende IdentityServer](/identityserver/upgrades/identityserver4-to-duende-identityserver-v7/).
