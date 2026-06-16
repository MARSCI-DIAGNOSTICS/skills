# GFM (GitHub Flavored Markdown) Configuration Guide

This guide covers GitHub Flavored Markdown configuration for markdownlint-cli2.

## Overview

GitHub Flavored Markdown (GFM) is the **default and recommended flavor** for most projects. It extends CommonMark with useful features widely supported across modern platforms.

## Why GFM is the Default

- **Industry standard** - Most markdown editors and platforms support GFM
- **Feature-rich** - Tables, task lists, and strikethrough are commonly needed
- **GitHub ubiquity** - README files, documentation, and issues all use GFM
- **Good tooling** - Excellent linting support in markdownlint-cli2

## GFM Extensions

GFM adds these features to CommonMark:

### Tables

Pipe tables with alignment support:

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| L1   | C1     | R1    |
| L2   | C2     | R2    |
```

**Related rules:**

- **MD055** (table-pipe-style) - Consistent pipe placement
- **MD056** (table-column-count) - Consistent column count per row
- **MD058** (blanks-around-tables) - Blank lines before/after tables

### Task Lists

Interactive checkboxes:

```markdown
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
```

**Note:** markdownlint ignores task list items when checking MD052 (reference links).

### Strikethrough

Deleted or deprecated text:

```markdown
~~This text is struck through~~
```

### Autolinks

Extended automatic URL linking:

```markdown
Visit https://github.com for more info.
Email support@example.com for help.
```

**Related rule:**

- **MD034** (no-bare-urls) - May conflict with autolinks; configure as needed

## Configuration

GFM works out of the box with default configuration:

```jsonc
{
  "config": {
    "default": true
    // GFM features are enabled by default:
    // - Table rules (MD055, MD056, MD058) are active
    // - Task lists are recognized
    // - Autolinks work as expected
  }
}
```

### Recommended GFM Configuration

For typical GFM projects, this configuration works well:

```jsonc
{
  "gitignore": true,
  "config": {
    "default": true,

    // Line length - often disabled for docs with tables/URLs
    "MD013": false,

    // Inline HTML - may need specific elements allowed
    "MD033": {
      "allowed_elements": ["br", "details", "summary", "sup", "sub"]
    }
  }
}
```

### GFM with Stricter Settings

For stricter GFM enforcement:

```jsonc
{
  "gitignore": true,
  "config": {
    "default": true,

    // Tables - enforce consistent style
    "MD055": {
      "style": "leading_and_trailing"
    },

    // Bare URLs - require explicit links (optional)
    "MD034": true
  }
}
```

## Table Best Practices

### Alignment

Use colons to specify column alignment:

```markdown
| Default | Left    | Center  | Right   |
|---------|:--------|:-------:|--------:|
| text    | aligned | aligned | aligned |
```

### Consistent Pipes

Choose a style and be consistent:

**Leading and trailing (recommended):**

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

**No leading pipe (also valid):**

```markdown
Header 1 | Header 2 |
---------|----------|
Cell 1   | Cell 2   |
```

### Column Width

Align columns for readability (optional but recommended):

```markdown
| Short | Medium Column | Longer Column Header |
|-------|---------------|----------------------|
| A     | B             | C                    |
| D     | E             | F                    |
```

## Task List Best Practices

### Spacing

Use consistent spacing after brackets:

```markdown
- [x] Completed (space after bracket)
- [ ] Pending (space after bracket)
```

### Nesting

Task lists can be nested:

```markdown
- [x] Main task
  - [x] Subtask 1
  - [ ] Subtask 2
- [ ] Another main task
```

## Common GFM Linting Errors

### MD055 - Table Pipe Style

**Error:** Inconsistent table pipe style

**Fix:** Use consistent leading/trailing pipes:

```markdown
<!-- Before (inconsistent) -->
| Header 1 | Header 2
|----------|----------
| Cell 1   | Cell 2

<!-- After (consistent) -->
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

### MD056 - Table Column Count

**Error:** Different number of columns in table rows

**Fix:** Ensure all rows have the same number of columns:

```markdown
<!-- Before (mismatched columns) -->
| A | B | C |
|---|---|
| 1 | 2 | 3 |

<!-- After (consistent columns) -->
| A | B | C |
|---|---|---|
| 1 | 2 | 3 |
```

### MD058 - Blanks Around Tables

**Error:** Tables should be surrounded by blank lines

**Fix:** Add blank lines before and after tables:

```markdown
Some text.

| Header |
|--------|
| Cell   |

More text.
```

## Platform Compatibility

GFM features are supported on:

| Platform | Tables | Task Lists | Strikethrough | Autolinks |
|----------|:------:|:----------:|:-------------:|:---------:|
| GitHub | ✓ | ✓ | ✓ | ✓ |
| GitLab | ✓ | ✓ | ✓ | ✓ |
| Bitbucket | ✓ | ✓ | ✓ | ✓ |
| VS Code | ✓ | ✓ | ✓ | ✓ |
| Notion | ✓ | ✓ | ✓ | ✓ |
| Obsidian | ✓ | ✓ | ✓ | ✓ |
| Typora | ✓ | ✓ | ✓ | ✓ |

**Note:** Most modern markdown tools support GFM features.

## Advanced: markdown-it Plugins

For features beyond GFM (footnotes, math, etc.), markdownlint-cli2 supports markdown-it plugins:

```jsonc
{
  "config": {
    "default": true
  },
  "markdownItPlugins": [
    ["markdown-it-footnote"]
  ]
}
```

**Note:** This is advanced configuration for specialized needs. GFM covers most use cases.

## Related Documentation

- [Flavors Overview](overview.md) - Flavor comparison and selection
- [CommonMark Configuration Guide](commonmark.md) - Strict CommonMark settings
- [Markdownlint Rules Reference](../markdownlint-rules.md) - All rules with flavor tags

## External References

- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/) - Official specification
- [GitHub Markdown Guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) - GitHub's markdown documentation
- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) - Official rule documentation

---

**Last Updated:** 2026-01-17
