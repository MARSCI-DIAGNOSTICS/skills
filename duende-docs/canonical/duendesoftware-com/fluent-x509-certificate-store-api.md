---
title: Fluent X.509 Certificate Store API
source_url: https://docs.duendesoftware.com/fluent-x509-certificate-store-api/
source_type: llms-full-txt
content_hash: sha256:1f94cbc8d3f98bd6590717a182f55ecb69e38cab105e69d32350777016d13267
doc_id: fluent-x509-certificate-store-api
---

> Provides a simplified, fluent API for accessing and managing X.509 certificates in a certificate store.

A common place to store X.509 certificates is within a host's X.509 certificate store. With .NET APIs, this is done using the `X509Store` class.

```csharp
using System.Security.Cryptography.X509Certificates;


// with .NET APIs
using var store = new X509Store(StoreName.My, StoreLocation.CurrentUser);


store.Open(OpenFlags.ReadOnly);


using var certificate = store.Certificates
    .Find(X509FindType.FindBySubjectDistinguishedName,
          "CN=localhost",
          false)[0];


if (certificate == null)
    throw new InvalidOperationException("Certificate not found");


Console.WriteLine(certificate);
```

The *X509* class in the IdentityModel library is a simplified API to load certificates from a certificate store. The following code loads a certificate by name from the personal machine store:

```csharp
using Duende.IdentityModel;


using var certificate = X509.CurrentUser
    .My
    .SubjectDistinguishedName
    .Find("CN=localhost", false)
    .FirstOrDefault();


if (certificate == null)
    throw new InvalidOperationException("Certificate not found");


Console.WriteLine(certificate);
```

### Certificate Store Locations

[Section titled "Certificate Store Locations"](#certificate-store-locations)

You can load certificates from the following machine or user stores:

* *My*
* *AddressBook*
* *TrustedPeople*
* *CertificateAuthority*
* *TrustedPublisher*

### Certificate Search Options

[Section titled "Certificate Search Options"](#certificate-search-options)

You can search for a certificate by the following attributes:

* Subject name,
* Thumbprint
* Issuer name
* Serial number.

### Debugging Certificates in a Store

[Section titled "Debugging Certificates in a Store"](#debugging-certificates-in-a-store)

When finding it difficult to find a certificate by name, you can use the following code to list all certificates in a store for debugging purposes:

```csharp
using System.Security.Cryptography.X509Certificates;


using var store = new X509Store(StoreName.My, StoreLocation.CurrentUser);
store.Open(OpenFlags.ReadOnly);


var certificates = store.Certificates;
foreach (var certificate in certificates)
{
    Console.WriteLine($"{certificate.Subject} ({certificate.Thumbprint})");
}
```
