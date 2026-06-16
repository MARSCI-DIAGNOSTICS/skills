# Pattern and Convention Compliance

**Tier**: 4 (Repo-Specific, Profile-Gated)
**Token Budget**: ~2,000 tokens
**Profile**: `thorough` (basic), `strict` (full pattern analysis)

## Purpose

Verify new code matches established patterns in the codebase. Detects deviations from error handling conventions, naming standards, architectural patterns, and file organization practices.

## Detection Workflow (Step 3b)

### 1. Pattern Auto-Detection

Before reviewing changes, sample existing code to detect established patterns:

```text
1. Error Handling Detection:
   a. Search for Result<T>, Either<L,R>, OneOf<> → Functional patterns
   b. Search for try/catch frequency → Exception-based
   c. Search for error codes, status enums → Error code patterns
   d. Compare ratio: >70% of one pattern = established convention

2. DI Pattern Detection:
   a. Constructor injection: private readonly fields + constructor params
   b. Method injection: IServiceProvider in method signatures
   c. Property injection: [Inject] attributes or public setters
   d. Service registration: AddScoped/AddTransient/AddSingleton patterns

3. Architectural Pattern Detection:
   a. CQRS: ICommand/IQuery interfaces, handlers, MediatR usage
   b. Repository: IRepository<T>, DbContext abstraction
   c. Unit of Work: IUnitOfWork, SaveChanges patterns
   d. Mediator: IMediator, Send/Publish patterns
   e. Domain Events: IDomainEvent, event handlers

4. Naming Convention Detection:
   a. Sample 20+ class names → Detect PascalCase/camelCase
   b. Sample 20+ method names → Detect verb-first, noun-first
   c. Sample interface names → Detect I prefix usage
   d. Sample constant names → Detect UPPER_SNAKE vs PascalCase

5. File Organization Detection:
   a. Feature folders: /Features/UserManagement/, /Features/Orders/
   b. Layer folders: /Controllers/, /Services/, /Repositories/
   c. Domain folders: /Domain/, /Application/, /Infrastructure/
   d. Hybrid: Mix of above patterns
```

### 2. Load Configuration Overrides

Check for explicit pattern configuration in `.claude/code-review.md`:

```markdown
## Patterns

### Error Handling
- pattern: Result<T>

### Architecture
- patterns: CQRS, mediator, repository

### Naming
- classes: PascalCase
- methods: PascalCase
- interfaces: I-prefix
- constants: UPPER_SNAKE

### File Organization
- style: feature-folders
```

**Priority**: Configuration overrides auto-detection. If both exist, configuration wins.

### 3. Compare New Code Against Patterns

For each changed file:

```text
1. Identify pattern-relevant constructs:
   - Error handling (try/catch, Result<>, return types)
   - Class/method/variable names
   - DI usage (constructor params, registrations)
   - File location relative to project structure

2. Compare against detected/configured patterns:
   - Match = no finding
   - Mismatch = flag with severity based on deviation type

3. Consider context:
   - Test files may have different patterns (relaxed)
   - Generated code may deviate (skip or low confidence)
   - Migration/legacy code may intentionally differ (note)
```

## Checks

### 4.20.1 Error Handling Pattern Mismatch (MAJOR)

**Detection**: Compare error handling approach against established pattern.

**Patterns**:

| Pattern | Indicators | Languages |
|---------|------------|-----------|
| Result<T> / Either | `Result<T>`, `Either<L,R>`, `OneOf<>` | C#, F# |
| Exceptions | `try/catch`, `throw`, custom exceptions | All |
| Error Codes | `enum ErrorCode`, `int` return types | C, Go-style |
| Option/Maybe | `Option<T>`, `Maybe<T>`, nullable patterns | F#, functional |

**Severity**: MAJOR (architectural consistency)
**Profile**: `thorough`

**Finding Format**:

```markdown
### Error Handling Pattern Mismatch

**File**: `src/Services/OrderService.cs:45`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Error handling approach differs from codebase convention.

**Details**:
- Codebase Pattern: `Result<T>` functional error handling
- This Code: `try/catch` exception-based handling
- Evidence: 85% of service methods return `Result<T>`

**Fix**: Refactor to use `Result<T>` pattern for consistency.

**Example**:
```csharp
// Before (exception-based)
public Order GetOrder(int id)
{
    var order = _repo.Find(id);
    if (order == null) throw new NotFoundException();
    return order;
}

// After (Result<T> pattern)
public Result<Order> GetOrder(int id)
{
    var order = _repo.Find(id);
    if (order == null) return Result.Failure<Order>(Errors.NotFound);
    return Result.Success(order);
}
```

### 4.20.2 Naming Convention Inconsistency (MINOR)

**Detection**: Compare naming against sampled conventions.

**Naming Aspects**:

| Aspect | Common Conventions |
|--------|-------------------|
| Classes | PascalCase (C#, Java), snake_case (Python) |
| Methods | PascalCase (C#), camelCase (Java, JS), snake_case (Python) |
| Variables | camelCase (most), snake_case (Python, Ruby) |
| Constants | UPPER_SNAKE (most), PascalCase (C#) |
| Interfaces | I-prefix (C#), no prefix (Java, TS) |
| Private fields | _underscore prefix, no prefix |

**Severity**: MINOR (style consistency)
**Profile**: `thorough`

**Finding Format**:

```markdown
### Naming Convention Inconsistency

