# Schema Evolution and Buf CLI

**Load when:** Planning schema changes, maintaining backward compatibility, or using Buf tooling

## Table of Contents

- [Backward/Forward Compatibility](#backwardforward-compatibility)
- [Rules for Safe Evolution](#rules-for-safe-evolution)
- [Reserved Fields](#reserved-fields)
- [Buf CLI Integration](#buf-cli-integration)

## Backward/Forward Compatibility

### Version 1 - Initial Schema

```protobuf
message OrderV1 {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
}
```

### Version 2 - Adding Fields (Backward Compatible)

```protobuf
message OrderV2 {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  // NEW: Added in v2 - old clients ignore, new clients use default
  optional string notes = 4;
  repeated string tags = 5;
}
```

### Version 3 - Deprecating Fields

```protobuf
message OrderV3 {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  optional string notes = 4;
  repeated string tags = 5;
  // DEPRECATED: Use customer_id instead
  string customer_email = 6 [deprecated = true];
}
```

## Rules for Safe Evolution

| Action | Safe? | Notes |
|--------|-------|-------|
| Add field | ✅ | Use new field number |
| Remove field | ⚠️ | Use `reserved` to prevent reuse |
| Rename field | ✅ | Field number is what matters |
| Change field number | ❌ | Breaks wire compatibility |
| Change field type | ⚠️ | Some changes compatible |
| Reorder fields | ✅ | Order doesn't matter |

### Compatible Type Changes

| From | To | Notes |
|------|-----|-------|
| int32 | int64 | Safe (widening) |
| uint32 | uint64 | Safe (widening) |
| int32 | uint32 | ⚠️ Only if values non-negative |
| string | bytes | ✅ If valid UTF-8 |
| enum | int32 | ✅ Wire compatible |

## Reserved Fields

```protobuf
message Order {
  reserved 6, 15, 100 to 200;
  reserved "old_field", "deprecated_field";

  string id = 1;
  // Field 6 was removed, reserved to prevent accidental reuse
}
```

**Why reserve?** Prevents accidental reuse of field numbers, which would break existing serialized data.

## Buf CLI Integration

### buf.yaml

```yaml
version: v2
lint:
  use:
    - DEFAULT
  except:
    - PACKAGE_VERSION_SUFFIX
breaking:
  use:
    - FILE
```

### buf.gen.yaml

```yaml
version: v2
plugins:
  - remote: buf.build/grpc/csharp
    out: gen/csharp
  - remote: buf.build/protocolbuffers/csharp
    out: gen/csharp
```

### Commands

```bash
# Lint proto files
buf lint

# Check breaking changes
buf breaking --against '.git#branch=main'

# Generate code
buf generate

# Format proto files
buf format -w
```

## Best Practices

### API Design Guidelines

1. **Use resource-oriented design**: `GetOrder`, `ListOrders`, `CreateOrder`
2. **Include unspecified enum value at 0**: Handles unknown values gracefully
3. **Use wrappers for optional primitives**: `google.protobuf.StringValue`
4. **Version your packages**: `v1`, `v1beta1`, `v2`
5. **Keep messages focused**: Single responsibility per message
6. **Document with comments**: Use `//` for documentation

### Naming Conventions

```protobuf
// Package: lowercase with dots
package ecommerce.orders.v1;

// Service: PascalCase with "Service" suffix
service OrderService {}

// Method: PascalCase verb phrase
rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

// Message: PascalCase
message OrderCreatedEvent {}

// Field: snake_case
string customer_id = 1;

// Enum: SCREAMING_SNAKE_CASE with prefix
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_DRAFT = 1;
}
```
