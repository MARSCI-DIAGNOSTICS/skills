---
title: Signing Key Store
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/signing-key-store/
source_type: llms-full-txt
content_hash: sha256:4077928ce602efde397fa9edd503aca9322c98a0bd1748ddd9e92ad7063b3f44
doc_id: signing-key-store
---

> Documentation for the ISigningKeyStore interface which manages the storage, retrieval, and deletion of cryptographic keys used for signing tokens.

#### Duende.IdentityServer.Stores.ISigningKeyStore

[Section titled "Duende.IdentityServer.Stores.ISigningKeyStore"](#duendeidentityserverstoresisigningkeystore)

Used to dynamically load client configuration.

```csharp
/// <summary>
/// Interface to model storage of serialized keys.
/// </summary>
public interface ISigningKeyStore
{
    /// <summary>
    /// Returns all the keys in storage.
    /// </summary>
    /// <returns></returns>
    Task<IEnumerable<SerializedKey>> LoadKeysAsync();


    /// <summary>
    /// Persists new key in storage.
    /// </summary>
    /// <param name="key"></param>
    /// <returns></returns>
    Task StoreKeyAsync(SerializedKey key);


    /// <summary>
    /// Deletes key from storage.
    /// </summary>
    /// <param name="id"></param>
    /// <returns></returns>
    Task DeleteKeyAsync(string id);
}
```

#### SerializedKey

[Section titled "SerializedKey"](#serializedkey)

```csharp
/// <summary>
/// Serialized key.
/// </summary>
public class SerializedKey
{
    /// <summary>
    /// Version number of serialized key.
    /// </summary>
    public int Version { get; set; }


    /// <summary>
    /// Key identifier.
    /// </summary>
    public string Id { get; set; }


    /// <summary>
    /// Date key was created.
    /// </summary>
    public DateTime Created { get; set; }


    /// <summary>
    /// The algorithm.
    /// </summary>
    public string Algorithm { get; set; }


    /// <summary>
    /// Contains X509 certificate.
    /// </summary>
    public bool IsX509Certificate { get; set; }


    /// <summary>
    /// Serialized data for key.
    /// </summary>
    public string Data { get; set; }


    /// <summary>
    /// Indicates if data is protected.
    /// </summary>
    public bool DataProtected { get; set; }
}
```

Note

The `Data` property contains a copy of all the values (and more) and is considered authoritative by IdentityServer, thus most of the other property values are considered informational and read-only.
