# Markdown Flavors Overview

This document provides guidance on selecting and configuring markdown flavors for linting.

## What Are Markdown Flavors?

Markdown "flavors" are variants of the original Markdown specification that add or modify syntax. While the core syntax is similar, different platforms extend markdown with additional features.

**markdownlint-cli2** uses the [micromark](https://github.com/micromark/micromark) parser which is CommonMark-compliant with optional extensions for GFM features.

## Supported Flavors

| Flavor | Default | Description | Primary Use Case |
|--------|---------|-------------|------------------|
| **GFM** | ✓ | GitHub Flavored Markdown | GitHub repos, most web projects |
| **CommonMark** | | Strict base specification | Maximum portability, cross-platform publishing |

## Feature Comparison

| Feature | CommonMark | GFM |
|---------|:----------:|:---:|
| Headings (`#`, `##`, etc.) | ✓ | ✓ |
| Emphasis (`*italic*`, `**bold**`) | ✓ | ✓ |
| Links (`[text](url)`) | ✓ | ✓ |
| Images (`![alt](url)`) | ✓ | ✓ |
| Code blocks (fenced) | ✓ | ✓ |
| Blockquotes (`>`) | ✓ | ✓ |
| Ordered/unordered lists | ✓ | ✓ |
| Horizontal rules | ✓ | ✓ |
| Inline code | ✓ | ✓ |
| **Tables** (`\| col \|`) | ✗ | ✓ |
| **Strikethrough** (`~~text~~`) | ✗ | ✓ |
| **Task lists** (`- [ ]`, `- [x]`) | ✗ | ✓ |
| **Autolinks** (extended) | Basic | Extended |

## Which Flavor Should I Use?

### Use GFM (Default) When

- Your markdown will be rendered on GitHub (README, docs, issues)
- You need tables, task lists, or strikethrough
- You're working on a typical web project
- You want maximum feature support with good portability

**GFM is the recommended default for most projects.**

### Use CommonMark When

- Maximum portability is critical (publishing to multiple platforms)
- You need strict compliance with the base specification
- Your toolchain requires pure CommonMark
- You're building a documentation system that must work everywhere

## markdownlint Flavor Support

markdownlint validates against CommonMark by default, with built-in support for GFM extensions:

```text
┌──────────────────────────────────────────────────────┐
│  markdownlint-cli2 (micromark parser)                │
│  ┌───────────────────────────────────────────────┐  │
│  │  CommonMark (base rules)                      │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  GFM Extensions                        │  │  │
│  │  │  - Tables (MD055, MD056, MD058)        │  │  │
│  │  │  - Autolinks                           │  │  │
│  │  │  - Strikethrough                       │  │  │
│  │  │  - Task lists                          │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

## Flavor-Sensitive Rules

These rules behave differently or only apply to specific flavors:

| Rule | Alias | Flavor Impact | Notes |
|------|-------|---------------|-------|
| MD055 | table-pipe-style | GFM-only | Tables not in CommonMark |
| MD056 | table-column-count | GFM-only | Tables not in CommonMark |
| MD058 | blanks-around-tables | GFM-only | Tables not in CommonMark |
| MD033 | no-inline-html | Universal (configurable) | GFM may need more relaxed settings |
| MD034 | no-bare-urls | Universal (behavior differs) | GFM autolinks differ from CommonMark |

## Configuration by Flavor

### Default Configuration (GFM)

The default markdownlint-cli2 configuration works well for GFM:

```jsonc
{
  "config": {
    "default": true
    // Table rules (MD055, MD056, MD058) enabled by default
    // Autolinks, task lists work automatically
  }
}
```

See [GFM Configuration Guide](gfm.md) for detailed GFM settings.

### Strict CommonMark Configuration

For strict CommonMark compliance, disable GFM-specific rules:

```jsonc
{
  "config": {
    "default": true,
    "MD055": false,  // No tables in CommonMark
    "MD056": false,  // No tables in CommonMark
    "MD058": false   // No tables in CommonMark
  }
}
```

See [CommonMark Configuration Guide](commonmark.md) for strict CommonMark settings.

## Future Flavors

Additional flavors may be added based on demand:

- **MDX**: JSX-in-markdown (requires custom parsing)
- **Extended Syntax**: Footnotes, definition lists, abbreviations
- **Platform-Specific**: Microsoft Learn alerts, Azure DevOps extensions

To request a new flavor guide, raise the need with the project maintainers.

## Related Documentation

- [GFM Configuration Guide](gfm.md) - Detailed GitHub Flavored Markdown settings
- [CommonMark Configuration Guide](commonmark.md) - Strict CommonMark settings
- [Markdownlint Rules Reference](../markdownlint-rules.md) - All rules with flavor tags

## External References

- [CommonMark Specification](https://spec.commonmark.org/) - The base markdown specification
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/) - GFM specification
- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) - Official rule documentation

---

**Last Updated:** 2026-01-17
