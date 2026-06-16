---
name: design-taxonomy
description: Design taxonomy structure for categories, tags, or hierarchical classification. Supports flat, hierarchical, and faceted patterns.
argument-hint: <taxonomy-name> [--type flat|hierarchical|faceted] [--format yaml|json]
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Design Taxonomy Command

Design a taxonomy structure with terms, hierarchy, and classification rules.

## Usage

```bash
/cms:design-taxonomy Categories --type hierarchical
/cms:design-taxonomy Tags --type flat
/cms:design-taxonomy ProductFilters --type faceted
```

## Taxonomy Types

- **flat**: Simple tags with no hierarchy
- **hierarchical**: Parent-child tree structure
- **faceted**: Multi-dimensional classification

## Workflow

### Step 1: Parse Arguments

Extract taxonomy name and type from the command.

### Step 2: Gather Requirements

Use AskUserQuestion for structured requirements gathering:

```yaml
# Question 1: Taxonomy Scope (MCP: CMS taxonomy patterns)
question: "What is the primary purpose of this taxonomy?"
header: "Purpose"
options:
  - label: "Content Organization (Recommended)"
    description: "Categories for articles, pages, or documents"
  - label: "Product Filtering"
    description: "Faceted navigation for e-commerce catalogs"
  - label: "Navigation Structure"
    description: "Menu hierarchy and site sections"
  - label: "Tagging System"
    description: "Flexible labels for cross-cutting concerns"

# Question 2: Hierarchy Depth (MCP: CLI best practices - scope selection)
question: "How deep should the taxonomy hierarchy be?"
header: "Depth"
options:
  - label: "Flat (Recommended)"
    description: "Single level - simple tags or labels"
  - label: "Shallow (2 levels)"
    description: "Parent-child structure for basic grouping"
  - label: "Deep (3+ levels)"
    description: "Full hierarchical tree for complex domains"
```

Use these responses to tailor taxonomy type and structure.

### Step 3: Invoke Skill

Invoke `taxonomy-architecture` skill with gathered requirements.

### Step 4: Generate Taxonomy Design

Based on type:

**Flat Taxonomy:**

```yaml
taxonomy:
  name: Tags
  type: flat
  settings:
    allow_multiple: true
    allow_new_terms: true
  terms:
    - name: Featured
    - name: Trending
    - name: Popular
```

**Hierarchical Taxonomy:**

```yaml
taxonomy:
  name: Categories
  type: hierarchical
  max_depth: 3
  settings:
    allow_multiple: true
    required_parent: false
  terms:
    - name: Technology
      children:
        - name: Software
          children:
            - name: Web Development
            - name: Mobile Apps
        - name: Hardware
    - name: Business
      children:
        - name: Marketing
        - name: Finance
```

**Faceted Taxonomy:**

```yaml
taxonomy:
  name: ProductFilters
  type: faceted
  facets:
    - name: Color
      terms: [Red, Blue, Green, Black, White]
    - name: Size
      terms: [Small, Medium, Large, XL]
    - name: Material
      terms: [Cotton, Polyester, Wool, Leather]
    - name: Price Range
      terms: [$0-25, $25-50, $50-100, $100+]
```

### Step 5: Generate Implementation

Provide EF Core model for the taxonomy:

```csharp
public class Taxonomy
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public TaxonomyType Type { get; set; }
    public List<Term> Terms { get; set; }
}

public class Term
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string Slug { get; set; }
    public Guid? ParentId { get; set; }
    public int SortOrder { get; set; }
}
```

## Related Skills

- `taxonomy-architecture` - Taxonomy patterns
- `content-type-modeling` - Taxonomy fields
