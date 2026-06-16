---
name: docs-ops
description: "Manage Claude Code documentation lifecycle. Actions: scrape, validate, refresh, rebuild-index, clear-cache."
argument-hint: <action> (scrape|validate|refresh|rebuild-index|clear-cache) [options]
allowed-tools: Read, Write, Bash, Skill, Glob, Grep, Task, WebFetch, WebSearch
---

# Claude Code Documentation Operations

Manage the Claude Code documentation lifecycle through a single consolidated skill.

## Argument Routing

| Action | Description |
|--------|-------------|
| `scrape` | Scrape documentation from official sources, then refresh and validate |
| `validate` | Validate index integrity and detect drift (read-only) |
| `refresh` | Refresh index from filesystem without scraping |
| `rebuild-index` | Clear and immediately rebuild the search index |
| `clear-cache` | Clear the search cache (lazy rebuild on next search) |

Parse `$ARGUMENTS` to determine the action. The first token is the action keyword. Remaining tokens are passed as options to the action handler.

---

## Action: scrape

Scrape Claude documentation from official sources and run the full post-scrape workflow (index refresh and validation).

### Semantics

- This action **always performs actual scraping** of at least one documentation source.
- Default behavior:
  - Scrape **all configured official sources** (Claude docs, Claude Code docs, Anthropic docs), skipping unchanged documents.
  - Refresh the local index and metadata.
  - Validate that everything looks healthy.

### Default Workflow

When invoked without qualifiers:

1. Invoke the `claude-ecosystem:docs-management` skill.
2. Request scraping with natural language:

   ```text
   Please scrape all configured Claude documentation sources. Skip unchanged documents, then refresh the local index and metadata and validate. After validation, clean up aged-out Anthropic articles (older than the configured max_age_days threshold). Run in foreground so we can see progress.

   IMPORTANT: Use Python 3.13 for validation (py -3.13) due to spaCy compatibility. Python 3.14 works for scraping.
   ```

3. Let the skill decide which scripts to run based on its SKILL.md guidance.

### Scope Flags (Natural Language)

Use natural language to narrow scope:

- **By domain**: "Scrape only docs.claude.com, then refresh the index."
- **By category**: "Scrape only /en/api/ from docs.claude.com."
- **Post-scrape behavior**:
  - `scrape-only`: Skip index refresh and validation.
  - `scrape+refresh`: Scrape and refresh index (default).
  - `scrape+detect-drift`: Scrape and detect drift (404s, missing files).
  - `scrape+auto-cleanup`: Scrape and automatically cleanup drift.
  - `scrape+age-cleanup`: Scrape, refresh, and remove aged-out Anthropic articles.

### What This Action Should NOT Do

- Never run validation-only or index-only workflow.
- Never run scrapes in background with polling loops.
- Never make ad-hoc script edits during scrape.

### Accurate Reporting

**Distinguish by domain:**

- `docs.claude.com` and `code.claude.com`: Serve .md URLs successfully
- `anthropic.com`: Does NOT serve .md URLs (expected 404s, falls back to HTML)

Report per-domain statistics accurately.

---

## Action: validate

Validate the Claude documentation index integrity and detect drift. This is read-only - no changes made.

### Checks Performed

- Index integrity (file existence)
- Drift detection (404s, hash mismatches)
- Metadata coverage
- Missing files

### Instructions

Invoke the `claude-ecosystem:docs-management` skill to validate the documentation index.

Request validation report including any detected issues or drift.

---

## Action: refresh

Refresh the local Claude documentation index without network scraping.

### Purpose

Use this action when you want to:

- Rebuild index from filesystem
- Extract keywords and metadata
- Validate metadata coverage
- Generate summary report

For full scraping + refresh, use the `scrape` action instead.

### Instructions

Invoke the `claude-ecosystem:docs-management` skill to refresh the local documentation index.

Request index rebuild and metadata validation from the skill.

**Note:** Use Python 3.13 for this action due to spaCy compatibility:

```text
Please refresh the local documentation index and validate metadata. Use Python 3.13 (py -3.13) for spaCy compatibility.
```

---

## Action: rebuild-index

Clear and immediately rebuild the docs-management search index. This is faster than `clear-cache` + waiting for next search because it triggers the rebuild immediately.

### When to Use

- After manually editing `index.yaml` or documentation files
- When search results seem stale or incorrect
- After a `git pull` with documentation changes
- When you need search working immediately (not on next query)

### Difference from clear-cache

| Action | Behavior | Search Availability |
|--------|----------|---------------------|
| `clear-cache` | Clears cache only | Rebuild on next search (lazy) |
| `rebuild-index` | Clears + rebuilds | Immediate (eager) |

