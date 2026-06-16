---
title: Multi Factor Authentication
source_url: https://docs.duendesoftware.com/identityserver/multi-factor-authentication/
source_type: llms-full-txt
content_hash: sha256:e01a7387ef75bc0d53266fdcddabd7f9af0852820dc919e13c84908098879bda
category: identityserver
doc_id: identityserver/multi-factor-authentication
---

> Overview of multi-factor authentication (MFA) implementation options in IdentityServer, including using ASP.NET Core capabilities in the hosting application or relying on upstream providers in federation scenarios.

Duende IdentityServer itself doesn't implement multi-factor authentication (MFA). MFA is part of the login process in the user interface which is the [responsibility of the hosting application](/identityserver/ui/). Microsoft provides some [general guidelines](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/mfa) on how to enable MFA in ASP.NET Core.

## MFA Hosted In IdentityServer

[Section titled "MFA Hosted In IdentityServer"](#mfa-hosted-in-identityserver)

An IdentityServer implementation can include MFA in its login page using anything that works with ASP.NET Core. One approach is to use [ASP.NET Identity](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity)'s [MFA support](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity-enable-qrcodes).

## MFA And External Authentication

[Section titled "MFA And External Authentication"](#mfa-and-external-authentication)

When using IdentityServer as a [federation gateway](/identityserver/ui/federation/), interactive users authenticate at the upstream provider. Typically, the upstream provider will perform the entire user authentication process, including any MFA required. There's no special configuration or implementation needed in IdentityServer in this case, as the upstream provider handles everything.
