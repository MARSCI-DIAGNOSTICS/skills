---
name: audience-builder
description: Build and optimize Meta audiences including Custom Audiences, Lookalike Audiences, and Saved Audiences for full-funnel targeting. Use when creating audiences, segmenting customers, building lookalikes, managing audience overlap, implementing exclusion strategies, or optimizing audience performance. Post-iOS 14.5, first-party data maximization is critical for targeting effectiveness.
---

# Meta Audience Builder

Build high-performing audiences for Meta advertising using Custom Audiences, Lookalike Audiences, and strategic segmentation for full-funnel targeting.

## Audience Types Overview

### Custom Audiences (First-Party Data)

| Type | Data Source | Best Use Case | Match Rate |
|------|-------------|---------------|------------|
| Website Custom | Pixel tracking | Retarget by pages/actions | 60-80% |
| Customer List | CSV upload | Re-engage existing customers | 50-70% |
| App Activity | SDK events | Target by in-app behavior | 70-85% |
| Engagement | Platform interactions | Video viewers, page engagers | 80-95% |
| Offline Activity | Offline events API | In-store visitors, phone leads | 40-60% |

### Lookalike Audiences (Modeled)

Create audiences similar to your best customers based on source audience patterns.

**Percentage sizes (US):**
- 1%: ~2.8 million (most similar)
- 2-3%: ~5.6-8.4 million (strong balance)
- 5%: ~14 million (broader reach)
- 10%: ~28 million (awareness scale)

### Saved Audiences (Interest/Demographic)

Target by interests, behaviors, demographics, and connections.

## Custom Audience Creation

### Website Custom Audiences

**Setup requirements:**
- Meta Pixel installed and firing events
- Sufficient traffic (1,000+ visitors minimum)
- Event optimization for key actions

**Segmentation strategies:**

**By engagement depth:**
- All website visitors (30 days)
- Product page viewers (14 days)
- Add to cart (7 days)
- Initiated checkout but not purchased (3 days)

**By product interest:**
- Category page visitors
- Specific product viewers
- Search behavior
- Time on site thresholds

**Retention periods:**
- General browsing: 30 days
- Product interest: 14-30 days
- Cart abandonment: 3-7 days
- Post-purchase: 180 days (for upsells)

### Customer List Audiences

**Data requirements:**
- Minimum: 100 records (but 1,000+ optimal)
- Multiple identifiers increase match rates
- PII must be hashed with SHA-256

**Optimal data fields:**
- Email (required minimum)
- Phone number (international format)
- First name
- Last name
- City, state, country
- Date of birth
- Gender

**Match rate optimization:**
```
Email only: 40-50% match
Email + phone: 55-65% match
Email + phone + name: 60-70% match
All fields: 70-80% match
```

**Value-based lists:**
- High lifetime value customers (top 20%)
- Recent purchasers (last 30 days)
- Frequent buyers (3+ purchases)
- High average order value (top 25%)

**CSV format requirements:**
- UTF-8 encoding
- No headers (or check "data has headers")
- One identifier per column
- Maximum file size: 500 MB
- Maximum 500 million people

### Engagement Audiences

**Video engagement:**
- ThruPlay (15 seconds or 97% completion)
- 25%, 50%, 75%, 95% watched
- 3-second views (for hook testing)

**Page engagement:**
- People who engaged with page (any interaction)
- People who visited page
- People who engaged with posts/ads

**Lead form:**
- Opened form but didn't submit
- Submitted form (for exclusion or nurture)

**Retention periods:**
- Video views: 30-365 days
- Page engagement: 365 days max
- Lead forms: 90 days

## Lookalike Audience Strategy

### Source Audience Best Practices

**Size recommendations:**
- Minimum: 100 people
- Optimal: 1,000-5,000 people
- Maximum: 50,000 people (diminishing returns)

**Quality over quantity:**
- Use high-value customers, not all purchasers
- Include RFM (Recency, Frequency, Monetary) scores
- Segment by product category for category-specific lookalikes
- Use conversion-based audiences (purchasers > add-to-cart)

**Value-Based Lookalikes (LTV):**
Upload customer list with purchase value data - Meta prioritizes similar high-value users

### Percentage Selection Strategy

**1% Lookalike:**
- Most similar to source
- Highest conversion rate
- Best for initial testing
- Recommended for high-ticket products
- Smallest reach (~2.8M US)

**2-3% Lookalike:**
- Strong similarity maintained
- Balanced reach and relevance
- Good for scaling winners
- Recommended for most campaigns

**5-7% Lookalike:**
- Broader reach for awareness
- Lower conversion rates
- Better for brand building
- Testing cold audiences

**10% Lookalike:**
- Maximum reach (28M+ US)
- Lowest similarity
- Top-of-funnel awareness only
- Not recommended for conversion campaigns

### Lookalike Refresh Frequency

Lookalikes auto-refresh every 3-7 days when actively used in running campaigns. Source audience updates don't require manual lookalike recreation.

## Audience Overlap Management

### Overlap Assessment

Use Meta's Audience Overlap Tool:
1. Navigate to Audiences
2. Select 2-5 audiences
3. Click Actions > Show Audience Overlap

**Overlap thresholds:**
- <15%: Acceptable overlap
- 15-30%: Minor concern, monitor
- 30-50%: Significant overlap, restructure recommended
- >50%: High overlap, campaigns competing against each other

### Overlap Reduction Strategies

**1. Audience stacking:**
Instead of separate campaigns, use Advantage+ audience controls (suggestions, not hard targeting)

**2. Sequential exclusions:**
- TOF campaign: Broad audience
- MOF campaign: Engaged audience, exclude purchasers
- BOF campaign: Cart abandoners, exclude recent purchasers

