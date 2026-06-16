---
title: Licensing
source_url: https://docs.duendesoftware.com/general/licensing/
source_type: llms-full-txt
content_hash: sha256:19bebe6b4de5130b2b4accf61d4011b9402951fc53a24a9c26f090acc8b70df2
doc_id: general/licensing
---

> Details about Duende IdentityServer and BFF licensing requirements, editions, configuration options, and trial mode functionality.

Duende products, except for our [open source tools](https://duendesoftware.com/products/opensource), require a license for production use. The [Duende Software website](https://duendesoftware.com/) provides an overview of different products and license editions.

Licenses can be configured via a file system, programmatic startup, or external configuration services like Azure Key Vault, with trial mode available for development and testing.

## IdentityServer

[Section titled "IdentityServer"](#identityserver)

Duende IdentityServer requires a license for production use, with three editions available (Starter, Business, and Enterprise) that offer various features based on organizational needs. A [community edition](https://duendesoftware.com/products/communityedition/) is available as well.

Free for development

IdentityServer is [free](#trial-mode) for development, testing and personal projects, but production use requires a [license](https://duendesoftware.com/products/identityserver).

### Editions

[Section titled "Editions"](#editions)

There are three license editions which include different [features](https://duendesoftware.com/products/features).

#### Starter Edition

[Section titled "Starter Edition"](#starter-edition)

The Starter edition includes the core OIDC and OAuth protocol implementation. This is an economical option that is a good fit for organizations with basic needs. It's also a great choice if you have an aging [IdentityServer4 implementation that needs to be updated](/identityserver/upgrades/identityserver4-to-duende-identityserver-v7/) and licensed. The Starter edition includes all the features that were part of IdentityServer4, along with support for the latest .NET releases, improved observability through [OpenTelemetry support](/identityserver/diagnostics/otel/), and years of bug fixes and enhancements.

#### Business Edition

[Section titled "Business Edition"](#business-edition)

The Business edition adds additional features that go beyond the core protocol support included in the Starter edition. This is a popular license because it adds the most commonly needed tools and features outside a basic protocol implementation. Feature highlights include support for server side sessions and automatic signing key management.

#### Enterprise Edition

[Section titled "Enterprise Edition"](#enterprise-edition)

Finally, the Enterprise edition includes everything in the Business edition and adds support for features that are typically used by enterprises with particularly complex architectures or that handle particularly sensitive data. Highlights include resource isolation, the OpenId Connect CIBA flow, and dynamic federation. This is the best option when you have a specific threat model or architectural need for these features.

### Redistribution

[Section titled "Redistribution"](#redistribution)

If you want to redistribute Duende IdentityServer to your customers as part of a product, you can use our [redistributable license](https://duendesoftware.com/products/identityserverredist).

### License Validation and Logging

[Section titled "License Validation and Logging"](#license-validation-and-logging)

The license is validated at startup and during runtime. All license validation is self-contained and does not leave the host. There are no outbound network calls related to license validation.

#### Startup Validation

[Section titled "Startup Validation"](#startup-validation)

At startup, IdentityServer first checks for a license. If there is no license configured, IdentityServer logs a warning indicating that a license is required in a production deployment and enters [Trial Mode](#trial-mode).

Next, assuming a license is configured, IdentityServer compares its configuration to the license. If there are discrepancies between the license and the configuration, IdentityServer will write log messages indicating the nature of the problem.

#### Runtime Validation

[Section titled "Runtime Validation"](#runtime-validation)

Most common licensing issues, such as expiration of the license or configuring more clients than are included in the license do not prevent IdentityServer from functioning. We trust our customers, and we don't want a simple oversight to cause an outage. However, some features will be disabled at runtime if your license does not include them, including:

* [Server Side Sessions](/identityserver/ui/server-side-sessions/)
* [Demonstrating Proof-of-Possession (DPoP)](/identityserver/tokens/pop/)
* [Resource Isolation](/identityserver/fundamentals/resources/isolation/)
* [Pushed Authorization Requests (PAR)](/identityserver/tokens/par/)
* [Dynamic Identity Providers](/identityserver/ui/login/dynamicproviders/)
* [Client Initiated Backchannel Authentication (CIBA)](/identityserver/ui/ciba/)

Again, the absence of a license is permitted for development and testing, and therefore does not disable any of these features. Similarly, using an expired license that includes those features does not cause those features to be disabled.

Tip

When rolling over to a renewed license, you can configure the new license before the old license expires. While the expiration timestamp of a license is used to validate a license is active, the start date is an administrative data point IdentityServer does not take into account for license validation. In other words, you can safely configure the new license before the old one lapses.

#### Trial Mode

[Section titled "Trial Mode"](#trial-mode)

Using IdentityServer without a license is considered Trial Mode. In Trial Mode, all enterprise features are enabled. Trial Mode is limited to 500 protocol requests. This includes all HTTP requests that IdentityServer itself handles, such as requests for the discovery, authorize, and token endpoints. UI requests, such as the login page, are not included in this limit. Beginning in IdentityServer 7.1, IdentityServer will log a warning when the trial mode threshold is exceeded:

```text
You are using IdentityServer in trial mode and have exceeded the trial
threshold of 500 requests handled by IdentityServer. In a future version,
you will need to restart the server or configure a license key to continue testing.
```

In a future version, IdentityServer will shut down at that time instead.

Note

When operating non-production environments, such as development, test, or QA, without a valid license key, you may run into this trial mode limitation.

To prevent your non-production IdentityServer from shutting down in the future, you can use your production license key. IdentityServer is [free](#trial-mode) for development, testing and personal projects, and we support using your production license in these environments when trial mode is not sufficient.

If you have feedback on trial mode, or specific use cases where you'd prefer other options, please [open a community discussion](https://github.com/DuendeSoftware/community/discussions).

#### Redistribution

[Section titled "Redistribution"](#redistribution-1)

We understand that when IdentityServer is redistributed, log messages from the licensing system are not likely to be very useful to your redistribution customers. For that reason, in a redistribution the severity of log messages from the license system is turned all the way down to the trace level.

We also appreciate that it might be cumbersome to deploy updated licenses in this scenario, especially if the deployment of your software does not coincide with the duration of the IdentityServer license. In that situation, we ask that you update the license key at the next deployment of your software to your redistribution customers. Of course, you are always responsible for ensuring that your license is renewed.

#### Log Severity

[Section titled "Log Severity"](#log-severity)

The severity of the log messages described above depend on the nature of the message and the type of license.

| Type of Message               | Standard License | Redistribution License (development\*) | Redistribution License (production\*) |
| ----------------------------- | ---------------- | -------------------------------------- | ------------------------------------- |
| Startup, missing license      | Warning          | Warning                                | Warning                               |
| Startup, license details      | Debug            | Debug                                  | Trace                                 |
| Startup, valid license notice | Informational    | Informational                          | Trace                                 |
| Startup, violations           | Error            | Error                                  | Trace                                 |
| Runtime, violations           | Error            | Error                                  | Trace                                 |

\* as determined by `IHostEnvironment.IsDevelopment()`

## BFF Security Framework

[Section titled "BFF Security Framework"](#bff-security-framework)

The Duende BFF Security Framework requires a license for production use, with two editions available (Starter and Enterprise) that offer various features based on organizational needs.

Trial mode

Duende BFF has a [limited trial mode](#bff-trial-mode) for development and testing. For small organizations or personal projects, consider the [community edition](https://duendesoftware.com/products/communityedition/). For production use, a [license](https://duendesoftware.com/products/bff) is required.

### Editions

[Section titled "Editions"](#editions-1)

BFF is a library designed to enhance the security of browser-based applications by moving authentication flows to the server side. The Duende BFF Security Framework requires a license for production use, and is available in two editions that [include different functionality](https://duendesoftware.com/products/bff) based on organizational needs.

### Redistribution

[Section titled "Redistribution"](#redistribution-2)

If you want to redistribute Duende BFF to your customers as part of a product, please [reach out to sales](https://duendesoftware.com/contact/sales).

### License Validation and Logging

[Section titled "License Validation and Logging"](#license-validation-and-logging-1)

The BFF license is validated during runtime. All license validation is self-contained and does not leave the host. There are no outbound network calls related to license validation.

#### BFF v3.1+ Runtime Validation

[Section titled "BFF v3.1+ Runtime Validation"](#bff-v31-runtime-validation)

BFF v3.1 does not technically enforce the presence of a license key. At runtime, if no license is present, an error message will be logged.

#### BFF v4 Runtime Validation

[Section titled "BFF v4 Runtime Validation"](#bff-v4-runtime-validation)

BFF v4 requires a valid license in production environments. When no license is present, the system operates in [trial mode](#bff-trial-mode) with a limitation of maximum of five sessions per host (not technically enforced) with any excess resulting in error logging.

Trial mode is also enabled when the license could not be validated, for example when the signature validation fails.

When an expired license is used, the system will continue to function with only a warning written to the logs, and not fall back to trial mode.

#### BFF Trial Mode

[Section titled "BFF Trial Mode"](#bff-trial-mode)

Using BFF without a license is considered Trial Mode. Whenrunning in Trial Mode, you will see the following error logged on startup:

```text
You do not have a valid license key for the Duende software.
BFF will run in trial mode. This is allowed for development and testing scenarios.


If you are running in production you are required to have a licensed version.
Please start a conversation with us: https://duende.link/l/bff/contact
```

In Trial Mode, BFF will be limited to a maximum of five (5) sessions per host. Sessions exceeding the limit will cause the host to log an error for every consecutive authenticated session:

```text
BFF is running in trial mode. The maximum number of allowed authenticated sessions (5) has been exceeded.


See https://duende.link/l/bff/trial for more information.
```

The trial mode session limit is not distributed or shared across multiple nodes.

Note

When operating non-production environments, such as development, test, or QA, without a valid license key, you may run into this trial mode limitation.

If you require a larger number of sessions, we support using your production license in these environments when trial mode is not enough.

## License Key

[Section titled "License Key"](#license-key)

The license key can be configured in one of two ways:

* Via a well-known file on the file system
* Programmatically in your startup code

You can also use other configuration sources such as Azure Key Vault, by using the programmatic approach.

Redistributable license

If you use our [redistributable license](https://duendesoftware.com/products/identityserverredist), we recommend loading the license at startup from an embedded resource.

We consider the license key to be private to your organization, but not necessarily a secret. If you're using private source control that is scoped to your organization, storing your license key within it is acceptable.

### File System

[Section titled "File System"](#file-system)

Duende products like IdentityServer and the BFF Security Framework look for a file named `Duende_License.key` in the [ContentRootPath](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.ihostenvironment.contentrootpath?#microsoft-extensions-hosting-ihostenvironment-contentrootpath) of your application. If present, the content of the file will be used as the license key.

### Startup

[Section titled "Startup"](#startup)

If you prefer to load the license key programmatically, you can do so in your startup code. This allows you to use the ASP.NET configuration system to load the license key from any [configuration provider](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/?view=aspnetcore-7.0#cp), including environment variables, `appsettings.json`, external configuration services such as Azure App Configuration, Azure Key Vault, etc.

#### IdentityServer

[Section titled "IdentityServer"](#identityserver-1)

The `AddIdentityServer` method accepts a lambda expression to configure various options in your IdentityServer, including the `LicenseKey`. Set the value of this property to the content of the license key file.

Program.cs

```csharp
builder.Services.AddIdentityServer(options =>
{
    // the content of the license key file
    options.LicenseKey = "eyJhbG...";
});
```

#### BFF Security Framework

[Section titled "BFF Security Framework"](#bff-security-framework-1)

The `AddBff` method accepts a lambda expression to configure various options in your BFF host, including the `LicenseKey`. Set the value of this property to the content of the license key file.

Program.cs

```csharp
builder.Services.AddBff(options =>
{
    // the content of the license key file
    options.LicenseKey = "eyJhbG...";
});
```

### Azure Key Vault

[Section titled "Azure Key Vault"](#azure-key-vault)

When deploying your application to Microsoft Azure, you can make use of [Azure Key Vault](https://azure.microsoft.com/products/key-vault/) to load the Duende license key at startup.

Similarly to setting the license key programmatically, you can use the `AddIdentityServer` or `AddBff` method, and use the overload that accepts a lambda expression to configure the `LicenseKey` property.

Program.cs

```csharp
var keyVaultUrl = new Uri("https://<YourKeyVaultName>.vault.azure.net/");


var secretClient = new Azure.Security.KeyVault.Secrets.SecretClient(
    keyVaultUrl,
    new Azure.Identity.DefaultAzureCredential()
);


KeyVaultSecret licenseKeySecret = secretClient.GetSecret("<YourSecretName>");
var licenseKey = licenseKeySecret.Value;


// Inject the secret (license key) into the IdentityServer configuration
builder.Services.AddIdentityServer(options =>
{
    options.LicenseKey = licenseKey;
});
```

If you are using [Azure App Configuration](https://azure.microsoft.com/products/app-configuration/), you can use a similar approach to load the license key into your application host.
