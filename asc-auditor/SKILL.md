---
name: asc-auditor
description: Audit Advantage+ Shopping Campaigns (ASC) on Meta to evaluate campaign health, identify optimization opportunities, and ensure proper setup. Use when evaluating ASC performance, verifying conversion tracking (Pixel + CAPI), analyzing creative assets, assessing budget allocation, reviewing audience signals, or generating audit reports. ASC campaigns drive 12-17% lower CPA and 25-34% higher ROAS vs standard campaigns.
---

# Advantage+ Shopping Campaign Auditor

Comprehensive audit framework for Meta's Advantage+ Shopping Campaigns (ASC) covering conversion tracking, creative assets, budget optimization, and performance benchmarking.

## Critical Context

**ASC API Deprecation Timeline:**
- No new ASC campaigns via legacy API after October 2025 (v24.0)
- Complete ASC API deprecation Q1 2026 (v25.0)
- Use new Advantage+ State fields (API v23.0+)

**ASC advantage_state values:**
- `ADVANTAGE_PLUS_SALES`
- `ADVANTAGE_PLUS_APP`
- `ADVANTAGE_PLUS_LEADS`
- `DISABLED` (standard campaigns)

## Audit Framework (6 Critical Components)

### 1. Conversion Tracking Verification

**Critical setup requirements:**

**Pixel + CAPI Dual Implementation:**
- Meta Pixel installed on website
- Conversions API (CAPI) implemented server-side
- Both sending same events with deduplication
- `event_id` parameter matching between Pixel and CAPI

**Event Match Quality (EMQ) Score:**
- Minimum acceptable: 6/10
- Target: 8+/10
- Check: Events Manager > Data Sources > Overview

**EMQ score factors:**
- Customer information parameters (email, phone, first name, last name)
- Event data quality
- Proper hashing of PII data
- Browser user agent matching

**Validation steps:**
1. Test Events tool shows events firing correctly
2. EMQ score visible in Events Manager
3. Deduplication working (not double-counting events)
4. Conversion attribution window set appropriately (7-day click, 1-day view recommended)

### 2. Budget and Structure Assessment

**Budget adequacy formula:**
Daily budget = 2-3x break-even cost per purchase

**Example:** If target CPA is $25, daily budget should be $50-75 minimum

**Budget pacing indicators:**
- **Spending full budget:** Good pacing
- **Under-spending:** Targeting too narrow, creative weak, or bids too low
- **Budget limited:** Increase budget 20-30% to unlock volume

**Existing customer budget cap:**
- 0-10% for prospecting campaigns
- 50-100% for retention/loyalty campaigns
- Configure based on business goals

### 3. Creative Volume and Diversity

**Minimum requirements:**
- 10-20 creative combinations minimum
- Meta recommends up to 150 combinations
- Mix of formats: images, videos, carousels
- Multiple aspect ratios (1:1, 4:5, 9:16)

**Creative diversity criteria:**
- Different visual styles
- Varied messaging angles
- Multiple hooks for videos
- UGC vs. polished content mix
- Product-focused vs. lifestyle imagery

**Refresh cadence:**
- Add 3-5 new creatives every 2-3 weeks
- Pause creatives with frequency >3.0
- Replace creatives showing fatigue signals

### 4. Learning Phase Analysis

**Learning phase duration:**
- Target: Complete within 7 days
- Acceptable: 7-14 days
- Concerning: 14+ days (insufficient conversions)

**Learning phase requirements:**
- 50 optimization events (purchases/leads) within 7 days
- Stable budget (no major changes)
- Stable targeting (no major changes)

**Stuck in learning:**
- **Cause:** <50 conversions per week
- **Fix:** Consolidate campaigns, increase budget, or shift to lower-funnel conversion events

### 5. Frequency Monitoring

**Frequency thresholds:**

| Campaign Type | Warning | Critical | Action |
|---------------|---------|----------|--------|
| Prospecting | 2.5 | 3.0 | Add creative, expand audience |
| Retargeting | 4.0 | 5.0 | Refresh creative, reduce spend |

**High frequency impacts:**
- CTR decline
- CPC increase
- CPM increase
- Creative fatigue
- Negative brand perception

### 6. Performance vs. Benchmarks

**Benchmark comparison:**

| Metric | Average | Good | Excellent |
|--------|---------|------|-----------|
| ROAS | 2.19-2.98x | 3.0x+ | 4.0x+ |
| CPA | $37 | Below target | <$20 |
| CPM | $10.88-$12 | <$10 | <$8 |
| Frequency | <2.5 | <2.0 | <1.5 |

**Meta study results:**
- ASC drives 12-17% lower CPA vs standard campaigns
- ASC drives 25-34% higher ROAS vs standard campaigns

## Health Score Calculation (100-Point System)

| Component | Weight | Scoring Criteria |
|-----------|--------|------------------|
| ROAS vs. Target | 25% | Exceeds (10), Meets (7), Within 20% (5), Below (0) |
| CPA vs. Target | 20% | Exceeds (10), Meets (7), Within 20% (5), Below (0) |
| Creative Health | 15% | 10+ fresh creatives (10), 5-9 (6), <5 (0) |
| Tracking Quality | 15% | EMQ 8+ (10), EMQ 6-7 (6), EMQ <6 (0) |
| Budget Efficiency | 10% | Exited learning (10), In learning (5), Stuck (0) |
| Frequency | 10% | <2.5 prospecting (10), 2.5-3.0 (5), >3.0 (0) |
| Asset Diversity | 5% | 4+ formats (5), 2-3 formats (3), 1 format (0) |

