---
title: Duende IdentityServer v6.0 to v6.1
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-v60-to-v61/
source_type: llms-full-txt
content_hash: sha256:0311f4c646fa6adc1e6b3aa1e28640b27d783228002303b361ec96fa55b26901
category: identityserver
doc_id: identityserver/duende-identityserver-v60-to-v61
---

This upgrade guide covers upgrading from Duende IdentityServer v6.0 to v6.1 ([release notes](https://github.com/DuendeSoftware/products/releases/tag/is%2F6.1.0)).

## Step 1: Update NuGet package

[Section titled "Step 1: Update NuGet package"](#step-1-update-nuget-package)

In your IdentityServer host project, update the version of the NuGet. For example in your project file:

```xml
<PackageReference Include="Duende.IdentityServer" Version="6.0.0" />
```

would change to:

```xml
<PackageReference Include="Duende.IdentityServer" Version="6.1.0" />
```

## Step 2: Update Database Schema (if needed)

[Section titled "Step 2: Update Database Schema (if needed)"](#step-2-update-database-schema-if-needed)

If you are using a [database](/identityserver/data) for your configuration or operational data, then there is a database schema update. This includes:

* Server-side sessions feature, which requires a new table ([more details](https://github.com/DuendeSoftware/products/pull/743)).
* Session coordination feature, which adds a column to the Clients table ([more details](https://github.com/DuendeSoftware/products/pull/820)).
* Improve primary key on the persisted grants table ([more details](https://github.com/DuendeSoftware/products/pull/793)).

IdentityServer is abstracted from the data store on multiple levels, so the exact steps involved in updating your data store will depend on your implementation details.

#### Custom Store Implementations

[Section titled "Custom Store Implementations"](#custom-store-implementations)

The core of IdentityServer is written against the [store interfaces](/identityserver/reference/stores), which abstract all the implementation details of actually storing data. If your IdentityServer implementation includes a custom implementation of those stores, then you will have to determine how best to include the changes in the model in the underlying data store and make any necessary changes to schemas, if your data store requires that.

#### Duende.IdentityServer.EntityFramework

[Section titled "Duende.IdentityServer.EntityFramework"](#duendeidentityserverentityframework)

We also provide a default implementation of the stores in the `Duende.IdentityServer.EntityFramework` package, but this implementation is still highly abstracted because it is usable with any database that has an EF provider. Different database vendors have very different dialects of sql that have different syntax and type systems, so we don't provide schema changes directly. Instead, we provide the Entity Framework entities and mappings which can be used with Entity Framework's migrations feature to generate the schema updates that are needed in your database.

To generate migrations, run the commands below. Note that you might need to adjust paths based on your specific organization of the migration files.

Terminal

```bash
dotnet ef migrations add Update_DuendeIdentityServer_v6_1 -c ConfigurationDbContext -o Data/Migrations/IdentityServer/ConfigurationDb
dotnet ef migrations add Update_DuendeIdentityServer_v6_1 -c PersistedGrantDbContext -o Data/Migrations/IdentityServer/PersistedGrantDb
```

Then to apply those changes to your database:

Terminal

```bash
dotnet ef database update -c ConfigurationDbContext
dotnet ef database update -c PersistedGrantDbContext
```

Some organizations prefer to use other tools for managing schema changes. You're free to manage your schema however you see fit, as long as the entities can be successfully mapped. Even if you're not going to ultimately use Entity Framework migrations to manage your database changes, generating a migration can be a useful development step to get an idea of what needs to be done.

## Step 3: Done!

[Section titled "Step 3: Done!"](#step-3-done)

That's it. Of course, at this point you can and should test that your IdentityServer is updated and working properly.
