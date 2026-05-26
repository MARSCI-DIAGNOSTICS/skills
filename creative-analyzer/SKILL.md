---
name: creative-analyzer
description: Analyze Meta ad creative performance including video metrics, visual elements, engagement patterns, and creative fatigue indicators. Use when evaluating creative effectiveness, identifying top performers, detecting fatigue signals, optimizing video content, planning creative refreshes, or generating creative performance reports. Covers hook rates, hold rates, fatigue detection, and refresh strategies.
---

# Meta Creative Analyzer

Systematic analysis framework for Meta ad creatives covering video performance, fatigue detection, refresh strategies, and optimization recommendations.

## Core Analysis Metrics

### Video Performance Metrics

**Hook Rate:** 3-second views ÷ impressions
- **Target:** 25-30%+
- **Good:** 20-25%
- **Poor:** <20%
- **Meaning:** Percentage of viewers who watch first 3 seconds

**Hold Rate:** ThruPlays ÷ impressions
- **Target:** 40-50%+
- **Good:** 30-40%
- **Poor:** <30%
- **Meaning:** Percentage who watch 15+ seconds or to completion

**ThruPlay Definition:** Video viewed for at least 15 seconds OR to completion (whichever comes first)

**Completion Rates by Quartile:**
- 25% watched: Strong hook
- 50% watched: Content engaging
- 75% watched: Highly engaging
- 95% watched: Exceptional content
- 100% watched: Story completed

### Engagement Metrics

**CTR (Click-Through Rate):**
- **Excellent:** >2.5%
- **Good:** 1.5-2.5%
- **Average:** 0.8-1.5%
- **Poor:** <0.8%

**Engagement Rate:** (Likes + Comments + Shares) ÷ Impressions
- **Excellent:** >2%
- **Good:** 1-2%
- **Average:** 0.5-1%
- **Poor:** <0.5%

**Comment Sentiment:**
- Positive indicators: Questions, praise, tags
- Negative indicators: Confusion, complaints, "why am I seeing this"

### Frequency Metrics

**Frequency = Impressions ÷ Reach**

| Campaign Type | Warning | Critical | Action |
|---------------|---------|----------|--------|
| Prospecting | 2.5 | 3.0 | Refresh creative immediately |
| Retargeting | 4.0 | 5.0 | Refresh creative, reduce budget |

**High frequency impacts:**
- Declining CTR
- Increasing CPC
- Creative fatigue
- Audience annoyance
- Negative brand perception

## Creative Fatigue Detection

### Primary Fatigue Signals

**1. Frequency Threshold Exceeded**
- Prospecting: >2.5-3.0
- Retargeting: >5.0

**2. CTR Decline**
- Week-over-week CTR drop of 15-20%+
- Sustained decline over 3+ days

**3. CPA Increase**
- Cost per acquisition doubles or more vs. historical average
- ROAS decline of 30%+ from peak

**4. Meta's Creative Fatigue Label**
- Meta shows "Creative Fatigue" when cost per result ≥2x past ads

### Secondary Fatigue Indicators

- Engagement rate decline
- Increased negative comments
- Higher frequency among converters
- Declining relevance score
- CPM increase without market changes

### Fatigue Timeline by Creative Type

**Static images:**
- Fast fatigue: 7-14 days
- Refresh: Every 2-3 weeks

**UGC video:**
- Medium fatigue: 14-21 days
- Refresh: Every 3-4 weeks

**High-production video:**
- Slower fatigue: 21-30 days
- Refresh: Every 4-6 weeks

**Carousel ads:**
- Variable: 14-28 days
- Refresh: Swap out 2-3 cards every 3 weeks

## Video Creative Best Practices

### Optimal Length by Placement

