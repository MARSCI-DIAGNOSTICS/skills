---
name: batch-scrape
description: Run scrape workflows for one or more ecosystems in dev mode using local plugin code
allowed-tools: Read, Bash, Skill
argument-hint: "[ecosystem] (claude|cursor|duende|google|openai|all)"
---

# Batch Scrape

Run documentation scraping workflows for one or more ecosystems using **local plugin code** (dev mode).

## Arguments

Parse `$ARGUMENTS` to determine mode and ecosystems:

- **Single ecosystem**: `claude`, `cursor`, `duende`, `google`, `openai`
- **Multiple ecosystems**: Space-separated list (e.g., `claude google`)
- **All ecosystems**: `all` or no arguments
- **Mode prefix**: Optionally prefix with `sequential` (default) or `headless`

**Examples:**

- `/batch-scrape claude` -- scrape claude ecosystem only
- `/batch-scrape cursor duende` -- scrape cursor + duende sequentially
- `/batch-scrape all` -- sequential, all ecosystems
- `/batch-scrape headless` -- headless, all ecosystems
- `/batch-scrape headless claude google` -- headless, just claude + google

## Ecosystem Routing Table

| Ecosystem | Dev Env Var | Plugin Path | Docs Skill |
| --- | --- | --- | --- |
| `claude` | `OFFICIAL_DOCS_DEV_ROOT` | `plugins/claude-ecosystem/skills/docs-management/` | `claude-ecosystem:docs-ops scrape` |
| `cursor` | `CURSOR_DOCS_DEV_ROOT` | `plugins/cursor-ecosystem/skills/cursor-docs/` | `cursor-ecosystem:docs-ops scrape` |
| `duende` | `DUENDE_DOCS_DEV_ROOT` | `plugins/duende-ecosystem/skills/duende-docs/` | `duende-ecosystem:docs-ops scrape` |
| `google` | `GEMINI_DOCS_DEV_ROOT` | `plugins/google-ecosystem/skills/gemini-cli-docs/` | `google-ecosystem:docs-ops scrape` |
| `openai` | `CODEX_DOCS_DEV_ROOT` | `plugins/openai-ecosystem/skills/codex-cli-docs/` | `openai-ecosystem:docs-ops scrape` |

## Dev Mode Environment Variable

**CRITICAL:** Environment variables set mid-session do NOT persist across Claude's Bash tool calls. Each Bash command runs in a fresh shell. You must set the env var in the SAME command that runs the script.

**IMPORTANT:** Claude's Bash tool uses **Git Bash (MINGW64)** on Windows, not PowerShell. Use Bash inline prefix syntax for all commands executed by Claude Code.

**Bash syntax (use this in Claude Code):**

```bash
<ENV_VAR>="<repo-root>/<plugin-path>" python <script-path>
```

**PowerShell syntax (for native PowerShell terminal only):**

```powershell
$env:<ENV_VAR> = "<repo-root>/<plugin-path>"; python <script-path>
```

This overrides the installed plugin path, redirecting all operations to the local development copy.

## Mode 1: Sequential (default)

Run each ecosystem's scrape workflow in order within a single session. Use `/compact` between each to manage context window size.

### Sequential Workflow

For each ecosystem in the selected list:

1. Run the ecosystem's scrape workflow (see ecosystem-specific sections below) -- follow all steps including audit/fix/commit
2. Run `/compact` to reclaim context before the next ecosystem

### Notes

- Each scrape workflow includes its own audit/fix/commit step -- complete it before moving on
- If context gets too large before completing all ecosystems, stop and resume in a new session
- Review `git log --oneline -10` after all runs to verify commits

## Mode 2: Headless

Run each ecosystem in a separate headless Claude session. These can run in parallel across terminal windows.

### Headless Workflow

For each ecosystem in the selected list, output the corresponding `claude -p` command:

```bash
claude -p "Run /batch-scrape <ecosystem> following all steps including audit/fix/commit." \
  --allowedTools "Read,Edit,Write,Bash,Skill,Glob,Grep"
```

Then instruct the user to run them in separate terminal windows.

### Notes

- Each `claude -p` invocation gets its own context window -- no cross-contamination
- Run in separate terminal windows for parallel execution
- Review all commits after runs complete: `git log --oneline -20`
- Use `--resume` to continue an interrupted session
- Headless mode auto-commits per the scrape workflow instructions -- review diffs before pushing

---

## Ecosystem: claude

Scrape Claude Code / Anthropic documentation using local plugin code at `plugins/claude-ecosystem/skills/docs-management/`.

### Step 1: Run Scraping

```bash
OFFICIAL_DOCS_DEV_ROOT="<repo-root>/plugins/claude-ecosystem/skills/docs-management" python <repo-root>/plugins/claude-ecosystem/skills/docs-management/scripts/core/scrape_all_sources.py --parallel --skip-existing
```

**STOP AND VERIFY:** Check the first lines of output for `[DEV MODE]`. If you see `[PROD MODE]`, the environment variable was not set correctly. Do NOT proceed -- troubleshoot the env var first.

### Step 2: Run Validation

```bash
OFFICIAL_DOCS_DEV_ROOT="<repo-root>/plugins/claude-ecosystem/skills/docs-management" python <repo-root>/plugins/claude-ecosystem/skills/docs-management/scripts/management/refresh_index.py
```

**STOP AND VERIFY:** Check for `[DEV MODE]` in output. If `[PROD MODE]` appears, stop and troubleshoot.

### Step 3: Run Age-Based Cleanup

Clean up Anthropic articles that have aged out based on `published_at` dates. The threshold is read automatically from `max_age_days` in `references/sources.json`.

```bash
OFFICIAL_DOCS_DEV_ROOT="<repo-root>/plugins/claude-ecosystem/skills/docs-management" python <repo-root>/plugins/claude-ecosystem/skills/docs-management/scripts/maintenance/cleanup_old_anthropic_docs.py --execute
```

**STOP AND VERIFY:** Check for `[DEV MODE]` in output. Review the cleanup summary -- it should report either "No old documents found" or list the specific files removed.

**Note:** The `--execute` flag is required to actually delete files (default is dry-run). The age threshold is read from `sources.json` automatically.

### Step 4: Git Status Check

Run `git status` to see what files changed in the local repo.

**IMPORTANT:** Only analyze and report on changes within `plugins/claude-ecosystem/`. Ignore changes in other plugins -- those are from separate scrape runs.

### Step 5: Content Diff Analysis

Analyze scraped content changes to detect potential issues from external source changes:

```bash
# Check for significant content changes in scraped docs
git diff --stat plugins/claude-ecosystem/skills/docs-management/canonical/

# Review specific changes for potential issues:
# - Broken formatting from upstream changes
# - Missing sections or content
# - New content that may need metadata updates
# - Encoding issues or unexpected characters
git diff plugins/claude-ecosystem/skills/docs-management/canonical/ | head -200
```

**What to look for:**

- **Large deletions**: May indicate upstream page restructuring or removal
- **Formatting changes**: Broken markdown, missing headers, malformed links
- **Encoding issues**: Unexpected characters, mojibake, or encoding artifacts
- **Metadata drift**: Changes that may require index.yaml updates
- **Script adjustments needed**: Patterns that suggest scraping logic needs updates

If issues are found, investigate the source URLs and determine if adjustments are needed to sources.json or scraping scripts.

### Step 6: Filter Effectiveness Analysis

After reviewing the git diff, perform a **structural analysis** to detect potential filtering gaps. This analysis should be future-proof (not relying on brittle text patterns).

**Analysis Steps:**