**File**: `src/Handlers/orderHandler.ts:1`
**Severity**: MINOR
**Confidence**: HIGH

**Problem**: Class name doesn't match codebase convention.

**Details**:
- Expected: PascalCase (e.g., `OrderHandler`)
- Found: camelCase (`orderHandler`)
- Codebase Sample: 95% of classes use PascalCase

**Fix**: Rename to `OrderHandler`.
```

### 4.20.3 Architectural Pattern Deviation (MAJOR)

**Detection**: Verify adherence to established architectural patterns.

**Pattern Indicators**:

| Pattern | Expected Elements |
|---------|-------------------|
| CQRS | Commands/Queries separate, handlers per operation |
| Mediator | MediatR/similar, no direct service-to-service calls |
| Repository | Interface abstraction, no direct DbContext usage |
| Domain Events | Event classes, handlers, eventual consistency |
| Clean Architecture | Layer separation, dependency inversion |

**Severity**: MAJOR (architectural integrity)
**Profile**: `strict`

**Finding Format**:

```markdown
### Architectural Pattern Deviation

**File**: `src/Controllers/OrderController.cs:34`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Direct DbContext usage bypasses repository pattern.

**Details**:
- Codebase Pattern: Repository abstraction (`IOrderRepository`)
- This Code: Direct `_dbContext.Orders.Find(id)` usage
- Violation: Breaks layer separation established in codebase

**Fix**: Use `IOrderRepository` instead of direct DbContext access.
```

### 4.20.4 DI Registration Inconsistency (MINOR)

**Detection**: Compare DI patterns in new service registrations.

**Severity**: MINOR
**Profile**: `strict`

### 4.20.5 File Organization Mismatch (MINOR)

**Detection**: Verify new files follow established folder structure.

**Organization Styles**:

| Style | Structure |
|-------|-----------|
| Feature Folders | `/Features/{Feature}/` contains all related files |
| Layer Folders | `/Controllers/`, `/Services/`, `/Repositories/` |
| Domain Folders | `/Domain/`, `/Application/`, `/Infrastructure/` |
| Hybrid | Combination based on project conventions |

**Severity**: MINOR
**Profile**: `strict`

**Finding Format**:

```markdown
### File Organization Mismatch

**File**: `src/Services/OrderValidator.cs`
**Severity**: MINOR
**Confidence**: MEDIUM

**Problem**: File location doesn't match feature folder organization.

**Details**:
- Codebase Style: Feature folders
- Expected Location: `src/Features/Orders/Validators/OrderValidator.cs`
- Actual Location: `src/Services/OrderValidator.cs`

**Fix**: Move to feature folder structure.
```

## Configuration Schema

Add to `.claude/code-review.md`:

```markdown
## Patterns

### Error Handling
- pattern: Result<T>  # Options: Result<T>, Either, exceptions, error-codes

### Architecture
- patterns: CQRS, mediator, repository  # Comma-separated

### Naming
- classes: PascalCase
- methods: PascalCase
- variables: camelCase
- constants: UPPER_SNAKE
- interfaces: I-prefix
- private-fields: _underscore

### File Organization
- style: feature-folders  # Options: feature-folders, layer-folders, domain-folders, hybrid

### Exceptions (files/folders to skip pattern checks)
- paths: tests/**, *.Generated.cs, Migrations/**
```

## Language-Specific Detection

### C# / .NET

```csharp
// Error handling detection
grep -r "Result<" --include="*.cs" | wc -l  // Functional
grep -r "try\s*{" --include="*.cs" | wc -l  // Exception-based

// DI pattern detection
grep -r "private readonly.*_" --include="*.cs"  // Constructor injection fields

// Architecture detection
grep -r "IMediator" --include="*.cs"  // Mediator pattern
grep -r "IRepository<" --include="*.cs"  // Repository pattern
```

### TypeScript / JavaScript

```typescript
// Error handling detection
grep -r "Result\." --include="*.ts"  // Functional
grep -r "try\s*{" --include="*.ts"  // Exception-based

// Architecture detection
grep -r "@Injectable" --include="*.ts"  // DI framework usage
grep -r "implements.*Repository" --include="*.ts"  // Repository pattern
```

### Python

```python
# Naming detection
grep -r "^class [A-Z]" --include="*.py"  # PascalCase classes
grep -r "^def [a-z_]" --include="*.py"  # snake_case functions

# Architecture detection
grep -r "@inject" --include="*.py"  # DI framework
grep -r "class.*Repository" --include="*.py"  # Repository pattern
```

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Mixed patterns (legacy + new) | Flag with LOW confidence, suggest gradual migration |
| Test files | Relaxed pattern enforcement, different conventions allowed |
| Generated code | Skip pattern checks entirely |
| Prototypes/POCs | Flag but don't block, informational only |
| Third-party integrations | May require different patterns, context-aware |

## Quick Reference

```text
PATTERN COMPLIANCE CHECKS:
[MAJOR] Error handling pattern mismatch → thorough, strict
[MINOR] Naming convention inconsistency → thorough, strict
[MAJOR] Architectural pattern deviation → strict only
[MINOR] DI registration inconsistency → strict only
[MINOR] File organization mismatch → strict only

DETECTION PRIORITY:
1. Load .claude/code-review.md configuration (explicit overrides)
2. Auto-detect from codebase sampling (if no config)
3. Compare new code against detected/configured patterns
4. Apply profile-based severity filtering
```

---

**Last Updated:** 2025-12-31
