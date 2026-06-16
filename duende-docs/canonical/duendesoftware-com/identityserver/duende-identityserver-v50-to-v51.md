---
title: Duende IdentityServer v5.0 to v5.1
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-v50-to-v51/
source_type: llms-full-txt
content_hash: sha256:60c6b46e081e027739b1ceccf4f3e458c61e483650955645480e1ccf09fab96d
category: identityserver
doc_id: identityserver/duende-identityserver-v50-to-v51
---

This upgrade guide covers upgrading from Duende IdentityServer v5.0 to v5.1 ([release notes](https://github.com/DuendeSoftware/products/releases/tag/is%2F5.1.0)). Fortunately there's not much to do :)

## Step 1: Update NuGet package

[Section titled "Step 1: Update NuGet package"](#step-1-update-nuget-package)

In your IdentityServer host project, update the version of the NuGet. For example in your project file:

```xml
<PackageReference Include="Duende.IdentityServer" Version="5.0.0" />
```

would change to:

```xml
<PackageReference Include="Duende.IdentityServer" Version="5.1.0" />
```

## Step 2: Update Database Schema (if needed)

[Section titled "Step 2: Update Database Schema (if needed)"](#step-2-update-database-schema-if-needed)

If you are using the `Duende.IdentityServer.EntityFramework` package as the implementation for the database for your operational data, then there is a small database schema update. This includes:

* A new index on the `ConsumedTime` column in the `PersistedGrants` table ([more details](https://github.com/DuendeSoftware/products/pull/84)).

If you're using EntityFramework Core migrations as the mechanism for managing schema changes over time, the commands below will update those migrations with the new changes. Note that you might need to adjust based on your specific organization of the migration files.

Terminal

```bash
dotnet ef migrations add Update_DuendeIdentityServer_v5_1 -c PersistedGrantDbContext -o Data/Migrations/IdentityServer/PersistedGrantDb
```

Then to apply those changes to your database:

Terminal

```bash
dotnet ef database update -c PersistedGrantDbContext
```

Some organizations prefer to use other tools for managing schema changes. You're free to manage your schema however you see fit, as long as the entities can be successfully mapped. Even if you're not going to ultimately use Entity Framework migrations to manage your database changes, generating a migration can be a useful development step to get an idea of what needs to be done.

## Step 3: Done!

[Section titled "Step 3: Done!"](#step-3-done)

That's it. Of course, at this point you can and should test that your IdentityServer is updated and working properly.
