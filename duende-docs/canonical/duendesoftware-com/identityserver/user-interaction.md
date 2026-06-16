---
title: User Interaction
source_url: https://docs.duendesoftware.com/identityserver/user-interaction/
source_type: llms-full-txt
content_hash: sha256:d562973bea789bfdad7134fd98d9c568e7039df9de8d5b9054289bb3d948beb1
category: identityserver
doc_id: identityserver/user-interaction
---

> Samples demonstrating customization of IdentityServer's interactive pages, including custom profile services, step-up authentication, SPA-style login pages, dynamic identity providers, CIBA implementation, and Windows authentication integration.

These samples illustrate customization of the [interactive pages](/identityserver/ui) used in your Duende IdentityServer.

### Custom Profile Service

[Section titled "Custom Profile Service"](#custom-profile-service)

This sample shows how to create a [custom profile service](/identityserver/fundamentals/claims/) to control what claims are issued from your IdentityServer. The majority of the sample is captured in `CustomProfileService.cs` in the `IdentityServer` project.

Also, another part of the sample shows how to collect a custom claim during the login workflow when using an external login provider (this is done in the `ExternalLogin/Callback.cshtml.cs` processing logic). This claim value is then stored in the user's session, and is then ultimately copied into the created tokens via the custom profile service logic.

[Custom Profile Service Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/ProfileService)GitHub Repository for the Custom Profile Service Sample

### Step Up

[Section titled "Step Up"](#step-up)

This sample shows how to implement [step up](https://datatracker.ietf.org/doc/draft-ietf-oauth-step-up-authn-challenge/). It consists of three projects:

* IdentityServerHost is a token server implemented with Duende IdentityServer.
* Api is a protected resource that uses the IdentityServerHost as its authority and can make Step-Up responses when requests don't meet its authentication requirements.
* Client is a client application that uses IdentityServerHost to login and makes requests to the Api.

To run the demo, start all three projects and navigate to the Client application at `https://localhost:6001`. From there, you can click on links to pages that will trigger step up in various ways. For example, you could

* Click on the secure page to trigger login.
* Authenticate with user alice, password alice.
* Note that alice does not require MFA to log in.
* Click on the MFA page to make an API request that requires MFA.
* This will trigger step up for Alice, who should be shown a fake MFA page at IdentityServer before returning to the Client application.
* Finally, click on the Recent Auth page to make an API request that requires an authentication in the past minute. The page will show the age of the authentication.
* It may be necessary to refresh the page after a minute has passed to trigger step up.

From there, you can experiment with other interactions. You can go to the Recent Auth with MFA page that has both authentication requirements, or try the user bob, who always requires MFA.

[Step Up Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/StepUp)GitHub Repository for the Step Up Sample

### SPA-style Login Page

[Section titled "SPA-style Login Page"](#spa-style-login-page)

This sample shows an example of building the interactive pages (login, consent, logout, and error) as client-rendered ( typical of SPAs), rather than server-rendered. Since there are many different SPA frameworks, the actual pages are coded using vanilla JavaScript.

Key takeaways:

* how to handle the necessary request parameters
* how to contact the backend of IdentityServer to implement the various workflows (login, logout, etc.)
* how to implement a backend to support the frontend pages

[SPA-style Login Page Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/SpaLoginUi)GitHub Repository for the SPA-style Login Page Sample

### Dynamic Providers

[Section titled "Dynamic Providers"](#dynamic-providers)

The [dynamic providers](/identityserver/ui/login/dynamicproviders/) feature allows for loading OpenID Connect identity provider configuration dynamically from a store. This sample sets up a simple database with one dynamic OIDC provider.

Some key points about the `IdentityServer` project in the sample:

* Execute the command "dotnet run /seed" to create and populate the Sqlite database.
* `SeedData.cs` has the code to populate the dynamic provider in the database.
* In the `Account/Login/Index.cshtml.cs` file, the code to build the UI to list the dynamic providers is in the `BuildModelAsync` helper. It uses the `IIdentityProviderStore` to query the dynamic provider database.

[Dynamic Providers Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/DynamicProviders)GitHub Repository for the Dynamic Providers Sample

### Adding Other Protocol Types To Dynamic Providers

[Section titled "Adding Other Protocol Types To Dynamic Providers"](#adding-other-protocol-types-to-dynamic-providers)

The [dynamic providers](/identityserver/ui/login/dynamicproviders/) feature allows for loading OpenID Connect identity provider configuration dynamically from a store. This sample shows how to extend the dynamic providers feature to support additional protocol types, and specifically WS-Federation.

Key takeaways:

* how to define a custom identity provider model
* how to map from the custom identity provider model to the protocol options
* how to register the custom protocol type with IdentityServer
* how to register the custom protocol type with IdentityServer
* how to use the existing provider store to persist custom provider model data

[Adding Other Protocol Types To Dynamic Providers Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/WsFederationDynamicProviders)Adding Other Protocol Types To Dynamic Providers Sample

### Using Sustainsys.Saml2 With Dynamic Providers

[Section titled "Using Sustainsys.Saml2 With Dynamic Providers"](#using-sustainsyssaml2-with-dynamic-providers)

The [Sustainsys.Saml2](https://saml2.sustainsys.com) open source library adds Saml2 protocol support to ASP.NET Core. It can be used together with the Duende dynamic identity providers feature.

The sample is minimalistic to show a simple Saml2 config and does not handle the complete set of Saml2 config options.

[Using Sustainsys.Saml2 With Dynamic Providers Sample ](https://github.com/Sustainsys/Saml2.Samples/tree/main/v2/DuendeDynamicProviders)GitHub Repository for the Using Sustainsys.Saml2 With Dynamic Providers Sample

### Client Initiated Backchannel Login (CIBA)

[Section titled "Client Initiated Backchannel Login (CIBA)"](#client-initiated-backchannel-login-ciba)

This sample shows how a client can make [CIBA](/identityserver/ui/ciba/) login requests using Duende IdentityServer. To run the sample, the IdentityServer and API hosts should be started first. Next run the ConsoleCibaClient which will initiate the backchannel login request.

The URL the user would receive to log in and approve the request is being written out to the IdentityServer log (visible in the console window).

Follow that URL, log in as "alice", and then approve the login request to allow the client to receive the results.

[Client Initiated Backchannel Login (CIBA) Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/Ciba)GitHub Repository for the Client Initiated Backchannel Login (CIBA) Sample

### Windows Authentication With IIS Hosting

[Section titled "Windows Authentication With IIS Hosting"](#windows-authentication-with-iis-hosting)

This sample shows how to use Windows Authentication when hosting your IdentityServer behind IIS (or IIS Express). The salient piece to understand is a new `LoginWithWindows` action method in the `AccountController` from the quickstarts.

Windows authentication is triggered, and once the result is determined the main authentication session cookie is created based on the `WindowsIdentity` results.

Note there is some configuration in `Startup` with a call to `Configure<IISOptions>` (mainly to set `AutomaticAuthentication` to `false`).

[Windows Authentication With IIS HostingSample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/UserInteraction/WindowsAuthentication)GitHub Repository for the Windows Authentication With IIS Hosting Sample
