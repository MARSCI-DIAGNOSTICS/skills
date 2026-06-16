# C# gRPC Implementation

**Load when:** Implementing gRPC services in .NET/C#

## Table of Contents

- [Generated Client Usage](#generated-client-usage)
- [Server Implementation](#server-implementation)
- [ASP.NET Core Registration](#aspnet-core-registration)
- [Project Configuration](#project-configuration)

## Generated Client Usage

```csharp
using ECommerce.Orders.V1;
using Grpc.Net.Client;

public sealed class OrderClient
{
    private readonly OrderService.OrderServiceClient _client;

    public OrderClient(string address)
    {
        var channel = GrpcChannel.ForAddress(address);
        _client = new OrderService.OrderServiceClient(channel);
    }

    public async Task<Order> CreateOrderAsync(
        string customerId,
        IEnumerable<(string ProductId, int Quantity)> items,
        CancellationToken ct = default)
    {
        var request = new CreateOrderRequest
        {
            CustomerId = customerId,
            Items = { items.Select(i => new CreateLineItemRequest
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity
            })}
        };

        var response = await _client.CreateOrderAsync(request, cancellationToken: ct);
        return response.Order;
    }

    public async Task<Order> GetOrderAsync(string id, CancellationToken ct = default)
    {
        var request = new GetOrderRequest { Id = id };
        return await _client.GetOrderAsync(request, cancellationToken: ct);
    }

    public async IAsyncEnumerable<OrderStatusUpdate> WatchStatusAsync(
        string orderId,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        var request = new WatchOrderStatusRequest { OrderId = orderId };
        using var call = _client.WatchOrderStatus(request, cancellationToken: ct);

        await foreach (var update in call.ResponseStream.ReadAllAsync(ct))
        {
            yield return update;
        }
    }
}
```

## Server Implementation

```csharp
using ECommerce.Orders.V1;
using Grpc.Core;

public sealed class OrderServiceImpl : OrderService.OrderServiceBase
{
    private readonly IOrderRepository _orders;
    private readonly ILogger<OrderServiceImpl> _logger;

    public OrderServiceImpl(
        IOrderRepository orders,
        ILogger<OrderServiceImpl> logger)
    {
        _orders = orders;
        _logger = logger;
    }

    public override async Task<CreateOrderResponse> CreateOrder(
        CreateOrderRequest request,
        ServerCallContext context)
    {
        var order = Domain.Order.Create(
            request.CustomerId,
            request.Items.Select(i => new Domain.LineItem(i.ProductId, i.Quantity)));

        await _orders.AddAsync(order, context.CancellationToken);

        return new CreateOrderResponse { Order = MapToProto(order) };
    }

    public override async Task<Order> GetOrder(
        GetOrderRequest request,
        ServerCallContext context)
    {
        var order = await _orders.GetByIdAsync(request.Id, context.CancellationToken);

        if (order is null)
        {
            throw new RpcException(new Status(
                StatusCode.NotFound,
                $"Order {request.Id} not found"));
        }

        return MapToProto(order);
    }

    public override async Task<ListOrdersResponse> ListOrders(
        ListOrdersRequest request,
        ServerCallContext context)
    {
        var (orders, nextToken, total) = await _orders.ListAsync(
            pageSize: request.PageSize,
            pageToken: request.PageToken,
            customerId: request.HasCustomerId ? request.CustomerId : null,
            status: request.HasStatus ? MapToDomain(request.Status) : null,
            ct: context.CancellationToken);

        return new ListOrdersResponse
        {
            Orders = { orders.Select(MapToProto) },
            NextPageToken = nextToken ?? "",
            TotalCount = total
        };
    }

    public override async Task WatchOrderStatus(
        WatchOrderStatusRequest request,
        IServerStreamWriter<OrderStatusUpdate> responseStream,
        ServerCallContext context)
    {
        await foreach (var update in _orders.WatchStatusAsync(
            request.OrderId,
            context.CancellationToken))
        {
            await responseStream.WriteAsync(new OrderStatusUpdate
            {
                OrderId = update.OrderId,
                PreviousStatus = MapToProto(update.PreviousStatus),
                CurrentStatus = MapToProto(update.CurrentStatus),
                Timestamp = Timestamp.FromDateTimeOffset(update.Timestamp),
                Message = update.Message ?? ""
            });
        }
    }

    private static Order MapToProto(Domain.Order order) =>
        new()
        {
            Id = order.Id.ToString(),
            CustomerId = order.CustomerId.ToString(),
            Status = MapToProto(order.Status),
            Items = { order.Items.Select(MapToProto) },
            Subtotal = MapToProto(order.Subtotal),
            Tax = MapToProto(order.Tax),
            Total = MapToProto(order.Total),
            CreatedAt = Timestamp.FromDateTimeOffset(order.CreatedAt),
            UpdatedAt = Timestamp.FromDateTimeOffset(order.UpdatedAt),
            TrackingNumber = order.TrackingNumber ?? ""
        };

    private static LineItem MapToProto(Domain.LineItem item) =>
        new()
        {
            Id = item.Id.ToString(),
            ProductId = item.ProductId.ToString(),
            ProductName = item.ProductName,
            Quantity = item.Quantity,
            UnitPrice = MapToProto(item.UnitPrice),
            LineTotal = MapToProto(item.LineTotal)
        };

    private static Money MapToProto(Domain.Money money) =>
        new()
        {
            Units = (long)money.Amount,
            Nanos = (int)((money.Amount - (long)money.Amount) * 1_000_000_000),
            Currency = money.Currency
        };

    private static OrderStatus MapToProto(Domain.OrderStatus status) =>
        status switch
        {
            Domain.OrderStatus.Draft => OrderStatus.Draft,
            Domain.OrderStatus.Submitted => OrderStatus.Submitted,
            Domain.OrderStatus.Paid => OrderStatus.Paid,
            Domain.OrderStatus.Shipped => OrderStatus.Shipped,
            Domain.OrderStatus.Delivered => OrderStatus.Delivered,
            Domain.OrderStatus.Cancelled => OrderStatus.Cancelled,
            _ => OrderStatus.Unspecified
        };

    private static Domain.OrderStatus MapToDomain(OrderStatus status) =>
        status switch
        {
            OrderStatus.Draft => Domain.OrderStatus.Draft,
            OrderStatus.Submitted => Domain.OrderStatus.Submitted,
            OrderStatus.Paid => Domain.OrderStatus.Paid,
            OrderStatus.Shipped => Domain.OrderStatus.Shipped,
            OrderStatus.Delivered => Domain.OrderStatus.Delivered,
            OrderStatus.Cancelled => Domain.OrderStatus.Cancelled,
            _ => throw new ArgumentOutOfRangeException(nameof(status))
        };
}
```

## ASP.NET Core Registration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddGrpc();
builder.Services.AddGrpcReflection(); // For tooling like grpcurl

var app = builder.Build();

app.MapGrpcService<OrderServiceImpl>();
app.MapGrpcReflectionService();

app.Run();
```

## Project Configuration

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <Protobuf Include="Protos\**\*.proto" GrpcServices="Server" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Grpc.AspNetCore" Version="2.71.0" />
    <PackageReference Include="Google.Protobuf" Version="3.29.3" />
  </ItemGroup>
</Project>
```

**Note:** Package versions are current as of January 2026. Verify latest versions via NuGet.
