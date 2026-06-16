---
name: audit-schema
description: Audit content schema for best practices, consistency, and potential issues. Checks naming, relationships, and field usage.
argument-hint: "[--fix] [--severity all|high|medium]"
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Audit Schema Command

Analyze content schema for best practices and potential issues.

## Usage

```bash
/cms:audit-schema
/cms:audit-schema --severity high
/cms:audit-schema --fix
```

## Options

- **--fix**: Suggest fixes for identified issues
- **--severity**: Filter by issue severity (all|high|medium)

## Workflow

### Step 1: Locate Schema Definitions

Search for content type definitions in:

- YAML/JSON specification files
- C# entity models
- Migration files

### Step 2: Invoke Skills

Invoke relevant skills for analysis:

- `content-type-modeling` - Type patterns
- `content-relationships` - Relationship integrity
- `dynamic-schema-design` - JSON column usage

### Step 3: Perform Audits

**Naming Convention Audit:**

- PascalCase for type names
- camelCase for field names
- Consistent pluralization
- Descriptive names

**Field Usage Audit:**

- Required fields have defaults or validation
- Optional fields marked correctly
- Field types appropriate for data
- No duplicate fields

**Relationship Audit:**

- All references resolve
- Inverse relationships defined
- No circular dependencies
- Cardinality correct

**Best Practices Audit:**

- Versioning enabled for editable content
- Slug/route fields present
- SEO fields for public content
- Audit fields (created, modified)

### Step 4: Generate Report

```markdown
## Schema Audit Report

### Summary
- Content Types: 12
- Total Fields: 87
- Relationships: 24
- Issues Found: 8 (3 high, 4 medium, 1 low)

### High Severity Issues

#### [H1] Missing Required Validation
**Type:** Product
**Field:** price
**Issue:** Required field has no default value
**Fix:** Add `[Required]` attribute or default value

#### [H2] Circular Dependency
**Types:** Category ↔ Product
**Issue:** Bidirectional reference may cause serialization issues
**Fix:** Use lazy loading or DTOs

### Medium Severity Issues

#### [M1] Inconsistent Naming
**Type:** blogPost (should be BlogPost)
**Fix:** Rename to PascalCase

#### [M2] Missing Inverse Relationship
**Type:** ProductVariant → Product
**Issue:** No navigation property back to Product
**Fix:** Add `Product` property to ProductVariant

### Low Severity Issues

#### [L1] Unused Field
**Type:** Article
**Field:** legacyId
**Issue:** Field appears unused in codebase
**Fix:** Remove if migration complete

### Recommendations

1. Add versioning to Product content type
2. Consider adding SEO part to Event content type
3. Review taxonomy depth for Categories (currently 5 levels)
```

### Step 5: Apply Fixes (if --fix)

For fixable issues, generate corrected schema:

```csharp
// Before
public class Product
{
    public decimal price { get; set; } // M1: wrong casing
}

// After (suggested fix)
public class Product
{
    [Required]
    public decimal Price { get; set; } // Fixed: PascalCase, Required
}
```

## Audit Categories

| Category | Checks |
|----------|--------|
| Naming | Casing, conventions, clarity |
| Fields | Types, validation, usage |
| Relationships | Integrity, cardinality, cycles |
| Best Practices | Versioning, SEO, audit trails |
| Performance | Indexing, query patterns |

## Related Skills

- `content-type-modeling` - Content type patterns
- `content-relationships` - Relationship patterns
- `dynamic-schema-design` - JSON column patterns
