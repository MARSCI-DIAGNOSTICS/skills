---
doc_id: milanjovanovic-tech-blog-vertical-slice-architecture-where-does-the-shared-logic-live
title: "Vertical Slice Architecture: Where Does the Shared Logic Live?"
description: "Deciding where shared logic lives is the most critical moment in Vertical Slice Architecture adoption, as choosing incorrectly reintroduces the coupling the architecture aims to eliminate. This article proposes a three-tier approach to sharing code that balances technical infrastructure, domain concepts, and local feature logic."
source_url: https://www.milanjovanovic.tech/blog/vertical-slice-architecture-where-does-the-shared-logic-live
published_at: "2025-11-29"
author: Milan Jovanović
---

# Vertical Slice Architecture: Where Does the Shared Logic Live?

**Vertical Slice Architecture** (VSA) seems like a breath of fresh air when you first encounter it.
You stop jumping between seven layers to add a single field.
You delete the dozens of projects in your solution.
You feel liberated.

But when you start implementing more complex features, the cracks begin to show.

You build a `CreateOrder` slice.
Then `UpdateOrder`.
Then `GetOrder`.
Suddenly, you notice the repetition.
The address validation logic is in three places.
The pricing algorithm is needed by both Cart and Checkout.

You feel the urge to create a `Common` project or `SharedServices` folder.
This is the most critical moment in your VSA adoption.

Choose wrong, and you'll reintroduce the coupling you were trying to escape.
Choose right, and you maintain the independence that makes VSA worthwhile.

Here's how I approach **shared code** in **Vertical Slice Architecture**.

## The Guardrails vs. The Open Road

To understand why this is hard, we need to look at what we left behind.

**Clean Architecture** provides strict guardrails.
It tells you exactly where code lives: Entities go in Domain, interfaces go in Application, implementations go in Infrastructure.
It's safe.
It prevents mistakes, but it also prevents shortcuts when they're appropriate.

**Vertical Slice Architecture** removes the guardrails.
It says, "Organize code by feature, not technical concern".
This gives you speed and flexibility, but it shifts the burden of discipline onto _you_.

So what can you do about it?

## The Trap: The "Common" Junk Drawer

The path of least resistance is to create a project (or folder) named `Shared`, `Common`, or `Utils`.

This is almost always a mistake.

Imagine a `Common.Services` project with an `OrderCalculationService` class.
It has a method for cart totals (used by Cart), another for historical revenue (used by Reporting),
and a helper for invoice formatting (used by Invoices).
Three unrelated concerns.
Three different change frequencies.
One class coupling them all together.

A `Common` project inevitably becomes a junk drawer for anything you can't be bothered to name properly.
It creates a tangled web of dependencies where unrelated features are coupled together because they happen to use the same helper method.

You've reintroduced the very coupling you tried to escape.

## The Decision Framework

When I hit a potential sharing situation, I ask three questions:

**1. Is this infrastructural or domain?**

Infrastructure (database contexts, logging, HTTP clients) almost always gets shared. Domain concepts need more scrutiny.

**2. How stable is this concept?**

If it changes once a year, share it. If it changes with every feature request, keep it local.

**3. Am I past the "Rule of Three"?**

Duplicating the same code once is fine.
However, creating three duplicates should raise an eyebrow.
Don't abstract until you hit three.

We solve this by refactoring our code.
Let's look at some examples.

## The Three Tiers of Sharing

Instead of binary "Shared vs. Not Shared," think in three tiers.

### Tier 1: Technical Infrastructure (Share Freely)

Pure plumbing that affects all slices equally: logging adapters, database connection factories, auth middleware,
the **Result pattern**, validation pipelines.

Centralize this in a `Shared.Kernel` or `Infrastructure` project.
Note that this can also be a folder within your solution.
It rarely changes due to business requirements.

```csharp
// ✅ Good Sharing: Technical Kernel
public readonly record struct Result
{
    public bool IsSuccess { get; }
    public string Error { get; }

    private Result(bool isSuccess, string error)
    {
        IsSuccess = isSuccess;
        Error = error;
    }

    public static Result Success() => new(true, string.Empty);
    public static Result Failure(string error) => new(false, error);
}
```

### Tier 2: Domain Concepts (Share and Push Logic Down)

This is one of the best places to share logic.
Instead of scattering business rules across slices, push them into entities and value objects.

Here's an example:

```csharp
// ✅ Good Sharing: Entity with Business Logic
public class Order
{
    public Guid Id { get; private set; }
    public OrderStatus Status { get; private set; }
    public List<OrderLine> Lines { get; private set; }

    public bool CanBeCancelled() => Status == OrderStatus.Pending;

    public Result Cancel()
    {
        if (!CanBeCancelled())
        {
            return Result.Failure("Only pending orders can be cancelled.");
        }

        Status = OrderStatus.Cancelled;
        return Result.Success();
    }
}
```

Now `CancelOrder`, `GetOrder`, and `UpdateOrder` all use the same business rules.
The logic lives in one place.

