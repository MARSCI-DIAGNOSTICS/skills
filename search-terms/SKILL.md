---
name: search-terms
description: Analyze Google Ads search term reports to discover keyword opportunities and negative keyword candidates. Use when mining for high-value queries, identifying wasted spend, optimizing match types, expanding keyword lists, classifying search intent, or generating performance insights. Reveals actual user queries triggering ads and enables data-driven campaign optimization.
---

# Search Terms Analysis

Analyze actual user queries triggering ads to identify keyword expansion opportunities, negative keyword candidates, and match type optimization insights.

## Core Analysis Framework

### Query Mining for Keyword Expansion

**Add as exact/phrase match keywords when:**
- 3+ conversions AND 30+ clicks
- Conversion rate ≥ account average
- Cost per conversion ≤ target CPA
- Search volume justifies dedicated keyword

**Expansion priority:**

| Priority | Criteria | Action |
|----------|----------|--------|
| High | 5+ conversions, CVR >average | Add as exact match immediately |
| Medium | 3-4 conversions, CVR ≥average | Add as phrase match |
| Low | 1-2 conversions, high potential | Monitor for another cycle |

### Intent Classification

Classify queries by user intent for appropriate targeting:

**Transactional:** "buy", "order", "purchase", "shop", "discount"
- High commercial intent
- Target with aggressive bidding
- Strong CTAs in ad copy

**Informational:** "how to", "what is", "guide", "tutorial"
- Research phase
- Target with educational content
- Lead magnet CTAs

**Commercial Investigation:** "best", "review", "comparison", "vs", "top"
- Consideration phase
- Target with social proof
- Comparison/review CTAs

**Navigational:** Brand names, competitor names
- High intent when it's your brand
- Exclude competitors as negatives (unless competitive strategy)

### N-Gram Analysis

Break search terms into word sequences to identify patterns:
- Accounts with 1M+ search terms typically have 30,000-50,000 unique n-grams
- Identify high-frequency phrases across queries
- Discover common modifiers ("cheap", "best", "near me")
- Scale pattern-based optimizations

**Example n-gram patterns:**
- "best [product]" - 500 queries
- "[product] near me" - 350 queries
- "cheap [product]" - 200 queries (evaluate for intent)

## Negative Keyword Discovery

### Conservative Approach (Recommended)
- 200+ clicks
- $100+ cost
- 0 conversions over 2-4 weeks
- Clear irrelevance

### Moderate Approach
- 100+ clicks
- $50+ cost
- 0 conversions
- CTR <50% of account average

### Aggressive Approach
- 50+ clicks
- $25+ cost
- 0 conversions
- Low engagement signals

**Critical:** Allow 7-14 days minimum data accumulation. Consider conversion lag time for longer sales cycles (B2B, high-ticket items).

## Google Ads API Integration

### SearchTermView Query

```sql
SELECT 
  search_term_view.search_term,
  segments.keyword.info.text,
  segments.keyword.info.match_type,
  search_term_view.status,
  campaign.name,
  ad_group.name,
  metrics.clicks,
  metrics.impressions,
  metrics.ctr,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.average_cpc
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.clicks > 0
ORDER BY metrics.cost_micros DESC
```

**Performance note:** For large datasets (10,000+ search terms), use `SearchStream` instead of `Search` for efficient streaming.

### Status Field Values

- `ADDED`: Search term added as keyword
- `EXCLUDED`: Search term excluded as negative
- `NONE`: No action taken

### Match Type Analysis

Compare actual search term vs keyword match type to evaluate match type effectiveness:

```sql
SELECT 
  segments.keyword.info.match_type,
  COUNT(DISTINCT search_term_view.search_term) as unique_queries,
  SUM(metrics.clicks) as total_clicks,
  SUM(metrics.conversions) as total_conversions,
  AVG(metrics.ctr) as avg_ctr
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
GROUP BY segments.keyword.info.match_type
```

## Performance Metrics Analysis

### Key Performance Indicators

**CTR Analysis:**
- Identify high-impression, low-click queries for ad copy optimization
- Compare CTR by match type and search intent
- Flag queries with CTR <50% of average as potential negatives

