---
name: negative-keywords
description: Manage Google Ads negative keywords to prevent ads from showing for irrelevant searches. Use when analyzing search terms, reducing wasted spend, improving CTR and conversion rates, managing negative keyword lists, or implementing automated negative keyword discovery. Improves CTR by 10-25% and reduces wasted spend by 10-20%.
---

# Negative Keywords Management

Prevent ads from showing for irrelevant searches through strategic negative keyword implementation. This skill covers match type selection, list management, API integration, and automated discovery workflows.

## Core Concepts

### Match Type Behavior (Critical Differences from Positive Keywords)

Negative keywords do NOT match close variants, synonyms, or misspellings. Each variation must be added explicitly.

| Match Type | Syntax | Blocks | Best Use Case |
|------------|--------|--------|---------------|
| **Negative Broad** | keyword | Queries containing ALL terms (any order) | Multi-word exclusions |
| **Negative Phrase** | "keyword" | Exact phrase in specified order | Order-sensitive terms |
| **Negative Exact** | [keyword] | Only that exact query | Traffic sculpting between ad groups |

**Example:** Negative broad `running shoes` blocks "red running shoes" and "shoes for running" but NOT "running socks" or "red shoes"

### List Level Selection

**Campaign-level negatives:**
- Universal exclusions across entire campaign
- Brand terms in non-brand campaigns
- Competitor names, job-related terms ("jobs", "careers", "salary")
- Industry-wide irrelevant terms

**Ad group-level negatives:**
- Traffic sculpting between ad groups
- Prevents internal competition
- More granular control for tight theme groups

**Shared negative keyword lists:**
- Apply same list to multiple campaigns
- Maximum 5,000 keywords per list
- Maximum 20 lists per account
- Account-level limit: 1,000 negatives

## Implementation Workflow

### Discovery Phase Thresholds

**High confidence (auto-add):**
- 100+ clicks AND 0 conversions AND $50+ cost
- Clear irrelevance to business offering

**Medium confidence (review required):**
- 50-100 clicks
- Conversion rate <50% of account average
- Ambiguous relevance

**Low confidence (monitor):**
- <50 clicks (insufficient data)
- Recently added keywords
- Seasonal terms

### Google Ads API Integration

**GAQL query for retrieving negatives:**
```sql
SELECT 
  shared_criterion.keyword.text,
  shared_criterion.keyword.match_type,
  shared_set.id,
  shared_set.name
FROM shared_criterion
WHERE shared_set.id IN ({shared_set_ids})
```

**Creating shared negative keyword lists:**
1. Create SharedSet (type: NEGATIVE_KEYWORDS)
2. Add keywords via SharedCriterionService with KeywordInfo
3. Attach to campaigns via CampaignSharedSetService

**Platform limits:**
- 5,000 keywords per shared list
- 20 lists per account
- 1,000 account-level negatives

## Common Pitfalls

### Over-Aggressive Blocking
❌ **Bad:** Adding "cheap" as broad negative blocks "cheap designer shoes"
✅ **Good:** Adding "cheap [product]" as phrase negative

### Negative Keyword Conflicts
Critical: Campaign positive keyword conflicts with negative stops ad serving entirely

### Search Query Position Limit
Platform limitation: Negative keywords won't block terms appearing after the 16th word position in queries

## Performance Impact Metrics

Expected improvements:
- CTR increase: 10-25%
- Wasted spend reduction: 10-20%
- Conversion rate improvement: 5-15%
- Quality Score improvement across affected keywords

## Best Practices

1. Start conservative with exact/phrase matches
2. Document reasoning for each negative
3. Monitor impact after bulk additions
4. Create themed lists (brand, job terms, competitors)
5. Quarterly review to remove outdated negatives
6. Test on single campaign first (7 days) before expanding
7. Use shared lists for universal exclusions

## Automation Workflow

Weekly automated discovery:
1. Filter search terms: 100+ clicks, 0 conversions, $50+ cost
2. Remove terms matching existing positive keywords
3. Check against existing negatives
4. Calculate potential savings
5. Generate recommendations by match type

For detailed API implementation, see references/google-ads-api.md
