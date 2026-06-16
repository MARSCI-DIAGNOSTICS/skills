---
title: "A Practical Demo of Zero-Downtime Migrations Using Password Hashing"
slug: a-practical-demo-of-zero-downtime-migrations-using-password-hashing
date: 2026-01-24
author: Milan Jovanovic
description: "Demonstrates a migration-on-login pattern for upgrading password hashing algorithms (PBKDF2 to Argon2) without downtime, using .NET 8 Keyed Services for dual-algorithm verification with automatic re-hashing."
tags:
  - aspnet-core
  - authentication
  - clean-architecture
source_url: https://www.milanjovanovic.tech/blog/a-practical-demo-of-zero-downtime-migrations-using-password-hashing
doc_id: milanjovanovic-tech-blog-a-practical-demo-of-zero-downtime-migrations-using-password-hashing
---

# A Practical Demo of Zero-Downtime Migrations Using Password Hashing

## Overview

Security standards evolve constantly. Legacy password hashing algorithms like PBKDF2 eventually need upgrading to modern alternatives such as Argon2 or Bcrypt. However, hashing is a one-way operation - you cannot reverse existing hashes to upgrade them automatically.

Simply swapping implementations breaks authentication for all existing users. This article demonstrates a **migration-on-login pattern** that maintains service continuity while transitioning to newer algorithms.

## The Problem

A naive approach of replacing the old `IPasswordHasher` implementation immediately locks out the entire user base. Existing password hashes remain in the old format while the new hasher cannot verify them, returning `401 Unauthorized` errors.

## The Solution: Migration on Login

Rather than batch-migrating all data upfront, the strategy migrates users gradually as they authenticate:

1. **Attempt verification with the new algorithm first**
2. **If that fails, fall back to the legacy algorithm**
3. **Upon successful legacy verification, immediately re-hash using the new algorithm and persist the change**

Future logins for that user proceed normally through the standard path.

## Implementation Using .NET Keyed Services

.NET 8's Keyed Services enable registering multiple implementations with unique identifiers:

```csharp
builder.Services.AddKeyedSingleton<IPasswordHasher, Pbdkf2PasswordHasher>("legacy");
builder.Services.AddKeyedSingleton<IPasswordHasher, Argon2PasswordHasher>("modern");
builder.Services.AddSingleton<IPasswordHasher, Argon2PasswordHasher>();
```

The login handler injects both implementations via `[FromKeyedServices]` attributes and executes the dual-verification approach with automatic migration on successful legacy authentication.

## Production Considerations

**Algorithm Prefixes:** Employ standard prefix conventions (e.g., Bcrypt's `$2a$` or `$2b$`) to identify hash formats efficiently rather than relying on trial-and-error verification.

**Feature Flags:** Wrap migration logic behind feature flags to disable database writes during high-traffic periods while maintaining read-only fallback authentication.

## Completion

After several months, most active accounts migrate automatically. A cleanup script identifies remaining legacy hashes, forcing password resets for inactive accounts before removing legacy hasher registrations entirely.
