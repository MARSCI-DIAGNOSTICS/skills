---
title: Backchannel Authentication Request Store
source_url: https://docs.duendesoftware.com/identityserver/backchannel-authentication-request-store/
source_type: llms-full-txt
content_hash: sha256:3e7411451b8026e5d814c2d337a942a6bc8cc15342f31a5413e60b5a35ffa46f
category: identityserver
doc_id: identityserver/backchannel-authentication-request-store
---

> Documentation for the IBackChannelAuthenticationRequestStore interface which is used to store and manage backchannel authentication requests for CIBA flows.

#### Duende.IdentityServer.Stores.IBackChannelAuthenticationRequestStore

[Section titled "Duende.IdentityServer.Stores.IBackChannelAuthenticationRequestStore"](#duendeidentityserverstoresibackchannelauthenticationrequeststore)

Used to store backchannel login requests (for [CIBA](/identityserver/ui/ciba/)).

```csharp
/// <summary>
/// Interface for the backchannel authentication request store
/// </summary>
public interface IBackChannelAuthenticationRequestStore
{
    /// <summary>
    /// Creates the request.
    /// </summary>
    Task<string> CreateRequestAsync(BackChannelAuthenticationRequest request, CancellationToken ct);


    /// <summary>
    /// Gets the requests.
    /// </summary>
    Task<IEnumerable<BackChannelAuthenticationRequest>> GetLoginsForUserAsync(string subjectId, CancellationToken ct, string? clientId = null);


    /// <summary>
    /// Gets the request.
    /// </summary>
    Task<BackChannelAuthenticationRequest?> GetByAuthenticationRequestIdAsync(string requestId, CancellationToken ct);


    /// <summary>
    /// Gets the request.
    /// </summary>
    Task<BackChannelAuthenticationRequest?> GetByInternalIdAsync(string id, CancellationToken ct);


    /// <summary>
    /// Removes the request.
    /// </summary>
    Task RemoveByInternalIdAsync(string id, CancellationToken ct);


    /// <summary>
    /// Updates the request.
    /// </summary>
    Task UpdateByInternalIdAsync(string id, BackChannelAuthenticationRequest request, CancellationToken ct);
}
```

#### BackChannelAuthenticationRequest

[Section titled "BackChannelAuthenticationRequest"](#backchannelauthenticationrequest)

```csharp
/// <summary>
/// Models a backchannel authentication request.
/// </summary>
public class BackChannelAuthenticationRequest
{
    /// <summary>
    /// The identifier for this request in the store.
    /// </summary>
    public string InternalId { get; set; }


    /// <summary>
    /// Gets or sets the creation time.
    /// </summary>
    public DateTime CreationTime { get; set; }


    /// <summary>
    /// Gets or sets the life time in seconds.
    /// </summary>
    public int Lifetime { get; set; }


    /// <summary>
    /// Gets or sets the ID of the client.
    /// </summary>
    public string ClientId { get; set; }


    /// <summary>
    /// Gets or sets the subject.
    /// </summary>
    public ClaimsPrincipal Subject { get; set; }


    /// <summary>
    /// Gets or sets the requested scopes.
    /// </summary>
    public IEnumerable<string> RequestedScopes { get; set; }


    /// <summary>
    /// Gets or sets the requested resource indicators.
    /// </summary>
    public IEnumerable<string> RequestedResourceIndicators { get; set; }


    /// <summary>
    /// Gets or sets the authentication context reference classes.
    /// </summary>
    public ICollection<string> AuthenticationContextReferenceClasses { get; set; }


    /// <summary>
    /// Gets or sets the tenant.
    /// </summary>
    public string Tenant { get; set; }


    /// <summary>
    /// Gets or sets the idp.
    /// </summary>
    public string IdP { get; set; }


    /// <summary>
    /// Gets or sets the binding message.
    /// </summary>
    public string BindingMessage { get; set; }




    /// <summary>
    /// Gets or sets a value indicating whether this instance has been completed.
    /// </summary>
    public bool IsComplete { get; set; }


    /// <summary>
    /// Gets or sets the authorized scopes.
    /// </summary>
    public IEnumerable<string> AuthorizedScopes { get; set; }


    /// <summary>
    /// Gets or sets the session identifier from which the user approved the request.
    /// </summary>
    public string SessionId { get; set; }


    /// <summary>
    /// Gets the description the user assigned to the client being authorized.
    /// </summary>
    public string Description { get; set; }
}
```