1. **Source Type Correlation**: Group modified files by source path prefix:
   - `anthropic-com/research/` - Research articles
   - `anthropic-com/news/` - News articles
   - `anthropic-com/engineering/` - Engineering blog
   - `code-claude-com/` - Claude Code docs
   - `docs-claude-com/` - API docs

   **Red flag:** If 5+ files from the same source all changed, this likely indicates a structural issue with that source's filtering configuration (not genuine content updates).

2. **Change Location Analysis**: For each modified file in a source group:
   - Check if changes are only in the last 20% of the file (likely footer/related sections)
   - Check if the diff shows only frontmatter (`content_hash`) changes with <10 content lines changed

   **Red flag:** Multiple files with changes concentrated at the end = likely "Related content" or footer sections not being filtered.

3. **Cross-Reference with Scraper Logs**: During scraping, the `ContentFilter` logs messages like:

   ```text
   Filtered N sections from URL: reasons=[...], headings=[...]
   ```

   **Red flag:** If files show as git-modified but scraper logs show `sections_removed: 0` for that source type = filter configuration may be missing for that source.

**Potential Improvements Output:**

If issues are detected, include a "Potential Improvements" section with actionable suggestions:

- "Consider adding `news_blog_stop_sections` to source X in `content_filtering.yaml`"
- "Filter may not be triggering for files matching pattern Y - check source_filters mapping"
- "Source Z has N files with footer-only changes - review filtering rules"

**Reference:** Filter configuration is in `plugins/claude-ecosystem/skills/docs-management/config/content_filtering.yaml`

### Step 7: Final Report

Summarize:

1. Scraping results (documents scraped, skipped, errors)
2. Validation results (index integrity, metadata coverage)
3. Age-based cleanup results (files removed, if any)
4. Content diff analysis findings (any issues detected)
5. Filter effectiveness analysis (any potential improvements identified)
6. Files ready for commit (only `plugins/claude-ecosystem/` changes)

### Step 8: Audit, Fix, and Commit

After the final report, if there are changed files ready for commit:

1. **Audit inline**: Check all modified canonical files for:
   - Encoding issues (mojibake, smart quotes, non-UTF-8 characters)
   - Broken links or malformed markdown
   - Empty/stub files with no meaningful content
   - Frontmatter inconsistencies

2. **Fix issues found**: Apply fixes directly -- do NOT write findings to a separate file

3. **Lint markdown**: Run markdownlint on modified files:

   ```bash
   npx markdownlint-cli2 --fix "plugins/claude-ecosystem/skills/docs-management/canonical/**/*.md"
   ```

4. **Commit**: Use the `melodic-software:git-commit` skill. Suggested format:
   - `feat(claude-ecosystem): re-scrape docs with [summary of changes]`
   - `fix(claude-ecosystem): fix encoding/formatting issues in scraped docs`

5. **STOP AND CONFIRM**: Present the commit plan to the user before executing

---

## Ecosystem: cursor

Scrape Cursor documentation using local plugin code at `plugins/cursor-ecosystem/skills/cursor-docs/`.

### Step 1: Run Scraping

```bash
CURSOR_DOCS_DEV_ROOT="<repo-root>/plugins/cursor-ecosystem/skills/cursor-docs" python <repo-root>/plugins/cursor-ecosystem/skills/cursor-docs/scripts/core/scrape_docs.py --llms-txt "https://cursor.com/llms.txt" --skip-existing
```

**STOP AND VERIFY:** Check the first lines of output for `[DEV MODE]`. If you see `[PROD MODE]`, the environment variable was not set correctly. Do NOT proceed -- troubleshoot the env var first.

### Step 2: Run Index Refresh (Rebuild + Extract Metadata)

Run the full index refresh pipeline which rebuilds the index AND extracts keywords/metadata:

```bash
CURSOR_DOCS_DEV_ROOT="<repo-root>/plugins/cursor-ecosystem/skills/cursor-docs" python <repo-root>/plugins/cursor-ecosystem/skills/cursor-docs/scripts/management/refresh_index.py
```

