# CommonMark Configuration Guide

This guide covers strict CommonMark configuration for maximum markdown portability.

## When to Use CommonMark

Choose strict CommonMark when:

- **Maximum portability** - Your docs must render correctly across many platforms
- **Cross-platform publishing** - Building for multiple markdown renderers
- **Standards compliance** - Toolchain requires strict CommonMark
- **Baseline compatibility** - Avoiding platform-specific extensions

## What CommonMark Excludes

CommonMark is the base specification. These features are **NOT** part of CommonMark:

| Feature | CommonMark | Alternative |
|---------|:----------:|-------------|
| Tables | ✗ | Use HTML tables or ASCII art |
| Strikethrough (`~~text~~`) | ✗ | Use other emphasis or inline HTML |
| Task lists (`- [ ]`) | ✗ | Use regular lists with text markers |
| Extended autolinks | ✗ | Use explicit link syntax `[url](url)` |
| Footnotes | ✗ | Use reference links at document end |

## Configuration Override

Add this to your `.markdownlint-cli2.jsonc` for strict CommonMark:

```jsonc
{
  "config": {
    "default": true,

    // Disable GFM-only rules (tables don't exist in CommonMark)
    "MD055": false,  // table-pipe-style
    "MD056": false,  // table-column-count
    "MD058": false,  // blanks-around-tables

    // Stricter bare URL handling (no autolink extensions)
    "MD034": true    // no-bare-urls - enforces explicit links
  }
}
```

## Writing CommonMark-Compatible Markdown

### Avoid Tables

CommonMark doesn't support pipe tables. If you need tabular data:

Use a list:

```markdown
**Comparison:**

- **Option A**: Fast but expensive
- **Option B**: Slow but affordable
- **Option C**: Balanced performance and cost
```

Or use definition-style formatting:

```markdown
**Feature Support:**

- **Tables**: Not supported in CommonMark
- **Strikethrough**: Not supported in CommonMark
- **Task lists**: Not supported in CommonMark
```

### Avoid Strikethrough

Instead of `~~deleted text~~`, use alternatives:

```markdown
<!-- CommonMark alternatives to strikethrough -->

- Use emphasis: *removed* or **removed**
- Use brackets: [REMOVED]
- Use inline HTML (if allowed): <del>removed</del>
- Simply rewrite to avoid needing strikethrough
```

### Avoid Task Lists

Instead of `- [ ] Task`, use text markers:

```markdown
<!-- CommonMark alternative to task lists -->

## Checklist

- [TODO] Set up environment
- [DONE] Install dependencies
- [IN PROGRESS] Write documentation
```

### Use Explicit Links

CommonMark autolinks are more limited. Always use explicit syntax:

```markdown
<!-- CommonMark-safe link syntax -->

For more information, see [https://example.com](https://example.com).

<!-- Avoid relying on bare URL autolinks -->
```

## Validation

To verify your markdown is CommonMark-compliant:

1. Run linting with CommonMark config
2. Test rendering in a strict CommonMark parser
3. Check that no GFM extensions are used

```bash
# Run linting (uses your .markdownlint-cli2.jsonc config)
npx markdownlint-cli2 "**/*.md"
```

## Platform Compatibility

CommonMark-compliant markdown renders correctly on:

| Platform | CommonMark Support |
|----------|:-----------------:|
| GitHub | ✓ (superset) |
| GitLab | ✓ (superset) |
| Bitbucket | ✓ (superset) |
| VS Code Preview | ✓ |
| Pandoc | ✓ |
| Hugo | ✓ |
| Jekyll | ✓ |
| Docusaurus | ✓ |
| MkDocs | ✓ |

**Note:** All major platforms support CommonMark as a baseline. Using only CommonMark features ensures your markdown works everywhere.

## Migration from GFM

If migrating existing GFM content to strict CommonMark:

1. **Tables**: Convert to lists or restructure content
2. **Task lists**: Use text markers (`[TODO]`, `[DONE]`)
3. **Strikethrough**: Rewrite or use alternatives
4. **Autolinks**: Convert bare URLs to explicit links

## Related Documentation

- [Flavors Overview](overview.md) - Flavor comparison and selection
- [GFM Configuration Guide](gfm.md) - GitHub Flavored Markdown settings
- [Markdownlint Rules Reference](../markdownlint-rules.md) - All rules with flavor tags

## External References

- [CommonMark Specification](https://spec.commonmark.org/) - Official specification
- [CommonMark Dingus](https://spec.commonmark.org/dingus/) - Test CommonMark rendering

---

**Last Updated:** 2026-01-17
