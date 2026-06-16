# Breaking Change Detection

**Tier**: 1 (Always Applied for library/public API changes)
**Token Budget**: ~1,200 tokens
**Profile**: All profiles (always-on for public API)

## Purpose

Detect changes that may break external consumers. Identifies removed public members, changed signatures, modified return types, and semantic behavior changes.

## Detection Workflow (Step 1e)

### 1. Identify Public API Surface

```text
By Language:

C#/.NET:
- public classes, interfaces, structs, enums
- public/protected methods and properties
- Exclude: internal, private, [InternalsVisibleTo] targets

TypeScript/JavaScript:
- export declarations (named and default)
- Exclude: internal modules, non-exported

Python:
- __all__ members (if defined)
- Public functions/classes (no _ prefix)
- Exclude: _private, __dunder (except __init__)

Go:
- Capitalized identifiers (exported)
- Exclude: lowercase (unexported)

Rust:
- pub items in lib.rs and public modules
- Exclude: pub(crate), pub(super)
```

### 2. Detect Breaking Changes from Git Diff

```bash
# Get removed lines that contain public API signatures
git diff HEAD~1 | grep "^-.*public\s" | grep -v "^---"

# For TypeScript, check removed exports
git diff HEAD~1 | grep "^-.*export\s" | grep -v "^---"

# Compare old vs new signatures for changes
git show HEAD~1:path/to/file.cs > /tmp/old.cs
git show HEAD:path/to/file.cs > /tmp/new.cs
# Parse and compare public member signatures
```

### 3. Classify Changes

| Change Type | Detection | Severity |
|-------------|-----------|----------|
| Member removed | Public method/class deleted | CRITICAL |
| Signature changed | Parameter type/count changed | CRITICAL |
| Return type changed | Different return type | MAJOR |
| Parameter added (required) | New non-optional parameter | CRITICAL |
| Parameter added (optional) | New optional/default parameter | MINOR |
| Visibility reduced | public → internal/private | CRITICAL |
| Behavior change | Semantic change (manual flag) | MAJOR |

## Checks

### 1.31.1 Public API Removal (CRITICAL)

**Detection**: Identify removed public members from diff.

**Severity**: CRITICAL (breaks all consumers)

**Finding Format**:

```markdown
### Public API Removal - Breaking Change

**File**: `src/Services/OrderService.cs`
**Severity**: CRITICAL
**Confidence**: HIGH

**Problem**: Public method was removed, breaking external consumers.

**Details**:
- Removed: `public Order GetOrderById(int id)`
- Impact: All callers of this method will fail to compile
- Alternatives: None detected in diff

**Fix**:
1. Restore the method, or
2. Mark as `[Obsolete]` with migration path, or
3. Document breaking change in CHANGELOG

**Migration Guide**:
```csharp
// If replacing with new API:
[Obsolete("Use GetOrder(OrderId id) instead. Will be removed in v3.0.")]
public Order GetOrderById(int id) => GetOrder(new OrderId(id));
```

### 1.31.2 Signature Change (CRITICAL)

**Detection**: Compare method signatures before/after.

**Severity**: CRITICAL (source and binary incompatibility)

**Finding Format**:

```markdown
### Signature Change - Breaking Change

**File**: `src/Services/UserService.cs:45`
**Severity**: CRITICAL
**Confidence**: HIGH

**Problem**: Method signature changed, breaking existing callers.

**Details**:
- Before: `CreateUser(string name, string email)`
- After: `CreateUser(string name, string email, bool isAdmin)`
- Breaking: New required parameter added

**Fix**: Add overload to maintain backwards compatibility.

```csharp
// Backwards compatible approach
public User CreateUser(string name, string email)
    => CreateUser(name, email, isAdmin: false);

public User CreateUser(string name, string email, bool isAdmin)
{
    // New implementation
}
```

### 1.31.3 Return Type Change (MAJOR)

**Detection**: Compare return types before/after.

**Severity**: MAJOR (may break consumers depending on usage)

**Finding Format**:

```markdown
### Return Type Change - Breaking Change

**File**: `src/Repositories/OrderRepository.cs:23`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Return type changed, may break consumers.

**Details**:
- Before: `List<Order> GetOrders()`
- After: `IEnumerable<Order> GetOrders()`
- Impact: Code using List-specific methods (Add, Count, indexer) will break

**Fix**: Consider if change is intentional. If so, document in CHANGELOG.
```

### 1.31.4 Behavior Change Flag (MAJOR)

**Detection**: Manual annotation via comment or commit message.

**Trigger Patterns**:

```text
// BREAKING: Changed behavior to...
// BEHAVIOR CHANGE: Now returns null instead of...
[BreakingChange("v2.0")]
```

**Severity**: MAJOR (semantic breaking change)

## Configuration Schema

Add to `.claude/code-review.md`:

```markdown
## Breaking Changes

### Mode
- mode: library  # Options: library (strict), internal (relaxed), disabled

### Ignore Paths
- ignore-paths: tests/**, internal/**, *.Tests.cs

### Allowed Breaking Changes
- allowed: []  # List of allowed breaking changes by name/pattern
```

## Language-Specific Patterns

### C\#

```csharp
// Breaking: Removed public member
- public void ProcessOrder(Order order) { }

// Breaking: Changed signature
- public Order GetOrder(int id)
+ public Order GetOrder(Guid id)

// Breaking: Changed return type
- public List<T> GetAll()
+ public IReadOnlyList<T> GetAll()

// Breaking: Reduced visibility
- public class OrderProcessor
+ internal class OrderProcessor
```

### TypeScript

```typescript
// Breaking: Removed export
- export function calculateTotal(items: Item[]): number

// Breaking: Changed signature
- export function getUser(id: number): User
+ export function getUser(id: string): User

// Breaking: Changed interface
interface Order {
-   total: number;
+   total: Money;  // Type changed
}
```

### Python

```python
# Breaking: Removed from __all__
- __all__ = ['process_order', 'Order', 'OrderStatus']
+ __all__ = ['process_order', 'Order']  # OrderStatus removed

# Breaking: Changed signature
- def get_user(user_id: int) -> User:
+ def get_user(user_id: str) -> User:

# Breaking: Changed return type
- def get_orders() -> list[Order]:
+ def get_orders() -> Iterator[Order]:
```

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Internal project | Relaxed mode, MAJOR instead of CRITICAL |
| Library project | Strict mode, all breaking changes CRITICAL |
| Pre-1.0 version | May allow more breaking changes (semver) |
| Deprecated API removal | Check if deprecation period elapsed |
| Test-only changes | Skip breaking change detection |

## Quick Reference

```text
BREAKING CHANGE CHECKS:
[CRITICAL] Public API removal → Always check
[CRITICAL] Signature change → Always check
[MAJOR] Return type change → Always check
[MAJOR] Behavior change → Flag via annotation

DETECTION STEPS:
1. Identify public API surface by language
2. Parse git diff for removed/changed public members
3. Classify by severity
4. Check configuration for mode (library/internal)
5. Flag with migration suggestions
```

---

**Last Updated:** 2025-12-31
