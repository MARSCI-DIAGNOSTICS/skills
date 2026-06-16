---
title: Identity Provider
source_url: https://docs.duendesoftware.com/identityserver/identity-provider/
source_type: llms-full-txt
content_hash: sha256:82c10316dc779e36d740513c6b004ed05ff3e4a15ae82432d6fb027e5c288896
category: identityserver
doc_id: identityserver/identity-provider
---

> Reference documentation for identity provider models in Duende IdentityServer, including OidcProvider for external OpenID Connect providers, IdentityProviderName, and the base IdentityProvider class.

## Duende.IdentityServer.Models.OidcProvider

[Section titled "Duende.IdentityServer.Models.OidcProvider"](#duendeidentityservermodelsoidcprovider)

The `OidcProvider` models an external OpenID Connect provider for use in the [dynamic providers](/identityserver/ui/login/dynamicproviders/) feature. Its properties map to the Open ID Connect options class from ASP.NET Core, and those properties include:

* **`Enabled`**

  Specifies if provider is enabled. Defaults to `true`.

* **`Scheme`**

  Scheme name for the provider.

* **`DisplayName`**

  Display name for the provider.

* **`Type`**

  Protocol type of the provider. Defaults to `"oidc"` for the `OidcProvider`.

* **`Authority`**

  The base address of the OIDC provider.

* **`ResponseType`**

  The response type. Defaults to `"id_token"`.

* **`ClientId`**

  The client id.

* **`ClientSecret`**

  The client secret. By default, this is the plaintext client secret and great consideration should be taken if this value is to be stored as plaintext in the store. It is possible to store this in a protected way and then unprotect when loading from the store either by implementing a custom `IIdentityProviderStore` or registering a custom `IConfigureNamedOptions<OpenIdConnectOptions>`.

* **`Scope`**

  Space separated list of scope values.

* **`GetClaimsFromUserInfoEndpoint`**

  Indicates if userinfo endpoint is to be contacted. Defaults to true.

* **`UsePkce`**

  Indicates if PKCE should be used. Defaults to true.

#### Duende.IdentityServer.Models.IdentityProviderName

[Section titled "Duende.IdentityServer.Models.IdentityProviderName"](#duendeidentityservermodelsidentityprovidername)

The `IdentityProviderName` models the display name of an identity provider.

* **`Enabled`**

  Specifies if provider is enabled. Defaults to `true`.

* **`Scheme`**

  Scheme name for the provider.

* **`DisplayName`**

  Display name for the provider.

#### Duende.IdentityServer.Models.IdentityProvider

[Section titled "Duende.IdentityServer.Models.IdentityProvider"](#duendeidentityservermodelsidentityprovider)

The `IdentityProvider` is a base class to model arbitrary identity providers, which `OidcProvider` derives from. This leaves open the possibility for extensions to the dynamic provider feature to support other protocol types (as distinguished by the `Type` property).