| Placement | Optimal Length | Aspect Ratio | Notes |
|-----------|----------------|--------------|-------|
| Facebook Feed | 15-30 seconds | 1:1 or 4:5 | Attention span limited |
| Instagram Feed | 15-60 seconds | 1:1 or 4:5 | Slightly longer acceptable |
| Stories | 15 seconds | 9:16 | Full vertical |
| Reels | 15-30 seconds | 9:16 | Authentic, native feel |

### Sound Considerations

**Critical stat:** 85% of Facebook videos watched with sound OFF

**Sound-off optimization:**
- Captions/subtitles essential (28% watch time increase)
- Visual storytelling must work alone
- Bold text overlays for key messages
- Strong visual hooks in first 3 seconds

**Sound-on enhancement:**
- Music enhances emotion
- Voiceover adds context
- Sound effects draw attention

### UGC (User-Generated Content) Performance

**Performance advantages:**
- Up to 300% higher CTR vs. polished content
- 92% of consumers trust UGC more than traditional ads
- Lower production costs
- Authentic feel increases trust

**UGC characteristics:**
- Raw, authentic (iPhone-quality acceptable)
- Real people using products
- Genuine testimonials
- Behind-the-scenes content

## Meta Marketing API Integration

### Video Metrics Retrieval

```
GET /{ad-id}/insights
?fields=impressions,video_thruplay_watched_actions,video_p25_watched_actions,
        video_p50_watched_actions,video_p75_watched_actions,
        video_p100_watched_actions,video_avg_time_watched_actions,
        frequency,ctr,cpc,conversions
&date_preset=last_30d
```

**Available breakdowns:**
- `publisher_platform` - Facebook vs. Instagram vs. Audience Network
- `platform_position` - Feed, Stories, Reels, etc.
- `device_platform` - Mobile vs. desktop
- `video_sound` - Sound on vs. sound off

### Creative Performance Comparison

```
GET /{adset-id}/ads
?fields=creative.name,creative.thumbnail_url,
        insights.date_preset(last_30d).fields(impressions,clicks,ctr,spend,
        conversions,cpm,frequency)
```

Identify:
- Top performers by ROAS
- Creatives with high frequency
- Declining performance trends
- Best-performing formats

### Ad Creative Asset Analysis

```
GET /{ad-id}
?fields=creative.asset_feed_spec.images,creative.asset_feed_spec.videos,
        creative.asset_feed_spec.bodies,creative.asset_feed_spec.titles,
        creative.effective_object_story_id
```

Extract which specific assets (images, videos, copy) are performing best.

## Creative Refresh Strategies

### When to Refresh

**Immediate refresh triggers:**
- Frequency >3.0 (prospecting) or >5.0 (retargeting)
- CTR decline >20% week-over-week
- CPA increase >25% from baseline
- Negative feedback scores increasing

**Proactive refresh schedule:**
- High-spend accounts: Every 2-3 weeks
- Medium-spend accounts: Every 3-4 weeks
- Low-spend accounts: Monthly

### Refresh Methodologies

**1. Variation on Winners**
- Keep winning hook
- Change angle or CTA
- New visuals, same message

**2. Complete Overhaul**
- New concept entirely
- Different pain points
- Fresh visual style

**3. Seasonal/Trend Adaptation**
- Incorporate current events
- Seasonal messaging
- Cultural moments

### Creative Testing Framework

**Phase 1: Isolation Testing (Week 1-2)**
- Test 3-5 creative variations
- Same audience, placement, budget
- Measure hook rate, hold rate, CTR, ROAS

**Phase 2: Winner Validation (Week 3)**
- Scale winning creative 2x budget
- Test against current best performers
- Confirm performance sustains at scale

**Phase 3: Optimization (Week 4+)**
- Create variations of winner
- Test different hooks with same body
- Iterative improvement

## Creative Performance Analysis Framework

### Weekly Analysis Checklist

- [ ] Identify creatives with frequency >2.5
- [ ] Flag creatives with CTR decline >15%
- [ ] Measure hook rates for all video ads
- [ ] Review hold rates and completion quartiles
- [ ] Analyze engagement rate trends
- [ ] Check for negative comment patterns
- [ ] Compare performance across placements

