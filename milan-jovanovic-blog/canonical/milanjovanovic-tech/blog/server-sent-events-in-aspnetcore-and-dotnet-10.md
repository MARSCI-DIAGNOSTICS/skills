---
doc_id: milanjovanovic-tech-blog-server-sent-events-in-aspnetcore-and-dotnet-10
title: "Server-Sent Events in ASP.NET Core and .NET 10"
description: "ASP.NET Core 10 introduces native Server-Sent Events as a lightweight, HTTP-native alternative to SignalR for simple one-way real-time updates like dashboards and notifications."
source_url: https://www.milanjovanovic.tech/blog/server-sent-events-in-aspnetcore-and-dotnet-10
published_at: "2025-12-20"
author: Milan Jovanović
---

# Server-Sent Events in ASP.NET Core and .NET 10

**Real-time updates** are no longer a "nice-to-have" feature.
Most modern UI applications expect live data streams of some kind from the server.
For years, the go-to answer in the .NET ecosystem has been **SignalR**.
While SignalR is incredibly powerful, it's _nice to have_ other **options** for simpler use cases.

With the release of ASP.NET Core 10, we finally have a native, high-level API for **Server-Sent Events** (SSE).
It bridges the gap between basic HTTP polling and full-duplex WebSockets via SignalR.

## Why SSE Instead of SignalR?

SignalR is a powerhouse that handles WebSockets, Long Polling, and SSE automatically, providing a full-duplex (**two-way**) communication channel.
However, it comes with a footprint: a specific protocol (Hubs), a required client-side library, and a need for "sticky sessions" or a backplane (like Redis) for scaling.

SSE is different because:

- **Unidirectional**: It's designed **specifically** for streaming data **from the server to the client**.
- **Native HTTP**: It's just a standard HTTP request with a `text/event-stream` content type. No custom protocols.
- **Automatic Reconnection**: Browsers natively handle reconnections via the **EventSource** API.
- **Lightweight**: No heavy client libraries or complex handshake logic.

## The Simplest Server-Sent Events Endpoint

The beauty of the .NET 10 SSE API is its simplicity.
You can use the new `Results.ServerSentEvents` to return a stream of events from any `IAsyncEnumerable<T>`.
Because `IAsyncEnumerable` represents a stream of data that can arrive over time,
the server knows to keep the HTTP connection open rather than closing it after the first "chunk" of data.

Here's a minimal example of an SSE endpoint that streams order placements in real-time:

```csharp
app.MapGet("orders/realtime", (
	ChannelReader<OrderPlacement> channelReader,
	CancellationToken cancellationToken) =>
{
	// 1. ReadAllAsync returns an IAsyncEnumerable
	// 2. Results.ServerSentEvents tells the browser: "Keep this connection open"
	// 3. New data is pushed to the client as soon as it enters the channel
	return Results.ServerSentEvents(
        channelReader.ReadAllAsync(cancellationToken),
        eventType: "orders");
});
```

When a client hits this endpoint:

1. The server sends a `Content-Type: text/event-stream` header.
2. The connection stays active and idle while waiting for data.
3. As soon as your application pushes an order into the `Channel`, the `IAsyncEnumerable` yields that item,
and .NET immediately flushes it down the open HTTP pipe to the browser.

It's an incredibly efficient way to handle "push" notifications without the overhead of a stateful protocol.

I'm using a **`Channel`** here as a means to an end.
In a real application, you might have a **background service**
that listens to a message queue (like RabbitMQ or Azure Service Bus)
or a database change feed, and pushes new events into the channel for connected clients to consume.

## Handling Missed Events

The simple endpoint we just built is great, but it has one weakness: it's missing resilience.

One of the biggest challenges with real-time streams is connection drops.
By the time the browser automatically reconnects, several events might have already been sent and lost.
To solve this, SSE has a built-in mechanism: the `Last-Event-ID` **header**.
When a browser reconnects, it sends this ID back to the server.

