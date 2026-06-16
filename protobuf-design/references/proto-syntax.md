# Proto3 Syntax Reference

**Load when:** Creating protobuf definitions, using well-known types, or implementing advanced patterns

## Table of Contents

- [Basic Structure](#basic-structure)
- [Well-Known Types](#well-known-types)
- [Advanced Patterns](#advanced-patterns)

## Basic Structure

```protobuf
// order_service.proto
syntax = "proto3";

package ecommerce.orders.v1;

option csharp_namespace = "ECommerce.Orders.V1";
option java_package = "com.ecommerce.orders.v1";
option go_package = "github.com/ecommerce/orders/v1;ordersv1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";

// Order service definition
service OrderService {
  // Create a new order
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

  // Get order by ID
  rpc GetOrder(GetOrderRequest) returns (Order);

  // List orders with pagination
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);

  // Submit order for processing
  rpc SubmitOrder(SubmitOrderRequest) returns (Order);

  // Cancel an order
  rpc CancelOrder(CancelOrderRequest) returns (Order);

  // Stream order status updates
  rpc WatchOrderStatus(WatchOrderStatusRequest) returns (stream OrderStatusUpdate);
}

// Enumerations
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_DRAFT = 1;
  ORDER_STATUS_SUBMITTED = 2;
  ORDER_STATUS_PAID = 3;
  ORDER_STATUS_SHIPPED = 4;
  ORDER_STATUS_DELIVERED = 5;
  ORDER_STATUS_CANCELLED = 6;
}

// Messages
message Order {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  repeated LineItem items = 4;
  Money subtotal = 5;
  Money tax = 6;
  Money total = 7;
  google.protobuf.Timestamp created_at = 8;
  google.protobuf.Timestamp updated_at = 9;
  optional string tracking_number = 10;
}

message LineItem {
  string id = 1;
  string product_id = 2;
  string product_name = 3;
  int32 quantity = 4;
  Money unit_price = 5;
  Money line_total = 6;
}

message Money {
  int64 units = 1;      // Whole units (e.g., dollars)
  int32 nanos = 2;      // Nano units (10^-9)
  string currency = 3;  // ISO 4217 currency code
}

// Request/Response messages
message CreateOrderRequest {
  string customer_id = 1;
  repeated CreateLineItemRequest items = 2;
}

message CreateLineItemRequest {
  string product_id = 1;
  int32 quantity = 2;
}

message CreateOrderResponse {
  Order order = 1;
}

message GetOrderRequest {
  string id = 1;
}

message ListOrdersRequest {
  int32 page_size = 1;
  string page_token = 2;
  optional string customer_id = 3;
  optional OrderStatus status = 4;
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
  int32 total_count = 3;
}

message SubmitOrderRequest {
  string id = 1;
}

message CancelOrderRequest {
  string id = 1;
  optional string reason = 2;
}

message WatchOrderStatusRequest {
  string order_id = 1;
}

message OrderStatusUpdate {
  string order_id = 1;
  OrderStatus previous_status = 2;
  OrderStatus current_status = 3;
  google.protobuf.Timestamp timestamp = 4;
  optional string message = 5;
}
```

## Well-Known Types

```protobuf
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/any.proto";
import "google/protobuf/struct.proto";
import "google/protobuf/empty.proto";
import "google/protobuf/field_mask.proto";

message Example {
  // Timestamp for date/time
  google.protobuf.Timestamp created_at = 1;

  // Duration for time spans
  google.protobuf.Duration timeout = 2;

  // Wrappers for nullable primitives
  google.protobuf.StringValue optional_name = 3;
  google.protobuf.Int32Value optional_count = 4;
  google.protobuf.BoolValue optional_flag = 5;

  // Any for dynamic typing
  google.protobuf.Any payload = 6;

  // Struct for JSON-like data
  google.protobuf.Struct metadata = 7;

  // FieldMask for partial updates
  google.protobuf.FieldMask update_mask = 8;
}
```

## Advanced Patterns

### Oneof (Union Types)

```protobuf
message PaymentMethod {
  oneof method {
    CreditCard credit_card = 1;
    BankAccount bank_account = 2;
    PayPalAccount paypal = 3;
  }
}

message CreditCard {
  string number = 1;
  string expiry = 2;
  string cvv = 3;
}

message BankAccount {
  string routing_number = 1;
  string account_number = 2;
}

message PayPalAccount {
  string email = 1;
}
```

### Maps

```protobuf
message Product {
  string id = 1;
  string name = 2;
  map<string, string> attributes = 3;  // key-value attributes
  map<string, Money> prices_by_region = 4;
}
```

### Nested Messages

```protobuf
message Customer {
  string id = 1;
  string email = 2;

  message Address {
    string street = 1;
    string city = 2;
    string state = 3;
    string postal_code = 4;
    string country = 5;
  }

  Address shipping_address = 3;
  Address billing_address = 4;
}
```