**Score interpretation:**
- 80-100: Excellent health, ready for scaling
- 60-79: Good health, minor optimizations needed
- 40-59: Warning, action required within 1 week
- <40: Critical issues, immediate intervention needed

## Meta Marketing API Integration

### Campaign-Level Insights

```
GET /{campaign-id}/insights
?fields=spend,impressions,cpm,ctr,cpc,actions,conversions,purchase_roas,frequency
&date_preset=last_30d
&action_attribution_windows=['7d_click','1d_view']
```

**Key metrics to monitor:**
- `spend` - Total spend
- `cpm` - Cost per 1,000 impressions
- `frequency` - Average impressions per person
- `purchase_roas` - Return on ad spend
- `actions` - Breakdown by action type
- `conversions` - Total conversions

### New Advantage+ State Fields (v23.0+)

```
GET /{campaign-id}
?fields=name,status,objective,advantage_state,smart_promotion_type
```

**advantage_state values:**
- `ADVANTAGE_PLUS_SALES` - ASC campaign
- `ADVANTAGE_PLUS_APP` - Advantage+ App campaigns
- `ADVANTAGE_PLUS_LEADS` - Advantage+ Lead campaigns
- `DISABLED` - Standard campaign

**smart_promotion_type:**
- `GUIDED_CREATION` - Migrated from manual to ASC
- `null` - Standard campaigns

### Ad-Level Creative Analysis

```
GET /{ad-id}/insights
?fields=impressions,clicks,spend,actions,frequency,cpm
&date_preset=last_30d
&breakdowns=publisher_platform
```

Identify:
- Top-performing creative by ROAS
- Creative with high frequency (>3.0)
- Creative with declining performance (CTR drop >20%)

## Common Issues and Fixes

### Issue: Low ROAS

**Potential causes:**
- Poor product-market fit
- Weak creative assets
- Unrealistic targets
- Insufficient budget for learning
- Landing page conversion issues

**Diagnostic steps:**
1. Check landing page conversion rate (benchmark: 2%+)
2. Analyze creative CTR (benchmark: 1.5%+)
3. Review audience fit (use Meta's audience insights)
4. Verify pricing competitiveness

**Fixes:**
- Refresh creative with new angles
- Adjust target ROAS upward (allow more spend to learn)
- Improve landing page experience
- Test different product sets

### Issue: High Frequency

**Causes:**
- Insufficient creative volume
- Audience too narrow
- Budget too high for audience size
- No creative refresh cadence

**Fixes:**
- Add 5-10 new creative combinations immediately
- Expand existing customer budget cap
- Reduce daily budget by 20%
- Implement 2-week creative refresh schedule

### Issue: Stuck in Learning

**Causes:**
- <50 conversions per week
- Frequent campaign edits
- Budget constraints
- Too many campaigns splitting volume

**Fixes:**
- Consolidate campaigns (reduce from 5 to 2-3)
- Increase budget to 3x target CPA
- Pause changes for 7-14 days
- Consider optimizing for add-to-cart instead of purchase temporarily

### Issue: Low EMQ Score

**Causes:**
- Missing customer information parameters
- Improper PII hashing
- Pixel-only implementation (no CAPI)
- Event deduplication not working

**Fixes:**
- Implement CAPI with full customer data
- Use SHA-256 hashing for PII
- Add email, phone, first name, last name parameters
- Verify deduplication with matching event_id

## Audit Report Structure

### Executive Summary
- Overall health score (X/100)
- Campaign ROAS vs. target
- Top 3 critical findings
- Immediate action items

### Detailed Analysis

**1. Tracking & Technical**
- Pixel + CAPI implementation status
- EMQ score and improvement opportunities
- Conversion tracking accuracy

**2. Campaign Structure**
- Budget allocation and pacing
- Learning phase status
- Existing customer budget cap configuration

**3. Creative Performance**
- Creative volume and diversity
- Top performers and underperformers
- Frequency analysis and fatigue indicators

**4. Performance Metrics**
- ROAS trend analysis
- CPA trend analysis
- Frequency trends
- CPM trends

### Action Plan

**Immediate (This Week):**
- Critical fixes (tracking issues, budget problems)

**Short-term (1-2 Weeks):**
- Creative refresh
- Budget optimization
- Audience expansion

**Long-term (1-3 Months):**
- Testing roadmap
- Scaling strategy
- Creative production pipeline

## Automation Opportunities

### Weekly Automated Checks
- Frequency monitoring (alert if >2.5)
- EMQ score tracking (alert if <6)
- Learning phase status (alert if stuck >14 days)
- Budget pacing (alert if under-spending >20%)
- ROAS anomaly detection (alert if drops >30%)

### Monthly Comprehensive Audit
- Full health score calculation
- Creative fatigue analysis
- Competitive benchmarking
- Strategic recommendations

## Integration with Other Skills

- **creative-analyzer:** Deep-dive into creative performance
- **audience-builder:** Optimize audience signals
- **hook-optimizer:** Improve video creative hooks
- **ad-copy:** Refine ad copy messaging

For detailed API documentation, see references/meta-marketing-api.md
For audit report templates, see references/asc-audit-templates.md
