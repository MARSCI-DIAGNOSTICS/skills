---
name: clear-plugin-cache
description: Clear cached plugin copies (requires reinstall after)
argument-hint: "[plugin-name] [--force] (optional)"
allowed-tools: Read, Bash(rm:*), Bash(ls:*), Bash(du:*), Bash(test:*), Glob
---

# Clear Plugin Cache Command

Clear cached plugin copies from the plugin system cache. This is a more aggressive operation that removes the entire plugin installation, requiring reinstall afterward.

## When to Use

- Plugin behaving unexpectedly after updates
- Corrupted plugin installation
- Freeing significant disk space
- Clean slate reinstallation needed

**For complete plugin reset** (including registry and settings): Use `/user-config:reset-plugins` instead. This command only clears the cache while preserving the registry.

## What Gets Cleared vs Preserved

**Cleared:**

- `~/.claude/plugins/cache/` - All cached plugin copies

**Preserved (NOT cleared):**

- `~/.claude/plugins/installed_plugins.json` - Plugin registry (knows what to reinstall)
- `~/.claude/plugins/known_marketplaces.json` - Marketplace sources

## Arguments

- **No arguments**: Clear ALL plugin caches (prompts for confirmation)
- **plugin-name**: Clear only the specified plugin's cache (e.g., `claude-ecosystem`)
- **--force**: Skip confirmation

**Examples:**

```text
/clear-plugin-cache                        # Clear all plugins
/clear-plugin-cache claude-ecosystem       # Clear only claude-ecosystem
/clear-plugin-cache --force                # Clear all without confirmation
/clear-plugin-cache claude-ecosystem --force   # Clear one without confirmation
```

## Step 1: Parse Arguments

```text
plugin_filter = None  # or specific plugin name
force_mode = "--force" in arguments (case-insensitive)

# Parse: anything that's not --force is treated as plugin name
for arg in arguments:
    if arg.lower() == "--force":
        force_mode = True
    elif not arg.startswith("--"):
        plugin_filter = arg
```

## Step 2: Locate Plugin Cache

The plugin cache is at: `~/.claude/plugins/cache/`

Structure:

```text
~/.claude/plugins/
  cache/
    {marketplace}/
      {plugin-name}/
        {version}/
          ... (full plugin copy)
```

## Step 3: Inventory Cache Contents

List what will be cleared:

```bash
# List all marketplace directories
ls -la ~/.claude/plugins/cache/

# For each marketplace, list plugins
ls -la ~/.claude/plugins/cache/{marketplace}/

# Get total size
du -sh ~/.claude/plugins/cache/
```

If plugin_filter is set, only inventory that specific plugin.

## Step 4: Confirmation (unless --force)

If NOT force_mode, present the cache clear plan:

### For ALL plugins

```markdown
## Plugin Cache Clear Plan

**Target:** ALL cached plugin copies

| Marketplace | Plugins | Size |
| --- | --- | --- |
| claude-code-plugins | 10 | 120 MB |

**Total:** 120 MB across 10 plugins

> **WARNING:** This will remove all installed plugins.
> You will need to reinstall them using `/plugin install {name}@{marketplace}`.
> The plugin registry (installed_plugins.json) is preserved, so Claude Code
> knows what to reinstall.

**Proceed?** Reply "yes" to continue, or use `--force` to skip this confirmation.
```

### For SINGLE plugin

```markdown
## Plugin Cache Clear Plan

**Target:** claude-ecosystem plugin cache only

| Plugin | Version | Size |
| --- | --- | --- |
| claude-ecosystem | 3.0.0 | 106 MB |

> **Note:** After clearing, reinstall with:
> `/plugin install claude-ecosystem@claude-code-plugins`

**Proceed?** Reply "yes" to continue, or use `--force` to skip this confirmation.
```

## Step 5: Clear Cache

### For ALL plugins

```bash
rm -rf ~/.claude/plugins/cache/*
```

### For SINGLE plugin

```bash
# Find and remove specific plugin across all marketplaces
rm -rf ~/.claude/plugins/cache/*/{plugin-name}
```

## Step 6: Report Success

```markdown
## Plugin Cache Cleared

Successfully cleared plugin cache.

**Cleared:**
- X plugins (Y MB total)

**Preserved:**
- installed_plugins.json (plugin registry)
- known_marketplaces.json (marketplace sources)

**Next steps:**
Reinstall plugins using:

`/plugin install {plugin-name}@{marketplace}`

Or browse and reinstall interactively:

`/plugin`
```

## Error Handling

- **Cache not found:** Report "Plugin cache directory not found or already empty."
- **Permission denied:** Report "Permission denied. Check file permissions on ~/.claude/plugins/cache/"
- **Plugin not found:** Report "Plugin '{name}' not found in cache. Available plugins: {list}"

## Safety Notes

- **This is safe for both local and git-based marketplaces** - the cache is always a downstream copy
- **Local marketplace:** Plugin will be re-copied from source directory
- **Git marketplace:** Plugin will be re-cloned/fetched from remote

The original source (your local repo or git remote) is NEVER modified.

## Cross-Platform Notes

- Windows: `~` resolves to `%USERPROFILE%`
- Use forward slashes in paths for consistency
- `rm -rf` works in Git Bash on Windows

## Related Commands

- `/user-config:reset-plugins` - Complete plugin reset (cache + registry + settings)
- `/user-config:prune` - General Claude Code cache cleanup (excludes plugins)
- `/plugin uninstall {name}` - Remove a specific plugin properly
