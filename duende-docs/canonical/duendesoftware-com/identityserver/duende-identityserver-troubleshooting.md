---
title: Duende IdentityServer Troubleshooting
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver-troubleshooting/
source_type: llms-full-txt
content_hash: sha256:b48c4242d6bc38888434658bc8bd77dd02022fe770fa2e9eb2e7859a740de805
category: identityserver
doc_id: identityserver/duende-identityserver-troubleshooting
---

When troubleshooting an IdentityServer setup we have some tips and tricks to share. These are both ways to get more information out of the system and how to detect and fix some common problems.

## General Debugging Advice

[Section titled âGeneral Debugging Adviceâ](#general-debugging-advice)

Duende IdentityServer is a security product and by design the error messages returned to a user or client application are very short. The actual error message is always written to the logs. The very first step in any troubleshooting should be to review the IdentityServer logs.

Another common issue is that the logs are redacted and that the interesting/relevant information is overwritten with **â\[PII is hidden]â**. (For example *The â\[PII is hidden]â for signing cannot be smaller than â\[PII is hidden]â bits*). This is a privacy feature of the Microsoft.IdentityModel libraries that we use for token handling. The definition of possible PII in those libraries is very generous and includes key sizes, URLs etc.

There is a static property that can be set to disable the redacting.

```csharp
IdentityModelEventSource.ShowPII = true;
```

We recommend to always set this flag to true in any development and test environment that does not contain real personal data.

## Diagnostics Data

[Section titled âDiagnostics Dataâ](#diagnostics-data)

**Version:** >=7.3

Newer versions of IdentityServer provide a way to collect important configuration and operational diagnostics data from your IdentityServer host. See [Diagnostics Data For IdentityServer](/identityserver/diagnostics/data/) for more information.

## Data protection

[Section titled âData protectionâ](#data-protection)

ASP.NET Core Data Protection is an encryption mechanism that is heavily used by Duende.IdentityServer and the ASP.NET Core Authentication libraries. If it is not correctly configured it might result in issues such as

* Unable to unprotect the message.State.
* The key `{xxxxx-xxxx-xxx-xxx-xxxxxxx}` was not found in the key ring.
* Failed to unprotect AuthenticationTicket payload for key `{key}`

See [our data protection guide](/identityserver/deployment/#aspnet-core-data-protection) for more information.

## Load Balancing, proxies and TLS offloading

[Section titled âLoad Balancing, proxies and TLS offloadingâ](#load-balancing-proxies-and-tls-offloading)

When running IdentityServer behind a load balancer it is important that IdentityServer still has access to the original request URL. IdentityServer uses that to create URLs that are included in the discovery document and in protocol messages.

To diagnose, open the discovery document (append `/.well-known/openid-configuration` to your root IdentityServer host), e.g. <https://demo.duendesoftware.com/.well-known/openid-configuration>. Make sure that the URLs listed in there have the correct host name and are listed as https (assuming you are running under https, which you should).

See [our proxy guide](/identityserver/deployment/#proxy-servers-and-load-balancers) for more information.

## TaskCancellationExceptions

[Section titled âTaskCancellationExceptionsâ](#taskcancellationexceptions)

TaskCancellationExceptions occur when the incoming HTTP connection is terminated by the requester. We pass the cancellation token along to Entity Framework so that it can cancel database queries and hopefully reduce load on your database. Both EF itself and the EF providers log those cancellations extremely aggressively before EF re-throws the exception. That unhandled exception then is handled by the IdentityServer middleware. This creates a lot of noise in the logs for what is actually expected behavior. It is normal for some HTTP requests to be canceled.

To help alleviate that, in version 6.2 of IdentityServer, we added a configurable filter to our logging to remove some of these unnecessary logs. Unfortunately the log messages that are written by EF itself are outside our control. Microsoft is in the process of updating EF to not log task cancellation so aggressively. In .NET 7, they were able to update the core EF but not the providers.

Since we know that these task cancellations are expected and safe, another thing you could do is to filter them out of your logs. Most logging tools should allow you to put filters in place. For example, in serilog, adding something like this to your configuration should do the trick:

```csharp
Log.Logger = new LoggerConfiguration()
  .Filter
  .ByExcluding(logEvent => logEvent.Exception is OperationCanceledException)
```

## WAF Rules

[Section titled âWAF Rulesâ](#waf-rules)

Data protected data can contain `--` (two dashes), which some firewalls disallow that because it looks like a SQL comment/injection. This is not an IdentityServer issue but something that should be fixed on the web application firewall.

## IdentityServerOptions.EmitStaticAudienceClaim and Token Validation

[Section titled âIdentityServerOptions.EmitStaticAudienceClaim and Token Validationâ](#identityserveroptionsemitstaticaudienceclaim-and-token-validation)

Some token validation implementations require that all JWTs include an audience claim with the key/value of `"aud"` and `"<issuer>/resources"`.

To add an audience claim to tokens created by IdentityServer, set the value of `IdentityServerOptions.EmitStaticAudienceClaim` to `true` during the setup of your IdentityServer instance (default: `false`).

Program.cs

```csharp
services.AddIdentityServer(options =>
{
    // add "aud" claim to JWT
    options.EmitStaticAudienceClaim = true;
})
.AddClientStore<ClientStore>()
.AddInMemoryIdentityResources(IdentityResources)
.AddInMemoryApiScopes(ApiScopes);
```

## Microsoft.IdentityModel versions

[Section titled âMicrosoft.IdentityModel versionsâ](#microsoftidentitymodel-versions)

Duende IdentityServer, the Microsoft external authentication handlers and other libraries all use the Microsoft.IdentityModel set of libraries. These libraries provide token and configuration handling features, and are

The `Microsoft.IdentityModel.*` libraries used by Duende IdentityServer all have to be of exactly the same version However, this is not enforced by NuGet so it is common to end up with an application that brings in different versions of `Microsoft.IdentityModel.*` through transitive dependencies.

Version conflicts can cause unexpected issues reading configuration data and tokens, i.e. **IDX10500: Signature validation failed. No security keys were provided to validate the signature.** or **System.MissingMethodException: Method not found âBoolean Microsoft.IdentityModel.Tokens.TokenUtilities.IsRecoverableConfiguration(â¦)â**

### Known Errors

[Section titled âKnown Errorsâ](#known-errors)

Errors that we have seen because of IdentityModel version mismatches include:

* IDX10500: Signature validation failed. No security keys were provided to validate the signature.
* System.MissingMethodException: Method not found âBoolean Microsoft.IdentityModel.Tokens.TokenUtilities.IsRecoverableConfiguration(â¦)â
* Microsoft.AspNetCore.Authentication.AuthenticationFailureException: An error was encountered while handling the remote login. ---> System.InvalidOperationException: An invalid request URI was provided. Either the request URI must be an absolute URI or BaseAddress must be set.

### Diagnosing

[Section titled âDiagnosingâ](#diagnosing)

Run this command in PowerShell:

```powershell
dotnet list package --include-transitive | sls "Microsoft.IdentityModel|System.IdentityModel"
```

The output should look something like this:

```txt
   > Microsoft.IdentityModel.Abstractions                       7.4.0
   > Microsoft.IdentityModel.JsonWebTokens                      7.4.0
   > Microsoft.IdentityModel.Logging                            7.4.0
   > Microsoft.IdentityModel.Protocols                          7.0.3
   > Microsoft.IdentityModel.Protocols.OpenIdConnect            7.0.3
   > Microsoft.IdentityModel.Tokens                             7.4.0
   > System.IdentityModel.Tokens.Jwt                            7.0.3
```

In the example above, it is clear that there are different versions active.

### Fixing

[Section titled âFixingâ](#fixing)

To fix this, add explicit package references to upgrade the packages that are of lower version to the most recent version used.

```xml
<ItemGroup>
    <PackageReference Include="Microsoft.IdentityModel.Protocols" Version="7.4.0"/>
    <PackageReference Include="Microsoft.IdentityModel.Protocols.OpenIdConnect" Version="7.4.0"/>
    <PackageReference Include="System.IdentityModel.Tokens.Jwt" Version="7.4.0"/>
</ItemGroup>
```

## Performance Issues

[Section titled âPerformance Issuesâ](#performance-issues)

In some installations, upgrading .NET and IdentityServer has caused performance issues. Since the IdentityServer and .NET version upgrades typically are done at the same time, it is sometimes hard to tell what the root cause is for the performance degradation. When working with installations to find the root cause, there are some dependencies that have been found to cause issues in specific versions.

### PostgreSQL Pooling

[Section titled âPostgreSQL Poolingâ](#postgresql-pooling)

There are issues with some versions of the PostgreSQL client library that gives large memory consumption. Enabling pooling on the operational store has solved this in the past:

```csharp
.AddOperationalStore(options =>
   {
      // Enable pooling:
      options.EnablePooling = true;


      // More settings....
   })
```

### Entity Framework Core & Microsoft SQL OPENJSON

[Section titled âEntity Framework Core & Microsoft SQL OPENJSONâ](#entity-framework-core--microsoft-sql-openjson)

Entity Framework Core version 8 introduced a new behaviour when creating `WHERE IN()` sql clauses. Previously, the possible values were supplied as parameters, which meant that the query text was dependent on the number of items in the collection. This was solved by sending the parameters as a JSON object and using `OPENJSON` to read the parameters. While this enabled query plan caching, it unfortunately caused Microsoft SQL Server to generate bad query execution plans.

Please see [this EF Core GitHub Issue](https://github.com/dotnet/efcore/issues/32394#issuecomment-2266634632) for information and possible mitigations.

### Microsoft Azure

[Section titled âMicrosoft Azureâ](#microsoft-azure)

The `Azure.Core` package versions `1.41.0` and prior had an issue that caused delays when accessing Azure resources. This could be Azure blob storage or key vault for data protection or Azure SQL Server for stores, especially if managed identities are used. This package is typically not referenced directly but brought in as a transient dependency through other packages. Ensure to use version `1.42.0` or later if you are hosting on Azure.

### Entity Framework Core, Microsoft.Data.SqlClient, and SqlServerRetryingExecutionStrategy

[Section titled âEntity Framework Core, Microsoft.Data.SqlClient, and SqlServerRetryingExecutionStrategyâ](#entity-framework-core-microsoftdatasqlclient-and-sqlserverretryingexecutionstrategy)

As more developers migrate their database-powered application to the cloud, they will need to handle intermittent connection failures. In most cases, these transient connection failures occur and resolve in a short period of time, allowing the application to self-correct and continue processing requests. The strategy is known as **connection resiliency**.

In recent versions of Entity Framework Core and `Microsoft.Data.SqlClient`, you can enable this retry strategy explicitly, but in the case of `Microsoft.Data.SqlClient`, when operating in a cloud environment, this strategy is enabled by default or defined in the connection string.

```csharp
protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
{
    optionsBuilder
        .UseSqlServer(
            @"Server=(localdb)\mssqllocaldb;Database=EFMiscellanous.ConnectionResiliency;Trusted_Connection=True;ConnectRetryCount=0",
            options => options.EnableRetryOnFailure());
}
```

In most cases, this is a *good feature to have enabled* but there are drawbacks that can cause severe system degradation.

* Enabling retry on failure causes Entity Framework Core to buffer the result set. This significantly increases memory requirements and causes garbage collection pauses.

* Some versions of `Microsoft.Data.SqlClient` call `Thread.Sleep` that can lock threads for up to ***10 seconds***. This can lead to thread exhaustion and server unresponsiveness. Weâve isolated this issue to versions.

  | Microsoft.EntityFrameworkCore.SqlServer | Microsoft.Data.SqlClient | Status     |
  | :-------------------------------------- | :----------------------- | :--------- |
  | `8.0.0`                                 | `>=5.1.1`                | â
 Good     |
  | `8.0.3`                                 | `>=5.1.5`                | â Affected |
  | `8.0.4`                                 | `>=5.1.5`                | â Affected |
  | `8.0.6`                                 | `>=5.1.5`                | â Affected |
  | `8.0.11`                                | `>=5.1.6`                | â
 Good     |
  | `9.0.1`                                 | `>=5.1.6`                | â
 Good     |
  | `>9.0.1`                                | `>=6.0.0`                | â Affected |

Architectural issues that may be causing connection resiliency issues you may want to investigate:

* Lack of caching in a high-load production environment.
* Under-provisioned database instance with limited resources or connections available.
* Datacenter networking issues caused by incorrect zoning choices.
* Under-provisioned application host with limited cores/threads.

## Cookie and Header Size Limits and Management

[Section titled âCookie and Header Size Limits and Managementâ](#cookie-and-header-size-limits-and-management)

The default cookie size limit is `4096` bytes. This is a limit imposed by the browser. In practice, this limit is enough for most applications. However, there are some scenarios where the default limit is not enough. ASP.NET Core will chunk cookies into multiple parts if they exceed the limit, but you may still run into `Bad Request - Request Too Long` when trying to set a cookie during the authentication process.

Here are some ways to manage the cookie size during authentication:

### Initiate a `SignOutAsync` during `Challenge`

[Section titled âInitiate a SignOutAsync during Challengeâ](#initiate-a-signoutasync-during-challenge)

When invoking `Challenge`, be sure to call `SignOutAsync` before returning the challenge result. This will ensure any existing session cookie is removed and a new one is created.

### Set SaveTokens to `false`

[Section titled âSet SaveTokens to falseâ](#set-savetokens-to-false)

When dealing with external authentication, you may want to set `SaveTokens` to `false` when calling `AddOpenIdConnect` to avoid storing the tokens in the cookie. Storing these tokens may not be necessary for your use case and take up unnecessary space.

Program.cs

```csharp
services.AddAuthentication()
    .AddOpenIdConnect(options =>
    {
        options.SaveTokens = false;
    });
```

### Set MapInboundClaims to `false`

[Section titled âSet MapInboundClaims to falseâ](#set-mapinboundclaims-to-false)

When dealing with external authentication, you may want to set `MapInboundClaims` to `false` when calling `AddOpenIdConnect` to avoid mapping the claims from the external provider.

Microsoftâs namespace for external claims is `http://schemas.microsoft.com/identity/claims/`, which is significantly larger than the claim names used by OpenID Connect and can take up unnecessary space.

Program.cs

```csharp
services.AddAuthentication()
    .AddOpenIdConnect(options =>
    {
        options.MapInboundClaims = false;
    });
```

### Implement `OnTicketReceived` To Reduce Cookie Size

[Section titled âImplement OnTicketReceived To Reduce Cookie Sizeâ](#implement-onticketreceived-to-reduce-cookie-size)

When dealing with external authentication, you may want to implement `OnTicketReceived` to reduce the size of the cookie. This is a callback that is invoked after the external authentication process is complete. You can use this callback to remove any claims that are not needed by your solution.

### Use Server-side Sessions

[Section titled âUse Server-side Sessionsâ](#use-server-side-sessions)

You can use [server-side sessions](/identityserver/ui/server-side-sessions) to store the userâs session data in a data store instead of in the cookie. This will greatly reduce the size of the cookie while allowing you to store more data in the session.

Note

This feature is part of the [Duende IdentityServer Business and Enterprise Edition](https://duendesoftware.com/products/identityserver).

### Implement a Custom `ITicketStore` to Reduce Cookie Size

[Section titled âImplement a Custom ITicketStore to Reduce Cookie Sizeâ](#implement-a-custom-iticketstore-to-reduce-cookie-size)

When configuring the cookie authentication handler, you can provide a custom `ITicketStore` implementation to store the authentication ticket data server-side instead of in the cookie.

Program.cs

```csharp
services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options =>
    {
        // Use your custom ITicketStore implementation:
        options.SessionStore = new CustomTicketStore();
    });
```

And then implement the `ITicketStore` interface to store the ticket data in a database or other storage mechanism.

CustomTicketStore.cs

```csharp
public class CustomTicketStore : ITicketStore
{
    public Task<string> StoreAsync(AuthenticationTicket ticket)
    {
        // Implement your logic to store the ticket data
        // Return a unique identifier for the stored ticket
    }


    public Task<AuthenticationTicket> RetrieveAsync(string key)
    {
        // Implement your logic to retrieve the ticket data by key
    }


    public Task RemoveAsync(string key)
    {
        // Implement your logic to remove the ticket data by key
    }


    public Task RenewAsync(string key, AuthenticationTicket ticket)
    {
        // Implement your logic to renew the ticket data by key
    }
}
```

ITicketStore and Dependency Injection

When using the `AddCookie` method to configure the cookie authentication handler, you cannot use dependency injection to resolve a service and its dependencies for `ITicketStore`.

To work around this limitation, you can create a custom `IPostConfigureOptions<CookieAuthenticationOptions>` implementation like we did for [Server-Side Sessions](/identityserver/ui/server-side-sessions), which uses [a shim](https://github.com/DuendeSoftware/products/blob/main/identity-server/src/IdentityServer/Configuration/DependencyInjection/PostConfigureApplicationCookieTicketStore.cs) to inject an `IHttpContextAccessor` into the actual `ITicketStore` service.

## URL and Query String Size Limits and Management

[Section titled âURL and Query String Size Limits and Managementâ](#url-and-query-string-size-limits-and-management)

While most browsers currently support URLs longer than 2000 characters, web servers may still return an error status code when they find that the URL or query string is too long.

For most authentication flows, URLs will stay well under 2000 characters in length. When federating to an external identity provider, however, URLs can quickly grow too large because of all the query parameters that were added.

Web servers can respond differently when a URL or query string is too large:

* Apache responds with `414 Request-URI Too Large` when a URL exceeds 8190 bytes.

* IIS responds with `404 Not Found` and uses two different substatus codes depending on the issue:

  * If the URL exceeds 4096 bytes, the substatus code is `404.14 URL Too Long`.
  * If the query string exceeds 2048 bytes, the substatus code is `404.15 Query String Too Long`.

* Nginx responds with `414 Request-URI Too Large` when a URL exceeds 8192 bytes.

To fix this issue, there are two solutions:

### Reduce State Query Parameter Size

[Section titled âReduce State Query Parameter Sizeâ](#reduce-state-query-parameter-size)

When IdentityServer redirects the user to an external Identity Provider, it includes a data protected `state` query parameter. The combination of this `state` parameter with other data being added by the external IdP can cause the URL to become too large. You can drastically reduce the size of the `state` parameter by storing the state in IdentityServer, rather than passing it along in the request URL.

See [External Providers - State, URL length, And ISecureDataFormat](/identityserver/ui/login/external/#state-url-length-and-isecuredataformat) for more information about this workaround.

### Increase the Maximum Size of URL or Query String data

[Section titled âIncrease the Maximum Size of URL or Query String dataâ](#increase-the-maximum-size-of-url-or-query-string-data)

Depending on the web server youâre using, you can change the maximum size of the URL or query string.

Caution

While increasing the size limits may work for your use case, the first solution is a more robust way to reduce the size of the query string when federating with an external identity provider.

* Apache

  You can increase the value for `LimitRequestLine` to allow longer URLs, by adding or changing this directive in your server config file (for all virtual hosts), or for specific virtual hosts in their respective `<VirtualHost></VirtualHost>` entry.

  See <https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestline> for more information.

* Microsoft IIS

  Configure the `requestLimits` XML element to increase the max URL and query string size in your `web.config` file:

  web.config

  ```xml
      <configuration>
        <system.webServer>
          <security>
            <requestFiltering>
              <requestLimits maxUrl="8192" maxQueryString="4096" />
            </requestFiltering>
          </security>
        </system.webServer>
      </configuration>
  ```

  See <https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/requestlimits/> for more information.

* Nginx

  You can increase the size for each buffer in `large_client_header_buffers` to allow longer URLs, by adding or changing this directive in the `http { }` context (for all virtual servers), or for specific virtual servers in their respective `server { }` entry.

  This setting has two parameters:

  * the number of buffers
  * the size of each buffer

  The second parameter, the size of the each buffer, determines the maximum URL length.

  See <https://nginx.org/en/docs/http/ngx_http_core_module.html#large_client_header_buffers> for more information.

## X.509 Certificates

[Section titled âX.509 Certificatesâ](#x509-certificates)

When your IdentityServer is hosted in a Windows environment, it is possible that private key material is being stored or read from a user profile location. On Azure however, App Services are typically configured not to load a user profile because this brings overhead and is often not needed. This can result in runtime errors when IdentityServer attempts to generate or load key material:

```text
System.Security.Cryptography.CryptographicException: Access denied.
   at System.Security.Cryptography.X509Certificates.X509CertificateLoader.ImportPfx(ReadOnlySpan`1 data, ReadOnlySpan`1 password, X509KeyStorageFlags keyStorageFlags)
   at System.Security.Cryptography.X509Certificates.X509CertificateLoader.LoadPkcs12NoLimits(ReadOnlyMemory`1 data, ReadOnlySpan`1 password, X509KeyStorageFlags keyStorageFlags, Pkcs12Return& earlyReturn)
   at System.Security.Cryptography.X509Certificates.X509CertificateLoader.LoadPkcs12(ReadOnlyMemory`1 data, ReadOnlySpan`1 password, X509KeyStorageFlags keyStorageFlags, Pkcs12LoaderLimits loaderLimits)
   at System.Security.Cryptography.X509Certificates.X509CertificateLoader.LoadPkcs12Pal(ReadOnlySpan`1 data, ReadOnlySpan`1 password, X509KeyStorageFlags keyStorageFlags, Pkcs12LoaderLimits loaderLimits)
   at System.Security.Cryptography.X509Certificates.CertificatePal.FromBlobOrFile(ReadOnlySpan`1 rawData, String fileName, SafePasswordHandle password, X509KeyStorageFlags keyStorageFlags)
   at System.Security.Cryptography.X509Certificates.X509Certificate..ctor(Byte[] rawData, String password, X509KeyStorageFlags keyStorageFlags)
   at System.Security.Cryptography.X509Certificates.X509Certificate2..ctor(Byte[] rawData, String password, X509KeyStorageFlags keyStorageFlags)
   at Duende.IdentityServer.Services.KeyManagement.X509KeyContainer.ToSecurityKey() in /_/identity-server/src/IdentityServer/Services/Default/KeyManagement/X509KeyContainer.cs:line 108
   at Duende.IdentityServer.Services.KeyManagement.AutomaticKeyManagerKeyStore.<>c.<GetValidationKeysAsync>b__5_0(KeyContainer x) in /_/identity-server/src/IdentityServer/Services/Default/KeyManagement/AutomaticKeyManagerKeyStore.cs:line 106
   at System.Linq.Enumerable.ArraySelectIterator`2.Fill(ReadOnlySpan`1 source, Span`1 destination, Func`2 func)
   at System.Linq.Enumerable.ArraySelectIterator`2.ToArray()
   at System.Linq.Enumerable.ToArray[TSource](IEnumerable`1 source)
   at Duende.IdentityServer.Services.KeyManagement.AutomaticKeyManagerKeyStore.GetValidationKeysAsync() in /_/identity-server/src/IdentityServer/Services/Default/KeyManagement/AutomaticKeyManagerKeyStore.cs:line 106
   at Duende.IdentityServer.Services.DefaultKeyMaterialService.GetValidationKeysAsync() in /_/identity-server/src/IdentityServer/Services/Default/DefaultKeyMaterialService.cs:line 112
   at Duende.IdentityServer.ResponseHandling.DiscoveryResponseGenerator.CreateDiscoveryDocumentAsync(String baseUrl, String issuerUri) in /_/identity-server/src/IdentityServer/ResponseHandling/Default/DiscoveryResponseGenerator.cs:line 110
   at Duende.IdentityServer.Endpoints.DiscoveryEndpoint.ProcessAsync(HttpContext context) in /_/identity-server/src/IdentityServer/Endpoints/DiscoveryEndpoint.cs:line 82
   at Duende.IdentityServer.Hosting.IdentityServerMiddleware.Invoke(HttpContext context, IdentityServerOptions options, IEndpointRouter router, IUserSession userSession, IEventService events, IIssuerNameService issuerNameService, ISessionCoordinationService sessionCoordinationService) in /_/identity-server/src/IdentityServer/Hosting/IdentityServerMiddleware.cs:line 109
```

To fix this issue on Azure hosted web applications, add the following environment variable to the App Service:

```text
WEBSITE_LOAD_USER_PROFILE=1
```

After saving this environment variable, your App Service will restart and Kudu (the engine behind git deployments in Azure App Service) will load the user profile when running your web application. For more information about this and other Kudu configuration options, see <https://github.com/projectkudu/kudu/wiki/Configurable-settings>.

If youâre hosting the web application using IIS on Windows, youâll need to configure the application pool to load the user profile. See <https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/iis/advanced?view=aspnetcore-9.0#data-protection> for more information on how to configure the application pool.

### Why does a web application need to load a user profile to work with X.509 certificates?

[Section titled âWhy does a web application need to load a user profile to work with X.509 certificates?â](#why-does-a-web-application-need-to-load-a-user-profile-to-work-with-x509-certificates)

The `X509Certificate2` class in .NET stores the private key part of a certificate somewhere else depending on the use of `X509KeyStorageFlags`:

* `X509KeyStorageFlags.MachineKeySet` stores the private key in a `Keys` registry subfolder of the certificate store.
* `X509KeyStorageFlags.UserKeySet` stores the private key in the current userâs roaming profile folder, e.g. `%AppData%\Microsoft\SystemCertificates\My\Keys`.

When loading a certificate containing both a public and private key in .NET, the private key may also end up in different locations:

* Machine keys end up in the `%ProgramData%\Microsoft\Crypto\RSA\MachineKeys` folder.
* User keys are stored in the current userâs roaming profile folder but this time in a different location: `%AppData%\Microsoft\Crypto\RSA`

If you donât explicitly use the `X509KeyStorageFlags.MachineKeySet` flag value, the default behavior is to use `X509KeyStorageFlags.DefaultKeySet`. According to the [.NET documentation](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509keystorageflags), this means: *The default key set is used. **The user key set is usually the default***.

When an application runs without an active user profile, any private key material stored in a user profile canât be accessed. Even loading a certificate can fail, since the load operation could attempt to store the private key material in the user profile.
