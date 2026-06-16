---
title: ASP.NET Identity Integration
source_url: https://docs.duendesoftware.com/identityserver/aspnet-identity-integration/
source_type: llms-full-txt
content_hash: sha256:74dac67a702a7af3fc1842fb337d66562eb0f704deb7d0afefc6392abf661523
category: identityserver
doc_id: identityserver/aspnet-identity-integration
---

> A sample demonstrating how to integrate ASP.NET Identity with Duende IdentityServer using minimal code to create a working user management system with OIDC capabilities.

This section contains a collection of samples when building a Duende IdentityServer solution that uses [ASP.NET Identity](/identityserver/aspnet-identity/) for managing the identity database for users of IdentityServer.

### ASP.NET Identity

[Section titled "ASP.NET Identity"](#aspnet-identity)

This sample shows using ASP.NET Identity with Duende IdentityServer. The intent was to show the least amount of code needed to get a working sample that used Microsoft's ASP.NET Identity user management library.

The first step in creating the sample was to create a new project that used the ASP.NET Identity templates from Visual Studio (*"Individual Accounts"* for the authentication type). This provides all the out-of-the-box features from ASP.NET Identity for user management with only minor modifications, which are described below.

Then Duende IdentityServer was added to add OIDC/OAuth 2.0 capabilities to the application. Only the minimal configuration was done to get Duende IdentityServer functional for this sample.

Finally, another project was added which acts as a OIDC client application to exercise the OIDC login (and logout) capabilities.

The changes to the template in the ASP.NET Identity project (i.e. "IdentityServerAspNetIdentity"):

* Sqlite support was added, replacing the default of SqlServer.
* Duende IdentityServer was configured in `Startup.cs` with the necessary information about the client application, and the OIDC scopes it would be requesting.
* Debug level logging was enabled for the "Duende" prefix to allow viewing the logging emitted during request processing.
* In the middleware pipeline, `UseIdentityServer` replaced `UseAuthentication`.
* The logout page was scaffolded to allow modification (located in Areas/Identity/Pages/Account/Logout.cshtml). The default logout page from the template is unaware of OIDC single signout, so this feature was added.

In the client application:

* A simple ASP.NET Core Razor Web Application was used as the starting point.
* In `Startup.cs` the standard cookie and OIDC authentication configuration was added.
* A secure page (`Secure.cshtml`) that required an authenticated user will render the logged-in user's claim in the page.
* The index page (`Index.cshtml`) was modified to allow a POST to trigger OIDC logout.
* A logout button was added to trigger the POST.

[ASP.NET Identity Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/AspNetIdentity)GitHub Repository for the ASP.NET Identity Sample

### ASP.NET Identity Passkey .NET 10

[Section titled "ASP.NET Identity Passkey ".NET 10](#aspnet-identity-passkey)

This sample shows how to port passkey support from a .NET 10 Blazor App project template into Duende IdentityServer.

It is based on the [*Duende IdentityServer with ASP.NET Core Identity*](/identityserver/overview/packaging/#duende-identityserver-with-aspnet-core-identity) project template, and adds the necessary changes to support passkey authentication:

* In `HostingExtensions.cs`, the ASP.NET Identity schema is set to `IdentitySchemaVersions.Version3`.
* An Entity Framework Core migration is added to generate the `AspNetUserPasskeys` table in the database.
* The `Passkeys/PasskeyEndpointRouteBuilderExtensions.cs` file registers required minimal API endpoints for passkey creation and passkey request options. The extension method is called in `HostingExtensions.cs`.
* The `Passkeys/PasskeyOperation.cs`, `Passkeys/PasskeySubmitTagHelper.cs` and `wwwroot/js/passkey-submit.js`files define a tag helper and web component to handle passkey creation and authentication.
* `Pages/_ViewImports.cshtml` is updated to load the tag helper.
* The `Models/PasskeyInputModel.cs` file is added and used in the `/Login/InputModel.cs` model.
* The `Login/Index.cshtml` and `Login/Index.cshtml.cs` file include the necessary logic to handle passkey authentication.
* The `Pages/Account/Passkeys.cshtml`, `Pages/Account/Passkeys.cshtml.cs`,`Pages/Account/RenamePasskey.cshtml`, and `Pages/Account/RenamePasskey.cshtml.cs` files add functionality to register a passkey credential and rename a passkey.

[ASP.NET Identity Passkey Sample ](https://github.com/DuendeSoftware/samples/tree/main/IdentityServer/v7/AspNetIdentityPasskeys)GitHub Repository for the ASP.NET Identity Passkey Sample