### Monthly Strategic Review

1. **Creative portfolio audit:**
   - How many active creatives?
   - Distribution across formats?
   - Age of each creative?
   
2. **Performance tier classification:**
   - Winners: Scale these
   - Contenders: Optimize these
   - Losers: Pause these

3. **Creative direction assessment:**
   - What themes are working?
   - What hooks are performing?
   - What angles have fatigued?

4. **Production pipeline evaluation:**
   - Do we have enough new content?
   - What's the refresh cadence?
   - Where are creative gaps?

## Format-Specific Best Practices

### Single Image

**Strengths:** Fast to produce, easy to test
**Weaknesses:** Faster fatigue, limited storytelling
**Best for:** Product-focused, simple messages, quick tests

**Optimization tips:**
- Eye-catching primary visual
- Benefit-driven overlay text (if any)
- Clear product visibility
- Brand consistency

### Video (Produced)

**Strengths:** Strong storytelling, emotional connection
**Weaknesses:** High production cost, longer creation time
**Best for:** Brand awareness, complex products, storytelling

**Optimization tips:**
- Hook in first 3 seconds
- Captions for sound-off viewing
- Clear CTA at end
- Multiple aspect ratios

### Video (UGC)

**Strengths:** Authenticity, trust, relatability
**Weaknesses:** Inconsistent quality, limited control
**Best for:** Social proof, testimonials, real results

**Optimization tips:**
- Keep it raw and authentic
- Feature real customers
- Natural testimonials
- Phone-quality acceptable

### Carousel

**Strengths:** Multiple products, storytelling sequence
**Weaknesses:** More complex to optimize, higher production
**Best for:** Product catalogs, step-by-step guides, comparisons

**Optimization tips:**
- Strongest image/card first
- Clear progression
- Variety in visuals
- Consistent branding

## Common Mistakes to Avoid

### 1. Ignoring Sound-Off Viewers
❌ Creating video that only works with sound
✅ Design for sound-off first, enhance with audio

### 2. No Hook Strategy
❌ Slow build-up in first 3 seconds
✅ Instant attention grab, pattern interrupt

### 3. Not Testing Enough Variations
❌ Running 1-2 creatives indefinitely
✅ Always have 10+ active creative variations

### 4. Waiting Too Long to Refresh
❌ Running creative until performance tanks
✅ Proactive 2-3 week refresh schedule

### 5. Killing Winners Too Early
❌ Pausing creative at first sign of decline
✅ Gradual phase-out while introducing new variations

## Creative Health Scoring

| Component | Weight | Scoring |
|-----------|--------|---------|
| Hook Rate | 20% | >30% (20), 25-30% (15), 20-25% (10), <20% (5) |
| Hold Rate | 20% | >45% (20), 35-45% (15), 25-35% (10), <25% (5) |
| CTR | 20% | >2% (20), 1.5-2% (15), 1-1.5% (10), <1% (5) |
| Frequency | 15% | <2.5 (15), 2.5-3 (10), >3 (5) |
| Engagement Rate | 15% | >2% (15), 1-2% (10), <1% (5) |
| Trend Direction | 10% | Improving (10), Stable (7), Declining (3) |

**Score interpretation:**
- 80-100: Excellent, scale this creative
- 60-79: Good, monitor and optimize
- 40-59: Warning, prepare replacement
- <40: Critical, replace immediately

## Integration with Other Skills

- **hook-optimizer:** Improve video hooks based on 3-second view analysis
- **ad-copy:** Optimize text elements based on performance
- **asc-auditor:** Monitor creative fatigue in ASC campaigns
- **audience-builder:** Test creative variations by audience segment

For creative testing templates, see references/creative-testing-framework.md
For video production guidelines, see references/video-best-practices.md