**STOP AND VERIFY:** Check for `[DEV MODE]` in output. If `[PROD MODE]` appears, stop and troubleshoot.

**IMPORTANT:** Use `refresh_index.py` (not `rebuild_index.py`). The refresh script runs the full pipeline:

1. Rebuild index from filesystem
2. Extract keywords and metadata for all documents
3. Generate summary report

Using only `rebuild_index.py` will strip metadata (keywords, subsections, tags, descriptions) from the index.

### Step 3: Run Validation

Verify index integrity:

```bash
CURSOR_DOCS_DEV_ROOT="<repo-root>/plugins/cursor-ecosystem/skills/cursor-docs" python <repo-root>/plugins/cursor-ecosystem/skills/cursor-docs/scripts/maintenance/validate_index.py
```

### Step 4: Git Status Check

Run `git status` to see what files changed in the local repo.

**IMPORTANT:** Only analyze and report on changes within `plugins/cursor-ecosystem/`. Ignore changes in other plugins -- those are from separate scrape runs.

### Step 5: Content Diff Analysis

Analyze scraped content changes to detect potential issues from external source changes:

```bash
# Check for significant content changes in scraped docs
git diff --stat plugins/cursor-ecosystem/skills/cursor-docs/canonical/

# Review specific changes for potential issues
git diff plugins/cursor-ecosystem/skills/cursor-docs/canonical/ | head -200
```

**What to look for:**

- **Large deletions**: May indicate upstream page restructuring or removal
- **Formatting changes**: Broken markdown, missing headers, malformed links
- **Encoding issues**: Unexpected characters, mojibake, or encoding artifacts
- **Metadata drift**: Changes that may require index.yaml updates
- **Script adjustments needed**: Patterns that suggest scraping logic needs updates

If issues are found, investigate the source URLs and determine if adjustments are needed to sources.json or scraping scripts.

### Step 6: Tag Distribution Analysis

After scraping, verify tag distribution is reasonable. Cursor docs use tags (not categories):

```bash
# Count documents by tag
CURSOR_DOCS_DEV_ROOT="<repo-root>/plugins/cursor-ecosystem/skills/cursor-docs" python -c "
import yaml
with open('<repo-root>/plugins/cursor-ecosystem/skills/cursor-docs/canonical/index.yaml', 'r', encoding='utf-8') as f:
    index = yaml.safe_load(f)
tags_count = {}
for doc_id, meta in index.items():
    tags = meta.get('tags', [])
    for tag in tags:
        tags_count[tag] = tags_count.get(tag, 0) + 1
for tag, count in sorted(tags_count.items(), key=lambda x: -x[1]):
    print(f'{tag}: {count}')
"
```

**Expected tags:**

| Tag | Expected Range |
| --- | -------------- |
| cursor | 100-110 (all docs) |
| agent | 15-25 |
| cli | 15-25 |
| configuration | 10-20 |
| inline-edit | 10-15 |
| examples | 8-15 |
| enterprise | 5-15 |
| context | 5-10 |
| reference | 4-10 |
| mcp | 3-8 |

**Red flags:**

- Total count differs significantly from ~100-110 documents
- Missing `cursor` tag on any document (all should have it)
- Tags with 0 documents that previously had content

### Step 7: Final Report

Summarize:

1. Scraping results (documents scraped, skipped, errors)
2. Validation results (index integrity, metadata coverage)
3. Content diff analysis findings (any issues detected)
4. Tag distribution (any anomalies)
5. Files ready for commit (only `plugins/cursor-ecosystem/` changes)

### Step 8: Audit, Fix, and Commit

After the final report, if there are changed files ready for commit:

1. **Audit inline**: Check all modified canonical files for:
   - Encoding issues (mojibake, smart quotes, non-UTF-8 characters)
   - Broken links or malformed markdown
   - Empty/stub files with no meaningful content
   - Frontmatter inconsistencies

2. **Fix issues found**: Apply fixes directly -- do NOT write findings to a separate file

