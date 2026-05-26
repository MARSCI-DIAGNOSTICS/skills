---
name: rsa-generator
description: Generate high-performing Responsive Search Ads for Google Ads with optimized headlines and descriptions. Use when creating RSAs, improving Ad Strength, optimizing asset combinations, writing ad copy, testing headline variations, or implementing dynamic keyword insertion. Requires 15 unique headlines and 4 descriptions for maximum effectiveness and Ad Strength ratings.
---

# Responsive Search Ad Generator

Generate high-performing RSAs with optimal headline diversity, Ad Strength optimization, and strategic asset pinning for Google Ads Search campaigns.

## Core Requirements

### Character Limits (Strict)
- Headlines: 30 characters each
- Descriptions: 90 characters each
- Display paths: 15 characters each (2 paths)

### Asset Volume
- Headlines: 5 minimum, 15 maximum
- Descriptions: 2 minimum, 4 maximum

**Critical:** Headlines must be genuinely unique. Google won't show ads with too-similar headlines. Avoid simple variations like "Buy Now" vs "Buy Today" vs "Buy Here".

## Headline Diversity Framework

| Category | Quantity | Purpose | Examples |
|----------|----------|---------|----------|
| Keyword-Focused | 2-3 | Include primary keywords verbatim | "Running Shoes Sale", "Buy Running Shoes" |
| USP/Value Props | 3-4 | Highlight unique benefits | "Free Shipping Always", "30-Day Returns" |
| CTAs | 2-3 | Action-oriented phrases | "Shop Now & Save 20%", "Get Yours Today" |
| Brand Headlines | 2-3 | Brand name, trust signals | "[Brand] Since 1990", "Trusted By 1M+" |
| Dynamic/Customizer | 2-3 | DKI, location, countdown | "{KeyWord:Running Shoes}", "2 Days Left!" |

### Dynamic Keyword Insertion (DKI)

**Syntax:** `{KeyWord:Default Text}`
**Capitalization options:**
- `{KeyWord:Default}` - Capitalizes first letter of each word
- `{Keyword:Default}` - Capitalizes first letter only
- `{keyword:Default}` - All lowercase
- `{KEYWORD:DEFAULT}` - All uppercase

**Default text must:**
- Fit within 30 character limit
- Make sense when DKI doesn't trigger
- Be relevant to ad group theme

**Example:** `{KeyWord:Athletic Shoes}` → Shows "Running Shoes" if query matches, otherwise "Athletic Shoes"

## Ad Strength Optimization

### Ad Strength Correlation
- Ad Strength correlates with impressions 56.8% of the time
- Improving Poor → Excellent = +12-15% more conversions (Google data)
- Ad Strength does NOT affect serving eligibility
- Average-strength ads can outperform Excellent-strength ads on ROAS

### Achieving Excellent Ad Strength

**Requirements:**
1. Use 10+ unique headlines
2. Use 4 descriptions
3. Include at least 1 keyword in 2+ headlines
4. Headlines vary significantly in message/structure
5. Add 2+ descriptions with unique messaging
6. Avoid excessive pinning

**Pinning Impact:** Excessive pinning almost guarantees you won't achieve Excellent. Only pin for compliance requirements (legal disclaimers, brand messaging requirements).

### Ad Strength Ratings

| Rating | Impressions Correlation | Performance Impact |
|--------|------------------------|---------------------|
| Poor | Low | Baseline |
| Average | Medium | May perform well despite rating |
| Good | High | +5-10% conversions vs Poor |
| Excellent | Highest | +12-15% conversions vs Poor |

## Copywriting Frameworks

### Framework 1: Problem → Solution → Proof
```
Headline 1: [Pain Point] Solved
Headline 2: [Solution/Product]
Headline 3: [Social Proof/Trust Signal]
Description: Address problem, introduce solution, provide proof, CTA
```

### Framework 2: Feature → Benefit → Urgency
```
Headline 1: [Key Feature]
Headline 2: [Primary Benefit]
Headline 3: [Urgency/Scarcity]
Description: Explain feature, elaborate benefit, create urgency, CTA
```

### Framework 3: Question → Answer → Action
```
Headline 1: [Question]
Headline 2: [Answer/Solution]
Headline 3: [CTA]
Description: Expand on solution, address objections, strong CTA
```

## Description Writing Strategy

**Description 1:** Primary value proposition + benefits
- 60-90 characters
- Include main keywords
- Clear differentiation

**Description 2:** Secondary benefits + CTA
- 60-90 characters
- Additional USPs
- Strong call-to-action

**Description 3:** Social proof + urgency (if using 4)
- Testimonials, ratings, awards
- Scarcity/urgency elements
- Alternative CTA