**Conversion Rate Analysis:**
- Identify high-converting query patterns for keyword expansion
- Compare CVR by query length (short vs long-tail)
- Find queries with high CVR but low volume for budget reallocation

**Cost Efficiency:**
- Calculate cost per conversion by query
- Identify expensive queries with poor ROAS
- Find underutilized high-performers for increased bids

### 2025 Benchmark Data

| Metric | Average | Strong | Excellent |
|--------|---------|--------|-----------|
| CTR | 6.66% | 8%+ | 10%+ |
| CPC | $5.26 | Below industry avg | <$3 |
| CVR | 7.52% | 10%+ | 15%+ |
| CPL | $70.11 | <$50 | <$30 |

**Industry variations:**
- Arts & Entertainment: 13.10% CTR
- Sports & Recreation: 9.66% CTR
- Real Estate: 9.20% CTR
- Finance: Lower CTR, higher CPC

## Analysis Workflow

### Daily Monitoring
- Review top 20 search terms by cost
- Flag new queries with 0 conversions and $25+ spend
- Identify emergency negative keyword candidates

### Weekly Deep Dive
1. Export search term report (last 30 days)
2. Filter by cost threshold ($50+)
3. Segment by performance tier:
   - Winners: 3+ conversions
   - Potentials: 1-2 conversions
   - Losers: 0 conversions, high cost
4. Generate recommendations:
   - Keywords to add
   - Negatives to implement
   - Match type adjustments
   - Bid modifications

### Monthly Strategic Review
1. N-gram analysis for pattern identification
2. Intent classification and segmentation strategy
3. Match type effectiveness evaluation
4. Long-tail vs. short-tail performance comparison
5. Geographic and device-specific query insights

## Common Insights and Actions

### Insight: High volume query not in keyword list
**Action:** Add as exact or phrase match keyword with dedicated budget

### Insight: Misspellings triggering ads
**Decision:** 
- If converting: Let match type handle it
- If not converting: Add as negative (remember: negatives don't catch variants)

### Insight: Branded queries on non-brand campaigns
**Action:** Add brand terms as campaign-level negatives on non-brand campaigns

### Insight: Geographic modifiers in queries
**Action:** Consider geo-targeted campaigns or location-based ad copy

### Insight: Question queries triggering ads
**Action:** Create content-focused ad copy addressing questions

## Automation Opportunities

### Automated Flagging System

**High-priority alerts:**
- Queries with $100+ spend, 0 conversions
- New queries with 50+ clicks in 24 hours
- Performance anomalies (sudden CTR/CVR drops)

**Weekly automated report:**
- Top 50 queries by spend with performance metrics
- Negative keyword candidates (meeting thresholds)
- Keyword expansion opportunities (3+ conversions)
- Match type effectiveness summary

### API-Driven Workflow

```python
# Pseudocode for automated discovery
search_terms = fetch_search_terms(last_30_days)

for term in search_terms:
    if term.clicks > 100 and term.conversions == 0 and term.cost > 50:
        flag_as_negative_candidate(term)
    elif term.conversions >= 3 and term.clicks >= 30:
        flag_as_keyword_opportunity(term)
    elif term.ctr < account_average_ctr * 0.5:
        flag_for_review(term, reason="low_ctr")

generate_weekly_report(flagged_terms)
```

## Match Type Optimization Insights

### Exact Match Performance
- Review queries triggering exact match keywords
- Validate queries match intent precisely
- Consider close variant performance

### Phrase Match Expansion
- Identify patterns in phrase match queries
- Evaluate if broader terms would improve reach
- Check for unwanted queries (add as negatives)

### Broad Match Monitoring
- Closely monitor broad match queries for relevance
- Quick negative keyword implementation
- Consider moving high-performers to phrase/exact

## Integration with Other Skills

- **negative-keywords:** Primary source for negative keyword discovery
- **rsa-generator:** Use high-performing queries as headline inspiration
- **pmax-auditor:** Apply search term insights to PMax campaigns

For query classification templates, see references/intent-classification.md
For automation scripts, see scripts/search-term-analyzer.py