**3. Funnel-based exclusions:**
```
Prospecting → Exclude all purchasers (180 days)
Retargeting → Exclude recent purchasers (7-14 days)
Loyalty → Include only purchasers (90+ days ago)
```

## Exclusion Strategy

### Standard Exclusions

**Prospecting campaigns:**
- Exclude all purchasers (180 days)
- Exclude cart abandoners (7 days)
- Exclude recent website visitors (3 days) - optional

**Retargeting campaigns:**
- Exclude recent purchasers (7-14 days)
- Exclude current subscribers (for lead gen)

**Product-specific campaigns:**
- Exclude purchasers of that product (365 days)
- Exclude purchasers of competing products (optional)

### Time-Based Exclusions

- Recent converters: 7-14 days (reduce frequency)
- Long-term purchasers: 365 days+ (unless retention)
- Lapsed customers: >90 days no purchase (re-engagement)

## Meta Marketing API Integration

### Create Custom Audience

```
POST /{ad_account_id}/customaudiences

{
  "name": "Website Visitors Last 30 Days",
  "subtype": "WEBSITE",
  "description": "All website visitors in last 30 days",
  "customer_file_source": "USER_PROVIDED_ONLY",
  "retention_days": 30
}
```

### Create Lookalike Audience

```
POST /{ad_account_id}/customaudiences

{
  "name": "1% Lookalike - High Value Purchasers",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "{source_audience_id}",
  "lookalike_spec": {
    "type": "similarity",
    "ratio": 0.01,
    "country": "US",
    "starting_ratio": 0.0,
    "is_financial_service": false
  }
}
```

### Add Users to Custom Audience (Customer List)

```
POST /{custom_audience_id}/users

{
  "payload": {
    "schema": ["EMAIL", "PHONE", "FN", "LN"],
    "data": [
      ["a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3", 
       "2c4c7a7a85ced28d18ccf2b90be71fa6a5a370e7ea5f27f2d8e0e8c5eaf15b38",
       "joe",
       "smith"],
      // More rows...
    ]
  }
}
```

**Note:** All PII must be normalized and SHA-256 hashed before sending.

### Check Audience Size

```
GET /{custom_audience_id}
?fields=approximate_count_lower_bound,approximate_count_upper_bound,time_updated
```

Audience must have 1,000+ users to be usable in campaigns.

## Audience Size Optimization

### Minimum Viable Audience Sizes

| Campaign Objective | Minimum Size | Recommended Size |
|--------------------|--------------|------------------|
| Conversions | 1,000 | 50,000+ |
| Traffic | 1,000 | 100,000+ |
| Awareness | 10,000 | 500,000+ |
| Engagement | 1,000 | 100,000+ |

**Too small (<1,000):**
- Won't spend budget
- Limited delivery
- Unstable performance

**Too large (>10M):**
- Diluted relevance
- Higher CPMs
- Lower conversion rates

**Sweet spot:** 50,000 - 2,000,000 for most conversion campaigns

## Performance Benchmarks by Audience Type

### CPM Ranges (2024)

| Audience Type | CPM Range | Typical Use |
|---------------|-----------|-------------|
| Prospecting (Broad) | $5-8 | Cold TOF |
| Interest-Based | $7-12 | Warm TOF |
| Lookalike 1% | $8-12 | Prospecting |
| Website Retargeting | $10-18 | MOF/BOF |
| Customer List Retargeting | $12-20 | Loyalty/Upsell |

**Higher CPMs don't always mean worse performance** - evaluate by CPA and ROAS, not just CPM.

## Advanced Strategies

### Audience Layering

**Narrow targeting (use sparingly):**
- Demographics + interests + behaviors
- Example: "Women 25-45 AND interested in yoga AND purchased health products"

**Broad targeting with exclusions (recommended):**
- Broad audience or lookalike
- Strategic exclusions only
- Let Meta's algorithm optimize

### Custom Combination Audiences

Combine multiple sources:
- Website visitors (30d) + customer list + engagement audiences
- Create unified audience for lookalike source

### Audience Testing Framework

**Phase 1: Broad Testing (Week 1-2)**
- Test 1% LAL vs. 3% LAL vs. 5% LAL
- Equal budgets
- Measure CPA and ROAS

**Phase 2: Refinement (Week 3-4)**
- Scale winners with 2x budget
- Test variations of winner (demographic overlays)
- Pause losers

**Phase 3: Optimization (Week 5+)**
- Implement exclusion strategies
- Expand winners with larger % lookalikes
- Refresh creative for fatigued audiences

## Common Mistakes to Avoid

### 1. Over-Segmentation
❌ Creating 20 micro-audiences with <10,000 each
✅ Consolidate into 3-5 meaningful segments

### 2. Ignoring Audience Overlap
❌ Running 5 campaigns targeting overlapping audiences
✅ Use overlap tool, implement exclusions

### 3. Not Refreshing Customer Lists
❌ Uploading once and never updating
✅ Update monthly or weekly for active campaigns

### 4. Wrong Lookalike Source
❌ Using all website visitors as source
✅ Using high-value purchasers only

### 5. Excessive Exclusions
❌ Excluding too many people (audience too small)
✅ Strategic exclusions only (recent converters, competitors)

## Integration with Other Skills

- **asc-auditor:** Use audience signals in ASC campaigns
- **creative-analyzer:** Test creative variations by audience segment
- **ad-copy:** Customize messaging by audience type
- **hook-optimizer:** Tailor hooks to audience awareness level

For audience templates by vertical, see references/audience-templates.md
For API integration guide, see references/meta-marketing-api.md
