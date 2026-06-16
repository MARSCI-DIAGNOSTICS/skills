---
name: scrape-posts
description: Scrape new articles from Milan Jovanovic's blog (November 2025+). Optimized - pre-filters from listing page, only scrapes new articles.
argument-hint: "[--force] [--since YYYY-MM-DD] [--limit N] [--dry-run]"
allowed-tools: Read, Bash, Skill, mcp__firecrawl__firecrawl_scrape, mcp__firecrawl__firecrawl_map, mcp__firecrawl__firecrawl_search
---

# Scrape Milan Jovanovic Blog Posts

Scrape new articles from Milan Jovanovic's .NET blog with **optimized pre-filtering**. Parses dates from listing page to avoid unnecessary per-article scraping.

## Arguments

- `--force`: Re-scrape all articles (compare content hash to skip unchanged)
- `--since YYYY-MM-DD`: Custom date filter (default: 2025-11-01)
- `--limit N`: Limit number of articles (for testing)
- `--dry-run`: Preview what would be scraped without saving

## Optimized Workflow

### Step 1: Invoke Skill

Invoke the `milan-jovanovic:milan-jovanovic-blog` skill to load context and access scripts.

### Step 2: Pre-Filter from Listing Page (OPTIMIZATION)

**Key efficiency optimization:** Parse dates from listing page BEFORE scraping individual articles.

1. Scrape the blog listing page using `firecrawl_scrape`:

   ```text
   URL: https://www.milanjovanovic.tech/blog
   Format: markdown
   ```

2. Save listing content to temp file (e.g., `.claude/temp/milan-listing.md`)

3. Run pre-filter script to identify articles needing scraping:

   ```bash
   # Normal mode - only new articles
   python scripts/core/check_new_articles.py .claude/temp/milan-listing.md --json --since 2025-11-01

   # Force mode - include existing for re-check
   python scripts/core/check_new_articles.py .claude/temp/milan-listing.md --json --force --since 2025-11-01
   ```

4. Parse JSON output to get `to_scrape` list. If empty, skip to Step 5 (no scraping needed).

### Step 3: Scrape Only Needed Articles

For each article in `to_scrape`:

1. **For articles with `in_index: false`** (new):
   - Scrape full article with `firecrawl_scrape`
   - Extract publication date from metadata
   - Clean promotional content
   - Save to `canonical/milanjovanovic-tech/blog/{slug}.md`

2. **For articles with `in_index: true`** (force mode re-check):
   - Scrape full article with `firecrawl_scrape`
   - Clean promotional content
   - Generate content hash
   - Compare to `content_hash` from pre-filter output
   - If unchanged, skip writing (log as "skipped - unchanged")
   - If changed, save updated content

### Step 4: Update Index

After scraping completes:

```bash
python scripts/management/refresh_index.py
```

### Step 5: Report Statistics

Report:

- Articles found on listing page
- Articles needing scraping (new + force re-check)
- Articles skipped (already indexed, not in force mode)
- Articles skipped (unchanged content hash, force mode)
- Articles filtered (before cutoff date)
- Any errors

## Content Cleanup Patterns

The scraper removes these promotional patterns:

**Footer patterns (stop processing):**

- "Whenever you're ready, there are X ways I can help you"
- "Become a Better .NET Software Engineer"
- "Hi, I'm Milan"

**Sponsor patterns (remove section):**

- AuthKit/WorkOS mentions
- "Sponsor this newsletter" links
- Incident response sponsor content

**Inline patterns (remove):**

- Reading time ("5 min read")
- "Manage read history" links
- Empty image placeholders

## Efficiency Gains

| Scenario | Without Optimization | With Optimization |
|----------|----------------------|-------------------|
| No new articles | 10+ firecrawl requests | 1-2 requests |
| 1 new article | 10+ firecrawl requests | 2-3 requests |
| Force (unchanged) | 10+ requests | 10+ requests but skips writes |

**Why this matters:** Firecrawl has API costs and rate limits. Pre-filtering saves 80-90% of requests when articles haven't changed.

## Example Usage

```text
/milan-jovanovic:scrape-posts
/milan-jovanovic:scrape-posts --limit 3 --dry-run
/milan-jovanovic:scrape-posts --force
/milan-jovanovic:scrape-posts --since 2025-12-01
```

## Troubleshooting

### Firecrawl Not Available

If firecrawl MCP is not connected, the command will fail. Ensure the firecrawl MCP server is configured and running.

### Date Parsing Issues

If listing page dates can't be parsed, the script logs them in `no_date` category. These articles are skipped unless you provide a specific URL.

### Pre-Filter Shows 0 Articles

If `check_new_articles.py` shows 0 articles to scrape:

- All articles are already indexed (use `--force` to re-check)
- All articles are before the cutoff date (adjust `--since`)
- Listing page format changed (check regex patterns in script)