In .NET 10, we can use the `SseItem<T>` type to wrap our data with metadata like IDs and retry intervals.

By combining a simple in-memory **OrderEventBuffer** with the **Last-Event-ID** provided by the browser, we can "replay" missed messages upon reconnection:

```csharp
app.MapGet("orders/realtime/with-replays", (
	ChannelReader<OrderPlacement> channelReader,
	OrderEventBuffer eventBuffer,
	[FromHeader(Name = "Last-Event-ID")] string? lastEventId,
	CancellationToken cancellationToken) =>
{
	async IAsyncEnumerable<SseItem<OrderPlacement>> StreamEvents()
	{
		// 1. Replay missed events from the buffer
		if (!string.IsNullOrWhiteSpace(lastEventId))
		{
			var missedEvents = eventBuffer.GetEventsAfter(lastEventId);
			foreach (var missedEvent in missedEvents)
			{
				yield return missedEvent;
			}
		}

		// 2. Stream new events as they arrive in the Channel
		await foreach (var order in channelReader.ReadAllAsync(cancellationToken))
		{
			var sseItem = eventBuffer.Add(order); // Buffer assigns a unique ID
			yield return sseItem;
		}
	}

	return TypedResults.ServerSentEvents(StreamEvents(), "orders");
});
```

## Filtering Server-Sent Events by User

Server-Sent Events is built on top of standard HTTP.
Because it is a standard `GET` request, your existing infrastructure "just works":

- **Security**: You can pass a standard JWT in the `Authorization` header.
- **User Context**: You can access `HttpContext.User` to extract a User ID and filter the stream.
You only send a user the data that belongs to them.

Here's an example of an SSE endpoint that streams only the orders for the authenticated user:

```csharp
app.MapGet("orders/realtime", (
	ChannelReader<OrderPlacement> channelReader,
	IUserContext userContext, // Injected context containing user metadata
	CancellationToken cancellationToken) =>
{
	// The UserId is extracted from the JWT access token by the IUserContext
	var currentUserId = userContext.UserId;

	async IAsyncEnumerable<OrderPlacement> GetUserOrders()
	{
		await foreach (var order in channelReader.ReadAllAsync(cancellationToken))
		{
			// We only yield data that belongs to the authenticated user
			if (order.CustomerId == currentUserId)
			{
				yield return order;
			}
		}
	}

	return Results.ServerSentEvents(GetUserOrders(), "orders");
})
.RequireAuthorization(); // Standard ASP.NET Core Authorization
```

Note that when you write a message to a `Channel` it's broadcast to **all** connected clients.
This isn't ideal for per-user streams.
You'll probably want to use something more robust for production.

## Consuming Server-Sent Events in JavaScript

On the client side, you don't need to install a single npm package.
The browser's native `EventSource` API handles the heavy lifting, including the "reconnect and send Last-Event-ID" logic we discussed above.

```javascript
const eventSource = new EventSource('/orders/realtime/with-replays');

// Listen for the specific 'orders' event type we defined in C#
eventSource.addEventListener('orders', (event) => {
  const payload = JSON.parse(event.data);
  console.log(`New Order ${event.lastEventId}:`, payload.data);
});

// Do something when the connection opens
eventSource.onopen = () => {
  console.log('Connection opened');
};

// Handle generic messages (if any)
eventSource.onmessage = (event) => {
  console.log('Received message:', event);
};

// Handle errors and reconnections
eventSource.onerror = () => {
  if (eventSource.readyState === EventSource.CONNECTING) {
    console.log('Reconnecting...');
  }
};
```

## Summary

SSE in .NET 10 is the perfect middle ground for simple, one-way updates like dashboards, notification bells, and progress bars.
It's lightweight, HTTP-native, and easy to secure using your existing middleware.

However, **SignalR** remains the robust, battle-tested choice for complex bi-directional communication or massive scale requiring a backplane.

The goal isn't to replace SignalR, but to give you a simpler tool for simpler jobs.
Choose the lightest tool that solves your problem.
