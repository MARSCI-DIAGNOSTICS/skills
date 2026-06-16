---
title: Session Management
source_url: https://docs.duendesoftware.com/identityserver/ui/server-side-sessions/session-management/
source_type: llms-full-txt
content_hash: sha256:b36f29ce3f8e9bbf2928c7cafd4bbc635ca4e28661ddd8875a0f6f262ef0265b
doc_id: identityserver/ui/server-side-sessions/session-management
---

> Configure and implement custom server-side session storage and lifecycle management through IUserSessionStore interface

Server-side sessions enable secure and efficient storage of session data, allowing flexibility through custom implementations of the `IUserSessionStore` interface. This ensures adaptability to various storage solutions tailored to your application's needs.

## User Session Store

[Section titled "User Session Store"](#user-session-store)

If using the server-side sessions feature, you will need to have a store for the session data. An Entity Framework Core based implementation of this store is provided.

If you wish to use some other type of store, can implement the `IUserSessionStore` interface:

* Duende BFF v4

  ```csharp
  /// <summary>
  /// User session store
  /// </summary>
  public interface IUserSessionStore
  {
      /// <summary>
      /// Retrieves a user session
      /// </summary>
      /// <param name="key"></param>
      /// <param name="ct">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task<UserSession?> GetUserSessionAsync(UserSessionKey key, CT ct = default);


      /// <summary>
      /// Creates a user session
      /// </summary>
      /// <param name="session"></param>
      /// <param name="ct">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task CreateUserSessionAsync(UserSession session, CT ct = default);


      /// <summary>
      /// Updates a user session
      /// </summary>
      /// <param name="key"></param>
      /// <param name="session"></param>
      /// <param name="ct">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task UpdateUserSessionAsync(UserSessionKey key, UserSessionUpdate session, CT ct = default);


      /// <summary>
      /// Deletes a user session
      /// </summary>
      /// <param name="key"></param>
      /// <param name="ct">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task DeleteUserSessionAsync(UserSessionKey key, CT ct = default);


      /// <summary>
      /// Queries user sessions based on the filter.
      /// </summary>
      /// <param name="partitionKey">The partition key to use</param>
      /// <param name="filter"></param>
      /// <param name="ct">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task<IReadOnlyCollection<UserSession>> GetUserSessionsAsync(PartitionKey partitionKey, UserSessionsFilter filter, CT ct = default);


      /// <summary>
      /// Deletes user sessions based on the filter.
      /// </summary>
      /// <param name="partitionKey">The partition key</param>
      /// <param name="filter"></param>
      /// <param name="ct">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task DeleteUserSessionsAsync(PartitionKey partitionKey, UserSessionsFilter filter, CT ct = default);
  }
  ```

  Do not store `UserSession` directly

  Your `IUserSessionStore` implementation is expected to implement custom code to roundtrip the data from the user session to the underlying storage mechanism. You should not rely on existing serializers, such as `System.Text.Json` or `Newtonsoft.Json`, to serialize the `UserSession` object.

* Duende BFF v3

  ```csharp
  /// <summary>
  /// User session store
  /// </summary>
  public interface IUserSessionStore
  {
      /// <summary>
      /// Retrieves a user session
      /// </summary>
      /// <param name="key"></param>
      /// <param name="cancellationToken">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task<UserSession?> GetUserSessionAsync(string key, CancellationToken cancellationToken = default);


      /// <summary>
      /// Creates a user session
      /// </summary>
      /// <param name="session"></param>
      /// <param name="cancellationToken">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task CreateUserSessionAsync(UserSession session, CancellationToken cancellationToken = default);


      /// <summary>
      /// Updates a user session
      /// </summary>
      /// <param name="key"></param>
      /// <param name="session"></param>
      /// <param name="cancellationToken">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task UpdateUserSessionAsync(string key, UserSessionUpdate session, CancellationToken cancellationToken = default);


      /// <summary>
      /// Deletes a user session
      /// </summary>
      /// <param name="key"></param>
      /// <param name="cancellationToken">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task DeleteUserSessionAsync(string key, CancellationToken cancellationToken = default);


      /// <summary>
      /// Queries user sessions based on the filter.
      /// </summary>
      /// <param name="filter"></param>
      /// <param name="cancellationToken">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task<IReadOnlyCollection<UserSession>> GetUserSessionsAsync(UserSessionsFilter filter, CancellationToken cancellationToken = default);


      /// <summary>
      /// Deletes user sessions based on the filter.
      /// </summary>
      /// <param name="filter"></param>
      /// <param name="cancellationToken">A token that can be used to request cancellation of the asynchronous operation.</param>
      /// <returns></returns>
      Task DeleteUserSessionsAsync(UserSessionsFilter filter, CancellationToken cancellationToken = default);
  }
  ```

Once you have an implementation, you can register it when you enable server-side sessions:

Program.cs

```csharp
builder.Services.AddBff()
    .AddServerSideSessions<YourStoreClassName>();
```

## User Session Store Cleanup

[Section titled "User Session Store Cleanup"](#user-session-store-cleanup)

The `IUserSessionStoreCleanup` interface is used to model cleaning up expired sessions.

```csharp
/// <summary>
/// User session store cleanup
/// </summary>
public interface IUserSessionStoreCleanup
{
    /// <summary>
    /// Deletes expired sessions
    /// </summary>
    Task DeleteExpiredSessionsAsync(CancellationToken cancellationToken = default);
}
```
