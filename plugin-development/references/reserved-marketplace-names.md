# Reserved Marketplace Names (Undocumented)

**Discovered:** 2025-12-16

Claude Code validates the `name` field in `marketplace.json` against a list of reserved names. This is **not documented** in official docs but enforced at runtime.

## Error Message

```text
The name 'claude-code-plugins' is reserved for official Anthropic marketplaces
and can only be used with GitHub sources from the 'anthropics' organization.
```

## Known Reserved Names

| Name | Reserved For |
|------|--------------|
| `claude-code-plugins` | `anthropics` organization |

**Note:** Additional names may be reserved. If you encounter a "reserved name" error, check this list and update if needed.

## The Fix

Change the `name` field in `.claude-plugin/marketplace.json` to something that doesn't contain reserved terms:

```json
{
  "name": "melodic-software",  // Changed from "claude-code-plugins"
  "owner": { ... }
}
```

## Important Notes

- The validation is on the `name` field in marketplace.json, NOT the GitHub repo name
- You can keep your repo named anything - just change the marketplace name
- Existing installations may need to remove and re-add the marketplace after this change
- This restriction appeared around December 2025 and may affect existing marketplaces

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Name is reserved" | Using `claude-code-plugins` or similar | Change marketplace name in `marketplace.json` |
| Marketplace not updating after name change | Cache still using old name | Remove and re-add the marketplace |

---

**Last Updated:** 2025-12-30