### Options

- **No options**: Show plan and ask for confirmation
- **--force**: Skip confirmation and rebuild immediately

### Instructions

This action clears the documentation search cache and immediately rebuilds the index.

#### Check Current Status

First, check the current cache state by running the cache manager info command. Report whether the cache exists, is valid, and when it was last built.

#### Request Confirmation

Unless the user passed `--force`, show a rebuild plan with the current cache state and ask for confirmation before proceeding. Explain that rebuilding takes a few seconds and search will be unavailable during the rebuild.

#### Clear and Rebuild

Once confirmed (or if `--force` was passed):

1. Clear the cache using the cache manager script
2. Trigger an immediate rebuild by running a search query through find_docs.py
3. Verify the rebuild succeeded by checking the new cache info

#### Report Results

Report the new index statistics including document count, terms indexed, and build time. Confirm that search is now available.

```markdown
## Index Rebuilt

Successfully rebuilt Claude Code documentation search index.

**New index stats:**
- Size: 1.8 MB
- Terms indexed: 6,020
- Documents: 451
- Tags: 33
- Categories: 16
- Build time: 45ms

**Search is now available.**
```

### Rebuild Triggers

The index automatically rebuilds when:

- `--clear-cache` flag is passed to find_docs.py
- cache_version.json is missing or invalid
- index.yaml content hash changes
- Plugin scripts change (plugin fingerprint hash)

### Cache Validation

The cache_manager.py uses content hashes (not just mtime) to detect changes. This correctly handles git operations where mtime changes but content doesn't.

---

## Action: clear-cache

Clear the docs-management search cache (inverted index). This forces the index to rebuild on the next documentation search.

### When to Use

- After manually editing `index.yaml`
- When search results seem stale or incorrect
- After a `git pull` with documentation changes
- To free up disk space (~1.8 MB)

### Options

- **No options**: Show what will be cleared and ask for confirmation
- **--force**: Skip confirmation and clear immediately

### Step 1: Parse Options

Check if `--force` flag is present.

```text
force_mode = "--force" in arguments (case-insensitive)
```

### Step 2: Locate Cache Directory

The docs-management cache is located at:

```text
~/.claude/plugins/cache/<marketplace>/claude-ecosystem/<version>/skills/docs-management/.cache/
```

**Detection approach:**

1. Find the installed claude-ecosystem plugin path from `~/.claude/plugins/installed_plugins.json`
2. Navigate to `skills/docs-management/.cache/`

### Step 3: Check Cache Status

List the cache files and their sizes:

| File | Purpose |
|------|---------|
| `inverted_index.json` | Search index (~1.8 MB) |
| `cache_version.json` | Hash-based validity tracking |

If cache directory doesn't exist or is empty, report: "Cache already clear. Nothing to do."

### Step 4: Confirmation (unless --force)

If NOT force_mode, present the cache clear plan:

```markdown
## Cache Clear Plan

**Target:** Claude Code documentation search index

| File | Size |
|------|------|
| inverted_index.json | X.X MB |
| cache_version.json | 512 bytes |

**Total:** X.X MB

> **Note:** The search index will rebuild automatically on the next documentation search.
> For immediate rebuild, use the `rebuild-index` action after clearing.

**Proceed?** Reply "yes" to continue, or use `--force` to skip this confirmation.
```

Wait for user confirmation. If user does not confirm, abort with: "Cache clear cancelled."

### Step 5: Clear Cache

Use the cache_manager.py script to clear the inverted index:

```bash
python "<install_path>/skills/docs-management/scripts/utils/cache_manager.py" --clear
```

Or manually delete the cache files:

```bash
rm -f "<cache_dir>/inverted_index.json"
rm -f "<cache_dir>/cache_version.json"
```

### Step 6: Report Success

```markdown
## Cache Cleared

Successfully cleared Claude Code documentation search cache.

**Cleared:**
- inverted_index.json (X.X MB)
- cache_version.json

**Next steps:**
- Search index will rebuild automatically on next search
- Or use `rebuild-index` action to rebuild immediately
```

### Error Handling

- **Cache not found:** Report "Cache already clear or plugin not installed."
- **Permission denied:** Report "Permission denied. Try running with elevated privileges."
- **Plugin not installed:** Report "claude-ecosystem plugin not found. Install with `/plugin install claude-ecosystem@<marketplace>`"

### Cross-Platform Notes

- Use forward slashes in paths for consistency
- Windows: `~` resolves to `%USERPROFILE%`
- The cache_manager.py script handles platform differences internally
