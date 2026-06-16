---
title: Server-Side Session Store
source_url: https://docs.duendesoftware.com/identityserver/server-side-session-store/
source_type: llms-full-txt
content_hash: sha256:dca2fe9a3ddd2d1f6b3a77926bb91956da52d0936ff2b8a43ddb060b4c030f46
category: identityserver
doc_id: identityserver/server-side-session-store
---

> Documentation for the IServerSideSessionStore interface and related models for managing server-side user authentication session data.

#### Duende.IdentityServer.Stores.IServerSideSessionStore

[Section titled "Duende.IdentityServer.Stores.IServerSideSessionStore"](#duendeidentityserverstoresiserversidesessionstore)

Used to persist users' authentication session data when using the [server-side sessions feature](/identityserver/ui/server-side-sessions/).

```csharp
/// <summary>
/// User session store
/// </summary>
public interface IServerSideSessionStore
{
    /// <summary>
    /// Retrieves a session
    /// </summary>
    Task<ServerSideSession?> GetSessionAsync(string key, CancellationToken ct);


    /// <summary>
    /// Creates a session
    /// </summary>
    Task CreateSessionAsync(ServerSideSession session, CancellationToken ct);


    /// <summary>
    /// Updates a session
    /// </summary>
    Task UpdateSessionAsync(ServerSideSession session, CancellationToken ct);


    /// <summary>
    /// Deletes a session
    /// </summary>
    Task DeleteSessionAsync(string key, CancellationToken ct);


    /// <summary>
    /// Gets sessions for a specific subject id and/or session id
    /// </summary>
    Task<IReadOnlyCollection<ServerSideSession>> GetSessionsAsync(SessionFilter filter, CancellationToken ct);


    /// <summary>
    /// Deletes sessions for a specific subject id and/or session id
    /// </summary>
    Task DeleteSessionsAsync(SessionFilter filter, CancellationToken ct);


    /// <summary>
    /// Removes and returns expired sessions
    /// </summary>
    Task<IReadOnlyCollection<ServerSideSession>> GetAndRemoveExpiredSessionsAsync(int count, CancellationToken ct);


    /// <summary>
    /// Queries sessions based on filter
    /// </summary>
    Task<QueryResult<ServerSideSession>> QuerySessionsAsync(CancellationToken ct, SessionQuery? filter = null);
}
```

#### ServerSideSession

[Section titled "ServerSideSession"](#serversidesession)

```csharp
/// <summary>
/// A user session
/// </summary>
public class ServerSideSession
{
    /// <summary>
    /// The key
    /// </summary>
    public string Key { get; set; } = default!;


    /// <summary>
    /// The cookie handler scheme
    /// </summary>
    public string Scheme { get; set; } = default!;


    /// <summary>
    /// The subject ID
    /// </summary>
    public string SubjectId { get; set; } = default!;


    /// <summary>
    /// The session ID
    /// </summary>
    public string SessionId { get; set; } = default!;


    /// <summary>
    /// The display name for the user
    /// </summary>
    public string DisplayName { get; set; }


    /// <summary>
    /// The creation time
    /// </summary>
    public DateTime Created { get; set; }


    /// <summary>
    /// The renewal time
    /// </summary>
    public DateTime Renewed { get; set; }


    /// <summary>
    /// The expiration time
    /// </summary>
    public DateTime? Expires { get; set; }


    /// <summary>
    /// The serialized ticket
    /// </summary>
    public string Ticket { get; set; } = default!;
}
```

Note

The `Ticket` property contains a copy of all the values (and more) and is considered authoritative by IdentityServer, thus most of the other property values are considered informational and read-only.

#### SessionFilter

[Section titled "SessionFilter"](#sessionfilter)

```csharp
/// <summary>
/// Filter to query user sessions
/// </summary>
public class SessionFilter
{
    /// <summary>
    /// The subject ID
    /// </summary>
    public string SubjectId { get; init; }


    /// <summary>
    /// The sesion ID
    /// </summary>
    public string SessionId { get; init; }
}
```

#### SessionQuery

[Section titled "SessionQuery"](#sessionquery)

```csharp
/// <summary>
/// Filter to query all user sessions
/// </summary>
public class SessionQuery
{
    /// <summary>
    /// The token indicating the prior results.
    /// </summary>
    public string ResultsToken { get; set; }


    /// <summary>
    /// If true, requests the previous set of results relative to the ResultsToken, otherwise requests the next set of results relative to the ResultsToken.
    /// </summary>
    public bool RequestPriorResults { get; set; }


    /// <summary>
    /// The number requested to return
    /// </summary>
    public int CountRequested { get; set; }


    /// <summary>
    /// The subject ID used to filter the results.
    /// </summary>
    public string SubjectId { get; init; }


    /// <summary>
    /// The sesion ID used to filter the results.
    /// </summary>
    public string SessionId { get; init; }


    /// <summary>
    /// The user display name used to filter the results.
    /// </summary>
    public string DisplayName { get; init; }
}
```

#### QueryResult

[Section titled "QueryResult"](#queryresult)

```csharp
/// <summary>
/// Query result for paged data
/// </summary>
public class QueryResult<T>
{
    /// <summary>
    /// The token that indicates these results. This is used for more results in subsequent queries.
    /// If null, then there were no more results.
    /// </summary>
    public string ResultsToken { get; init; }


    /// <summary>
    /// True if there is a previous set of results.
    /// </summary>
    public bool HasPrevResults { get; set; }


    /// <summary>
    /// True if there is another set of results.
    /// </summary>
    public bool HasNextResults { get; set; }


    /// <summary>
    /// The total count (if available).
    /// </summary>
    public int? TotalCount { get; init; }


    /// <summary>
    /// The total pages (if available).
    /// </summary>
    public int? TotalPages { get; init; }


    /// <summary>
    /// The current (if available).
    /// </summary>
    public int? CurrentPage { get; init; }


    /// <summary>
    /// The results.
    /// </summary>
    public IReadOnlyCollection<T> Results { get; init; } = default!;
}
```
