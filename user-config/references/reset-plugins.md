# Action: reset-plugins

Complete plugin reset - the "nuclear option" for plugins. Clears all plugin-related data from both `~/.claude/plugins/` directory AND `enabledPlugins` from `~/.claude/settings.json`.

## When to Use

- Starting fresh with plugins after configuration issues
- Resolving "Plugin not found in marketplace" errors
- Cleaning up after marketplace changes
- Recovering from corrupted plugin state
- Full reinstallation of all plugins needed

**For cache-only cleanup** (preserves registry): Use `/clear-plugin-cache` instead.

## What Gets Cleared

| Location | Contents | Notes |
|----------|----------|-------|
| `~/.claude/plugins/cache/` | Cached plugin copies | All versions |
| `~/.claude/plugins/installed_plugins.json` | Plugin registry | Tracks installed plugins |
| `~/.claude/plugins/install-counts-cache.json` | Install stats | Marketplace stats cache |
| `~/.claude/settings.json` -> `enabledPlugins` | Plugin enable/disable map | Only this key, other settings preserved |

## What Gets Preserved (by default)

| Location | Contents | Notes |
|----------|----------|-------|
| `~/.claude/plugins/known_marketplaces.json` | Custom marketplace sources | Use `--include-marketplaces` to clear |
| `claude-plugins-official` | Official Anthropic marketplace | ALWAYS preserved, even with `--include-marketplaces` |
| `~/.claude/settings.json` (other keys) | All other settings | Only `enabledPlugins` is removed |

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--dry-run` | Preview what would be cleared without deleting | false |
| `--include-marketplaces` | Also clear custom marketplace registrations (preserves official) | false |
| `--force` | Skip confirmation prompt | false |

## Workflow

### Step 1: Parse Arguments

```text
DRY_RUN = "--dry-run" in arguments
INCLUDE_MARKETPLACES = "--include-marketplaces" in arguments
FORCE = "--force" in arguments
```

### Step 2: Inventory What Will Be Cleared

Check each location and gather statistics (cache size, file counts, registry entries).

### Step 3: Show Reset Plan

Present the plan to the user with a table of what will be cleared and what will be preserved.

### Step 4: Confirmation (unless --force)

If NOT FORCE and NOT DRY_RUN:

```text
Use AskUserQuestion:
  Question: "Proceed with plugin reset? This cannot be undone."
  Options: ["Yes, reset plugins", "No, cancel"]
```

### Step 5: Execute Reset (unless --dry-run)

#### 5a: Clear Plugin Cache

```bash
rm -rf ~/.claude/plugins/cache/*
```

#### 5b: Clear Plugin Registry Files

```bash
rm -f ~/.claude/plugins/installed_plugins.json
rm -f ~/.claude/plugins/install-counts-cache.json
```

#### 5c: Clear Custom Marketplaces (if --include-marketplaces)

Read `known_marketplaces.json`, filter to keep only `claude-plugins-official`, write back.

#### 5d: Remove enabledPlugins from settings.json

Read `settings.json`, delete the `enabledPlugins` key, write back preserving all other keys.

### Step 6: Report Results

Show what was cleared, what was preserved, and next steps (restart Claude Code, reinstall plugins).

## Error Handling

| Error | Response |
|-------|----------|
| `~/.claude/plugins/` not found | "Plugin directory not found. Nothing to reset." |
| `~/.claude/settings.json` not found | Skip settings modification, continue with directory cleanup |
| Permission denied | "Permission denied. Check file permissions on ~/.claude/" |
| JSON parse error | "Failed to parse settings.json. File may be corrupted." |

## Safety Notes

- **This is destructive** - all installed plugins will need to be reinstalled
- **Official marketplace preserved** - `claude-plugins-official` is never removed
- **Settings preserved** - Only `enabledPlugins` key is removed from settings.json
- **Confirmation required** - Unless `--force` is specified
- **Dry-run available** - Always preview first if unsure

## Cross-Platform Notes

- Windows: `~` resolves to `$USERPROFILE` (e.g., `C:\Users\{username}`)
- Use forward slashes in paths for consistency
- `rm -rf` and `rm -f` work in Git Bash on Windows