**Description 4:** Feature details + guarantee (if using 4)
- Specific features
- Risk reversal (guarantee, returns)
- Supplementary CTA

## Google Ads API Implementation

### RSA Creation Structure

```python
from google.ads.googleads.client import GoogleAdsClient

# Create RSA
ad_group_ad_service = client.get_service("AdGroupAdService")
ad_group_ad_operation = client.get_type("AdGroupAdOperation")
ad = ad_group_ad_operation.create.ad

# Set RSA type
ad.responsive_search_ad.CopyFrom(
    client.get_type("ResponsiveSearchAdInfo")
)

# Add headlines
for headline_text in headline_list:  # List of up to 15 headlines
    headline = client.get_type("AdTextAsset")
    headline.text = headline_text
    # Optional: Pin to position
    # headline.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    ad.responsive_search_ad.headlines.append(headline)

# Add descriptions
for description_text in description_list:  # List of up to 4 descriptions
    description = client.get_type("AdTextAsset")
    description.text = description_text
    ad.responsive_search_ad.descriptions.append(description)

# Set display paths
ad.responsive_search_ad.path1 = "path1"  # 15 chars max
ad.responsive_search_ad.path2 = "path2"  # 15 chars max

# Set final URL
ad.final_urls.append("https://example.com/landing-page")

# Assign to ad group
ad_group_ad_operation.create.ad_group = ad_group_resource_name

# Execute
response = ad_group_ad_service.mutate_ad_group_ads(
    customer_id=customer_id,
    operations=[ad_group_ad_operation]
)
```

### Asset Performance Retrieval

```sql
SELECT 
  ad_group_ad_asset_view.ad_group_ad,
  ad_group_ad_asset_view.asset,
  ad_group_ad_asset_view.field_type,
  ad_group_ad_asset_view.performance_label,
  ad_group_ad_asset_view.enabled,
  metrics.impressions,
  metrics.clicks,
  metrics.conversions,
  metrics.cost_micros
FROM ad_group_ad_asset_view
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group.id = {ad_group_id}
ORDER BY metrics.impressions DESC
```

**Performance labels:** BEST, GOOD, LOW, LEARNING, PENDING

**Optimization strategy:** Replace LOW performers every 2-4 weeks with variations inspired by BEST performers.

## Performance Benchmarks (2024)

### Industry Averages

| Industry | Average CTR | Average CPC |
|----------|-------------|-------------|
| Arts & Entertainment | 13.04% | $1.72 |
| Real Estate | 9.20% | $2.10 |
| B2B | ~3.5% | Varies |
| Attorneys & Legal | 5.30% | $8.94 |

### General Performance
- Average Search CTR: 6.42% (up from 6.11% in 2023)
- RSAs achieve 5-15% higher CTR vs standard search ads
- RSAs achieve 7% more conversions vs standard search ads

## Common Mistakes to Avoid

### 1. Repetitive Headlines
❌ "Buy Now", "Buy Today", "Buy Here"
✅ "Shop Premium Selection", "Order with Free Shipping", "Get 20% Off Today"

### 2. Over-Pinning
❌ Pinning 5+ headlines to specific positions
✅ Pin only for compliance (legal disclaimers, required brand mentions)

### 3. Keyword Stuffing
❌ "Running Shoes Running Shoes Run"
✅ Natural language with keywords integrated: "Shop Running Shoes for Marathon Training"

### 4. Missing CTAs
❌ Only descriptive headlines
✅ Include 2-3 action-oriented headlines

### 5. Ignoring Mobile Preview
❌ Assuming all combinations work on mobile
✅ Test headline combos at 30 char display limit

## Testing Framework

### Phase 1: Asset Testing (2-3 weeks)
- Launch RSA with full asset set (15 headlines, 4 descriptions)
- Monitor asset performance labels
- Identify BEST and LOW performers

### Phase 2: Optimization (Ongoing)
- Replace LOW performers every 2-4 weeks
- Create variations of BEST performers
- Test new angles and messaging

### Phase 3: Scale Winners
- Apply best-performing asset patterns across ad groups
- Build asset library of proven performers
- Continuously refresh creative every 4-6 weeks

## Asset Refresh Cadence

**Monthly:** Review performance labels, replace LOW assets
**Quarterly:** Full creative refresh with new angles
**Bi-annually:** Complete messaging overhaul

## Integration with Other Skills

- **search-terms:** Use high-performing search terms as headline inspiration
- **pmax-auditor:** Apply RSA best practices to PMax asset groups
- **ad-copy:** Adapt copywriting frameworks for Meta platform

For headline templates by industry, see references/headline-templates.md
For DKI advanced techniques, see references/dki-guide.md