3. **Lint markdown**: Run markdownlint on modified files:

   ```bash
   npx markdownlint-cli2 --fix "plugins/cursor-ecosystem/skills/cursor-docs/canonical/**/*.md"
   ```

4. **Commit**: Use the `melodic-software:git-commit` skill. Suggested format:
   - `feat(cursor-ecosystem): re-scrape docs with [summary of changes]`
   - `fix(cursor-ecosystem): fix encoding/formatting issues in scraped docs`

5. **STOP AND CONFIRM**: Present the commit plan to the user before executing

---

## Ecosystem: duende

Scrape Duende IdentityServer documentation using local plugin code at `plugins/duende-ecosystem/skills/duende-docs/`.

### Step 1: Run Scraping

```bash
DUENDE_DOCS_DEV_ROOT="<repo-root>/plugins/duende-ecosystem/skills/duende-docs" python <repo-root>/plugins/duende-ecosystem/skills/duende-docs/scripts/core/scrape_docs.py
```

**STOP AND VERIFY:** Check the first lines of output for `[DEV MODE]`. If you see `[PROD MODE]`, the environment variable was not set correctly. Do NOT proceed -- troubleshoot the env var first.

### Step 2: Run Index Rebuild

Rebuild the index from the freshly scraped files:

```bash
DUENDE_DOCS_DEV_ROOT="<repo-root>/plugins/duende-ecosystem/skills/duende-docs" python <repo-root>/plugins/duende-ecosystem/skills/duende-docs/scripts/management/rebuild_index.py
```

**STOP AND VERIFY:** Check for `[DEV MODE]` in output. If `[PROD MODE]` appears, stop and troubleshoot.

### Step 3: Run Validation

Verify index integrity:

```bash
DUENDE_DOCS_DEV_ROOT="<repo-root>/plugins/duende-ecosystem/skills/duende-docs" python <repo-root>/plugins/duende-ecosystem/skills/duende-docs/scripts/maintenance/validate_index.py
```

### Step 4: Git Status Check

Run `git status` to see what files changed in the local repo.

**IMPORTANT:** Only analyze and report on changes within `plugins/duende-ecosystem/`. Ignore changes in other plugins -- those are from separate scrape runs.

### Step 5: Content Diff Analysis

Analyze scraped content changes to detect potential issues from external source changes:

```bash
# Check for significant content changes in scraped docs
git diff --stat plugins/duende-ecosystem/skills/duende-docs/canonical/

# Review specific changes for potential issues
git diff plugins/duende-ecosystem/skills/duende-docs/canonical/ | head -200
```

**What to look for:**

- **Large deletions**: May indicate upstream page restructuring or removal
- **Formatting changes**: Broken markdown, missing headers, malformed links
- **Encoding issues**: Unexpected characters, mojibake, or encoding artifacts
- **Metadata drift**: Changes that may require index.yaml updates
- **Script adjustments needed**: Patterns that suggest scraping logic needs updates

If issues are found, investigate the source URLs and determine if adjustments are needed to sources.json or scraping scripts.

### Step 6: Category Distribution Analysis

After scraping, verify category distribution is reasonable:

```bash
# Count documents per category
DUENDE_DOCS_DEV_ROOT="<repo-root>/plugins/duende-ecosystem/skills/duende-docs" python <repo-root>/plugins/duende-ecosystem/skills/duende-docs/scripts/management/manage_index.py count
```

**Expected categories:**

| Category | Expected Range |
| ---------- | ---------------- |
| identityserver | 50-80 |
| bff | 20-40 |
| accesstokenmanagement | 3-10 |
| identitymodel | 1-10 |
| identitymodel-oidcclient | 3-10 |
| introspection | 2-10 |
| general | 1-5 |
| uncategorized | 100-200 |

**Red flags:**

- Categories with 0 documents (category detection broken)
- Massive increase in uncategorized (URL pattern changed)
- Total count differs significantly from ~248 documents

