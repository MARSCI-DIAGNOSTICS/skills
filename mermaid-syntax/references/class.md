# Class Diagram Syntax

Class diagrams show object-oriented structures and relationships.

## Basic Class Definition

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
        -sleep() void
        #eat(food) bool
    }
```

## Visibility Modifiers

| Symbol | Meaning |
| --- | --- |
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

## Relationships

```mermaid
classDiagram
    Animal <|-- Dog : Inheritance
    Animal <|-- Cat : Inheritance
    Dog *-- Leg : Composition
    Dog o-- Toy : Aggregation
    Dog --> Food : Association
    Dog ..> Water : Dependency
    Dog ..|> Mammal : Realization
```

| Syntax | Relationship |
| --- | --- |
| `<\|--` | Inheritance |
| `*--` | Composition |
| `o--` | Aggregation |
| `-->` | Association |
| `..>` | Dependency |
| `..\|>` | Realization |

## Cardinality

```mermaid
classDiagram
    Customer "1" --> "*" Order : places
    Order "1" --> "1..*" LineItem : contains
```

## Complete Example

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String passwordHash
        +Date createdAt
        +authenticate(password) bool
        +updateProfile(data) void
    }

    class Order {
        +String id
        +Date orderDate
        +OrderStatus status
        +calculateTotal() Decimal
        +cancel() void
    }

    class OrderItem {
        +String productId
        +int quantity
        +Decimal price
    }

    class Product {
        +String id
        +String name
        +Decimal price
        +int stock
    }

    User "1" --> "*" Order : places
    Order "1" *-- "*" OrderItem : contains
    OrderItem "*" --> "1" Product : references
```