This implies an important concept: **different vertical slices can share the same domain model.**

### Tier 3: Feature-Specific Logic (Keep It Local)

Logic shared between related slices, like `CreateOrder` and `UpdateOrder`, doesn't need to go global.
Create a `Shared` folder (there's an exception to every rule) within the feature:

```
📂 Features
└──📂 Orders
    ├──📂 CreateOrder
    ├──📂 UpdateOrder
    ├──📂 GetOrder
    └──📂 Shared
        ├──📄 OrderValidator.cs
        └──📄 OrderPricingService.cs
```

This also has a hidden benefit.
If you delete the Orders feature, the shared logic goes with it.
No zombie code left behind.

Let's explore some advanced scenarios most people overlook.

## Cross-Feature Sharing

What about **sharing code between unrelated features** in Vertical Slice Architecture?

The `CreateOrder` slice needs to check if a customer exists.
`GenerateInvoice` needs to calculate tax.
Orders and Customers both need to format notification messages.

This doesn't fit neatly into a feature's `Shared` folder.
So where does it go?

**First, ask: do you actually need to share?**

Most cross-feature "sharing" is just data access in disguise.

If `CreateOrder` needs customer data, it queries the database directly.
It doesn't call into the Customers feature.
Each slice owns its data access.
The `Customer` entity is shared (it lives in `Domain`), but there's no shared service between them.

**When you genuinely need shared logic**, ask what it _is_:

- **Domain logic** (business rules, calculations) → `Domain/Services`
- **Infrastructure** (external APIs, formatting) → `Infrastructure/Services`

```csharp
// Domain/Services/TaxCalculator.cs
public class TaxCalculator
{
    public decimal CalculateTax(Address address, decimal subtotal)
    {
        var rate = GetTaxRate(address.State, address.Country);
        return subtotal * rate;
    }
}
```

Both `CreateOrder` and `GenerateInvoice` can use it without coupling to each other.

Before creating any cross-feature service, ask: could this logic live on a domain entity instead?
Most "shared business logic" is actually data access, domain logic that belongs on an entity, or premature abstraction.

If you need to trigger a side effect in another feature, I recommend using **messaging and events**.
Alternatively, the feature you want to call into can expose a facade (**public API**) for that operation.

## When Duplication Is the Right Call

Sometimes "shared" code isn't actually shared.
It just looks that way.

```csharp
// Features/Orders/GetOrder
public record GetOrderResponse(Guid Id, decimal Total, string Status);

// Features/Orders/CreateOrder
public record CreateOrderResponse(Guid Id, decimal Total, string Status);
```

They're identical.
The temptation to create a `SharedOrderDto` is overwhelming.
Resist it.

Next week, `GetOrder` needs a tracking URL.
But `CreateOrder` happens before shipping, so there's no URL yet.
If you'd shared the DTO, you'd now have a nullable property that's confusingly empty half the time.

**Duplication is cheaper than the wrong abstraction.**

## The Practical Structure

Here's what a mature Vertical Slice Architecture project looks like:

```
📂 src
└──📂 Features
│   ├──📂 Orders
│   │   ├──📂 CreateOrder
│   │   ├──📂 UpdateOrder
│   │   └──📂 Shared          # Order-specific sharing
│   ├──📂 Customers
│   │   ├──📂 GetCustomer
│   │   └──📂 Shared          # Customer-specific sharing
│   └──📂 Invoices
│       └──📂 GenerateInvoice
└──📂 Domain
│   ├──📂 Entities
│   ├──📂 ValueObjects
│   └──📂 Services            # Cross-feature domain logic
└──📂 Infrastructure
│   ├──📂 Persistence
│   └──📂 Services
└──📂 Shared
    └──📂 Behaviors
```

- **Features** — Self-contained slices. Each owns its request/response models.
- **Features/[Name]/Shared** — Local sharing between related slices.
- **Domain** — Entities, value objects, and domain services. Shared business logic lives here.
- **Infrastructure** — Technical concerns.
- **Shared** — Cross-cutting behaviors only.

## The Rules

After building several systems this way, here's what I've landed on:

1. **Features own their request/response models.** No exceptions.

2. **Push business logic into the domain.** Entities and value objects are the best place to share business rules.

3. **Keep feature-family sharing local.** If only Order slices need it, keep it in `Features/Orders/Shared` (feel free to find a better name than `Shared`).

4. **Infrastructure is shared by default**. Database contexts, HTTP clients, logging. These are technical concerns.

5. **Apply the Rule of Three.** Don't extract until you have three real usages with identical, stable logic.

## Takeaway

Vertical Slice Architecture asks: "What feature does _this_ belong to?"

The shared code question is really asking: "What do I do when the answer is _multiple features_?"

Acknowledge that some concepts genuinely span features.
Give them a home based on their _nature_ (domain, infrastructure, or cross-cutting behavior).
Resist the urge to share everything just because you could.

The goal isn't zero duplication.
It's code that's easy to change when requirements change.

And requirements always change.