### Step 7: Final Report

Summarize:

1. Scraping results (documents scraped, skipped, errors)
2. Validation results (index integrity, metadata coverage)
3. Content diff analysis findings (any issues detected)
4. Category distribution (any anomalies)
5. Files ready for commit (only `plugins/duende-ecosystem/` changes)

### Step 8: Audit, Fix, and Commit

After the final report, if there are changed files ready for commit:

1. **Audit inline**: Check all modified canonical files for:
   - Encoding issues (mojibake, smart quotes, non-UTF-8 characters)
   - Broken links or malformed markdown
   - Empty/stub files with no meaningful content
   - Frontmatter inconsistencies

2. **Fix issues found**: Apply fixes directly -- do NOT write findings to a separate file

3. **Lint markdown**: Run markdownlint on modified files:

   ```bash
   npx markdownlint-cli2 --fix "plugins/duende-ecosystem/skills/duende-docs/canonical/**/*.md"
   ```

4. **Commit**: Use the `melodic-software:git-commit` skill. Suggested format:
   - `feat(duende-ecosystem): re-scrape docs with [summary of changes]`
   - `fix(duende-ecosystem): fix encoding/formatting issues in scraped docs`

5. **STOP AND CONFIRM**: Present the commit plan to the user before executing

---

## Ecosystem: google

Scrape Gemini CLI documentation using local plugin code at `plugins/google-ecosystem/skills/gemini-cli-docs/`.

### Step 1: Run Scraping

```bash
GEMINI_DOCS_DEV_ROOT="<repo-root>/plugins/google-ecosystem/skills/gemini-cli-docs" python <repo-root>/plugins/google-ecosystem/skills/gemini-cli-docs/scripts/core/scrape_all_sources.py --parallel --skip-existing
```

**STOP AND VERIFY:** Check the first lines of output for `[DEV MODE]`. If you see `[PROD MODE]`, the environment variable was not set correctly. Do NOT proceed -- troubleshoot the env var first.

### Step 2: Run Index Refresh

```bash
GEMINI_DOCS_DEV_ROOT="<repo-root>/plugins/google-ecosystem/skills/gemini-cli-docs" python <repo-root>/plugins/google-ecosystem/skills/gemini-cli-docs/scripts/management/refresh_index.py
```

**STOP AND VERIFY:** Check for `[DEV MODE]` in output. If `[PROD MODE]` appears, stop and troubleshoot.

### Step 3: Git Status Check

Run `git status` to see what files changed in the local repo.

**IMPORTANT:** Only analyze and report on changes within `plugins/google-ecosystem/`. Ignore changes in other plugins -- those are from separate scrape runs.

### Step 4: Content Diff Analysis

Analyze scraped content changes to detect potential issues from external source changes:

```bash
# Check for significant content changes in scraped docs
git diff --stat plugins/google-ecosystem/skills/gemini-cli-docs/canonical/

# Review specific changes for potential issues
git diff plugins/google-ecosystem/skills/gemini-cli-docs/canonical/ | head -200
```

**What to look for:**

- **Large deletions**: May indicate upstream page restructuring or removal
- **Formatting changes**: Broken markdown, missing headers, malformed links
- **Encoding issues**: Unexpected characters, mojibake, or encoding artifacts
- **Metadata drift**: Changes that may require index.yaml updates
- **Script adjustments needed**: Patterns that suggest scraping logic needs updates

If issues are found, investigate the source URLs and determine if adjustments are needed to sources.json or scraping scripts.

### Step 5: Filter Effectiveness Analysis

After reviewing the git diff, perform a **structural analysis** to detect potential filtering gaps.

**Analysis Steps:**

1. **Source Analysis**: Since gemini-cli-docs uses a single source (geminicli.com llms.txt), check if:
   - All expected pages are being scraped (~73 expected)
   - Any pages are consistently causing issues
   - Content structure has changed requiring filter updates

