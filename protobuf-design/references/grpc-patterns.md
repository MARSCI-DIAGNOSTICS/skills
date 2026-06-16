# gRPC Service Patterns

**Load when:** Designing gRPC services with streaming patterns

## Table of Contents

- [RPC Types](#rpc-types)
- [Pattern Examples](#pattern-examples)
- [When to Use Each Pattern](#when-to-use-each-pattern)

## RPC Types

### Unary RPC

```protobuf
// Simple request-response
rpc GetOrder(GetOrderRequest) returns (Order);
```

**Use for:** Single request, single response operations.

### Server Streaming

```protobuf
// Server sends multiple responses
rpc ListOrderHistory(ListOrderHistoryRequest) returns (stream Order);
```

**Use for:** Large result sets, real-time updates, notifications.

### Client Streaming

```protobuf
// Client sends multiple requests
rpc BatchCreateOrders(stream CreateOrderRequest) returns (BatchCreateResponse);
```

**Use for:** Batch uploads, file uploads, aggregated data collection.

### Bidirectional Streaming

```protobuf
// Both client and server stream
rpc OrderChat(stream OrderMessage) returns (stream OrderMessage);
```

**Use for:** Chat applications, collaborative editing, real-time sync.

## Pattern Examples

### Pagination with Server Streaming

```protobuf
service OrderService {
  // Stream all orders matching criteria
  rpc StreamOrders(StreamOrdersRequest) returns (stream Order);
}

message StreamOrdersRequest {
  optional string customer_id = 1;
  optional OrderStatus status = 2;
}
```

### Real-Time Status Updates

```protobuf
service OrderService {
  // Watch for status changes
  rpc WatchOrderStatus(WatchOrderStatusRequest) returns (stream OrderStatusUpdate);
}

message WatchOrderStatusRequest {
  string order_id = 1;
}

message OrderStatusUpdate {
  string order_id = 1;
  OrderStatus previous_status = 2;
  OrderStatus current_status = 3;
  google.protobuf.Timestamp timestamp = 4;
}
```

### Batch Processing with Client Streaming

```protobuf
service ImportService {
  // Import multiple records
  rpc ImportRecords(stream ImportRecord) returns (ImportResult);
}

message ImportRecord {
  string id = 1;
  bytes data = 2;
}

message ImportResult {
  int32 total_processed = 1;
  int32 successful = 2;
  int32 failed = 3;
  repeated ImportError errors = 4;
}
```

## When to Use Each Pattern

| Pattern | Use Case | Example |
|---------|----------|---------|
| Unary | Simple CRUD operations | GetOrder, CreateOrder |
| Server Streaming | Large data, real-time updates | ListOrders, WatchStatus |
| Client Streaming | Batch uploads, aggregation | BatchImport, FileUpload |
| Bidirectional | Chat, collaborative, real-time sync | LiveChat, Collaboration |