2. **Change Location Analysis**: For each modified file:
   - Check if changes are only in the last 20% of the file (likely footer/related sections)
   - Check if the diff shows only frontmatter (`content_hash`) changes with <10 content lines changed

   **Red flag:** Multiple files with changes concentrated at the end = likely footer sections not being filtered.

3. **Cross-Reference with Scraper Logs**: During scraping, check for logged messages about:
   - Skipped URLs
   - Parse errors
   - Filter operations

**Potential Improvements Output:**

If issues are detected, include a "Potential Improvements" section with actionable suggestions:

- "Consider adding filtering rules for section X in `filtering.yaml`"
- "Source structure may have changed - review llms.txt parsing"
- "N files have footer-only changes - review filtering rules"

**Reference:** Filter configuration is in `plugins/google-ecosystem/skills/gemini-cli-docs/config/filtering.yaml`

### Step 6: Final Report

Summarize:

1. Scraping results (documents scraped, skipped, errors)
2. Validation results (index integrity, metadata coverage)
3. Content diff analysis findings (any issues detected)
4. Filter effectiveness analysis (any potential improvements identified)
5. Files ready for commit (only `plugins/google-ecosystem/` changes)

### Step 7: Audit, Fix, and Commit

After the final report, if there are changed files ready for commit:

1. **Audit inline**: Check all modified canonical files for:
   - Encoding issues (mojibake, smart quotes, non-UTF-8 characters)
   - Broken links or malformed markdown
   - Empty/stub files with no meaningful content
   - Frontmatter inconsistencies

2. **Fix issues found**: Apply fixes directly -- do NOT write findings to a separate file

3. **Lint markdown**: Run markdownlint on modified files:

   ```bash
   npx markdownlint-cli2 --fix "plugins/google-ecosystem/skills/gemini-cli-docs/canonical/**/*.md"
   ```

4. **Commit**: Use the `melodic-software:git-commit` skill. Suggested format:
   - `feat(google-ecosystem): re-scrape docs with [summary of changes]`
   - `fix(google-ecosystem): fix encoding/formatting issues in scraped docs`

5. **STOP AND CONFIRM**: Present the commit plan to the user before executing

---

## Ecosystem: openai

Scrape OpenAI Codex CLI documentation using local plugin code at `plugins/openai-ecosystem/skills/codex-cli-docs/`.

### Step 1: Run Scraping

```bash
CODEX_DOCS_DEV_ROOT="<repo-root>/plugins/openai-ecosystem/skills/codex-cli-docs" python <repo-root>/plugins/openai-ecosystem/skills/codex-cli-docs/scripts/core/scrape_docs.py --parallel
```

**STOP AND VERIFY:** Check the first lines of output for `[DEV MODE]`. If you see `[PROD MODE]`, the environment variable was not set correctly. Do NOT proceed -- troubleshoot the env var first.

### Step 2: Run Index Refresh

```bash
CODEX_DOCS_DEV_ROOT="<repo-root>/plugins/openai-ecosystem/skills/codex-cli-docs" python <repo-root>/plugins/openai-ecosystem/skills/codex-cli-docs/scripts/management/refresh_index.py
```

**STOP AND VERIFY:** Check for `[DEV MODE]` in output. If `[PROD MODE]` appears, stop and troubleshoot.

### Step 3: Git Status Check

Run `git status` to see what files changed in the local repo.

**IMPORTANT:** Only analyze and report on changes within `plugins/openai-ecosystem/`. Ignore changes in other plugins -- those are from separate scrape runs.

### Step 4: Content Diff Analysis

Analyze scraped content changes to detect potential issues from external source changes:

```bash
# Check for significant content changes in scraped docs
git diff --stat plugins/openai-ecosystem/skills/codex-cli-docs/canonical/

# Review specific changes for potential issues
git diff plugins/openai-ecosystem/skills/codex-cli-docs/canonical/ | head -200
```

**What to look for:**

- **Large deletions**: May indicate upstream page restructuring or removal
- **Formatting changes**: Broken markdown, missing headers, malformed links
- **Encoding issues**: Unexpected characters, mojibake, or encoding artifacts
- **Metadata drift**: Changes that may require index.yaml updates
- **Script adjustments needed**: Patterns that suggest scraping logic needs updates

If issues are found, investigate the source URLs and determine if adjustments are needed to sources.json or scraping scripts.

### Step 5: Filter Effectiveness Analysis

After reviewing the git diff, perform a **structural analysis** to detect potential filtering gaps.

**Analysis Steps:**

1. **Source Analysis**: Check if:
   - All expected pages from llms.txt are being scraped
   - Any pages are consistently causing issues
   - Content structure has changed requiring filter updates

2. **Change Location Analysis**: For each modified file:
   - Check if changes are only in the last 20% of the file (likely footer/related sections)
   - Check if the diff shows only frontmatter (`content_hash`) changes with <10 content lines changed

   **Red flag:** Multiple files with changes concentrated at the end = likely footer sections not being filtered.

3. **Cross-Reference with Scraper Logs**: During scraping, check for logged messages about:
   - Skipped URLs
   - Parse errors
   - Filter operations

**Potential Improvements Output:**

If issues are detected, include a "Potential Improvements" section with actionable suggestions:

- "Consider adding filtering rules for section X in `filtering.yaml`"
- "Source structure may have changed - review llms.txt parsing"
- "N files have footer-only changes - review filtering rules"

**Reference:** Filter configuration is in `plugins/openai-ecosystem/skills/codex-cli-docs/config/filtering.yaml`

### Step 6: Final Report

Summarize:

1. Scraping results (documents scraped, skipped, errors)
2. Validation results (index integrity, metadata coverage)
3. Content diff analysis findings (any issues detected)
4. Filter effectiveness analysis (any potential improvements identified)
5. Files ready for commit (only `plugins/openai-ecosystem/` changes)

### Step 7: Audit, Fix, and Commit

After the final report, if there are changed files ready for commit:

1. **Audit inline**: Check all modified canonical files for:
   - Encoding issues (mojibake, smart quotes, non-UTF-8 characters)
   - Broken links or malformed markdown
   - Empty/stub files with no meaningful content
   - Frontmatter inconsistencies

2. **Fix issues found**: Apply fixes directly -- do NOT write findings to a separate file

3. **Lint markdown**: Run markdownlint on modified files:

   ```bash
   npx markdownlint-cli2 --fix "plugins/openai-ecosystem/skills/codex-cli-docs/canonical/**/*.md"
   ```

4. **Commit**: Use the `melodic-software:git-commit` skill. Suggested format:
   - `feat(openai-ecosystem): re-scrape docs with [summary of changes]`
   - `fix(openai-ecosystem): fix encoding/formatting issues in scraped docs`

5. **STOP AND CONFIRM**: Present the commit plan to the user before executing

---

## What NOT to Do

- Do NOT run scripts without the inline dev mode env var prefix
- Do NOT use PowerShell syntax (`$env:...`) in Claude Code -- use Bash inline prefix instead
- Do NOT assume env vars persist between Bash tool calls (they do not)
- Do NOT use global `/[ecosystem]:docs-ops scrape` commands (uses installed plugin)
- Do NOT run scripts in background with polling loops
- Do NOT proceed if `[PROD MODE]` appears -- stop and fix the env var
- Do NOT include changes from other plugins in the final report
- Do NOT write audit findings to a plan file -- report inline and fix directly
- Do NOT stop after scraping without completing audit/fix/commit steps
- Do NOT run multiple ecosystems that share scripts in the same headless session
- Do NOT push to remote until all scrape runs are reviewed
- Do NOT use `rebuild_index.py` alone for cursor -- use `refresh_index.py` to preserve metadata
