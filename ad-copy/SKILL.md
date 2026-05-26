---
name: ad-copy
description: Write high-performing ad copy for Meta advertising (Facebook, Instagram) optimized for mobile engagement, scroll-stopping hooks, and conversion-focused messaging. Use when creating ads, improving CTR, writing copy for different funnel stages, optimizing character limits, testing CTA variations, or adapting messaging across placements. Covers copywriting frameworks, character limits, performance benchmarks, and API integration.
---

# Meta Ad Copy Optimization

Write compelling ad copy for Meta platforms (Facebook, Instagram, Messenger) with platform-specific optimization for mobile-first audiences and diverse placements.

## Platform Context

**Mobile dominance:** Mobile users spend only 1.7 seconds on content (vs. 2.5s desktop)
**Immediate engagement critical:** First 3 seconds determine 90% of engagement
**Placement diversity:** Feed, Stories, Reels, Messenger, Audience Network each require adaptations

## Character Limits by Placement

| Element | Recommended | Truncation Point | Notes |
|---------|-------------|------------------|-------|
| Primary Text | 125 characters | ~115 chars mobile | Front-load value prop |
| Headline | 40 characters | Varies by placement | Short and impactful |
| Link Description | 30 characters | Desktop only | Often not shown |
| Carousel Headline | 27 characters | Per card | Very limited |

**Critical:** Front-load value proposition in first 30 characters to ensure visibility before "See More" truncation.

## Copywriting Frameworks

### Framework 1: PAS (Problem-Agitate-Solution)

**Structure:**
```
[Pain point question]?
We get it. [Agitate the problem - make them feel it].
That's why we created [product]—[solution/benefit].
[Social proof if space allows]. [CTA]
```

**Example:**
```
Tired of skincare that doesn't deliver?
We hear you. You've tried expensive creams that promise miracles but leave you disappointed.
That's why we created CleanGlow—dermatologist-formulated for real results.
Join 50K+ happy customers. Try it risk-free today. →
```

### Framework 2: AIDA (Attention-Interest-Desire-Action)

**Structure:**
```
[Attention-grabbing hook - bold statement or question]
Here's the thing: [Interest-building fact or story]
Imagine [Desire-creating vision of transformation]
[CTA with urgency]
```

**Example:**
```
Your competitors are stealing your customers. 📉
Here's the thing: 73% of consumers compare prices before buying.
Imagine never losing a sale to price again with our AI-powered pricing tool.
Start your free trial—no credit card required. Limited spots available!
```

### Framework 3: BAB (Before-After-Bridge)

**Structure:**
```
Before: [Current pain state]
After: [Desired future state]
Bridge: [How your product gets them there]
[CTA]
```

**Example:**
```
Before: Spending 10+ hours/week on manual data entry
After: Automated workflows saving you 8 hours/week
The Bridge: FlowBot AI handles repetitive tasks automatically
Free up your time today. Get started →
```

### Framework 4: Feature-Benefit-Proof

**Structure:**
```
[Key feature]
What this means for you: [Benefit translation]
[Social proof/statistic]
[CTA]
```

**Example:**
```
24/7 customer support via AI + human backup
What this means: Never lose a customer to a unanswered question
92% customer satisfaction rating
Experience it yourself →
```

## Funnel-Specific Messaging

### TOF (Top of Funnel - Cold Audience)

**Objectives:** Awareness, education, curiosity
**Tone:** Helpful, educational, non-salesy
**Content:** Broader problem/solution, value-first approach

**Example:**
```
Did you know 68% of small businesses waste $2K+ monthly on inefficient software?
We created a free guide showing exactly where money leaks happen.
Download the Small Business Efficiency Audit [CTA]
```

### MOF (Middle of Funnel - Warm Audience)

**Objectives:** Consideration, trust-building, differentiation
**Tone:** Informative, benefit-focused
**Content:** Product benefits, case studies, how it works

**Example:**
```
"After switching to [Product], we cut software costs by 40% in just 2 months." - Sarah M., CFO
See how we helped 500+ businesses streamline operations.
Read the case study + get our optimization checklist →
```

### BOF (Bottom of Funnel - Hot Audience)

**Objectives:** Conversion, urgency, objection handling
**Tone:** Direct, persuasive, action-oriented
**Content:** Specific offers, guarantees, urgency/scarcity

**Example:**
```
You're 1 click away from 40% lower operating costs.
Start your 14-day free trial—no credit card required.
💰 100% money-back guarantee
⏰ Special pricing ends Sunday
Get started now →
```

### Retargeting

**Objectives:** Re-engagement, addressing abandonment
**Tone:** Personal, friendly reminder
**Content:** Personalized to previous interaction

**Template:**
```
Hey, we noticed you were checking out [specific product]. 👀
Still on your mind? We saved it for you.
[Offer/discount]—but only for [time limit].
Complete your order →
```

## CTA Optimization

### High-Performing CTAs by Objective

**Lead Generation:**
- "Get Your Free [Resource]"
- "Download the Guide"
- "Start Free Trial"
- "Book a Demo"

**E-commerce:**
- "Shop Now"
- "Order Today & Save [X]%"
- "Add to Cart"
- "Get Yours Before They're Gone"

**Engagement:**
- "Learn More"
- "See How It Works"
- "Watch the Video"
- "Read the Story"

**App Install:**
- "Install Now"
- "Download Free"
- "Get the App"
- "Start Playing"

**CTA buttons increase conversion rates by 2.85x** compared to ads without them.

## Performance Benchmarks (2024-2025)

### Industry Averages

| Industry | CTR | CPC | CPL |
|----------|-----|-----|-----|
| Real Estate | 2.60% | $1.10 | $13.87 |
| Arts & Entertainment | 2.59% | $0.44 | $8.50 |
| Travel | 2.20% | $0.43 | — |
| Finance & Insurance | 0.88% | $1.05 | — |
| **All Industries** | **1.57%** | **$0.70-$0.77** | **$21.98** |

### Performance Indicators

**Strong performance:**
- CTR >2.0% (cold audience)
- CTR >3.5% (retargeting)
- CPC below industry average
- Engagement rate >2%

**Needs optimization:**
- CTR <0.8% (cold audience)
- CTR <2.0% (retargeting)
- High impressions, low clicks
- Comments indicating confusion

## Meta Marketing API Integration

### AdCreative Creation

```javascript
POST /{ad_account_id}/adcreatives

{
  "name": "Summer Sale Campaign - Ad 1",
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "link_data": {
      "image_hash": "IMAGE_HASH",
      "link": "https://example.com/summer-sale",
      "message": "Your primary text goes here (125 chars max recommended)",
      "name": "Headline goes here (40 chars max)",
      "description": "Link description (30 chars max)",
      "call_to_action": {
        "type": "SHOP_NOW"
      }
    }
  }
}
```

### Dynamic Creative Testing

Enable "Optimize Text Per Person" for automatic testing of multiple text variations:

```javascript
{
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "link_data": {
      "message": ["Primary text variant 1", "Primary text variant 2", "Primary text variant 3"],
      "name": ["Headline 1", "Headline 2", "Headline 3"],
      "description": ["Description 1", "Description 2"],
      "call_to_action": {"type": "SHOP_NOW"}
    }
  }
}
```

Meta's algorithm automatically tests combinations and serves best-performing variations to each user.

### CTA Types Available

Common call_to_action types:
- `SHOP_NOW` - E-commerce
- `LEARN_MORE` - Education/info
- `SIGN_UP` - Lead gen
- `DOWNLOAD` - App install
- `BOOK_NOW` - Services/events
- `GET_QUOTE` - B2B/services
- `CONTACT_US` - General inquiry
- `APPLY_NOW` - Applications

## Copy Testing Framework

### Phase 1: Hook Testing (3-5 variations)
- Test different angles of primary text opening
- Keep body and CTA consistent
- Identify scroll-stopping hooks

### Phase 2: Body Testing (2-3 variations)
- Use winning hook from Phase 1
- Test different benefit/feature emphasis
- Evaluate which messaging resonates

### Phase 3: CTA Testing (2-3 variations)
- Use winning hook + body
- Test CTA language variations
- Measure conversion intent

**Minimum test duration:** 7 days or 2,000+ impressions per variant
**Statistical significance:** Aim for p < 0.05

## Platform-Specific Adaptations

### Feed (Facebook & Instagram)
- Longer primary text acceptable (125 chars)
- Headline + description displayed
- Desktop users see more content

### Stories
- Minimal text (mobile vertical format)
- Bold, large text overlays work well
- Emojis enhance mobile experience
- Full vertical 9:16 aspect ratio

### Reels
- Native, authentic feel critical
- Hook must be instant (0-1 second)
- Sound can be on or off (plan for both)
- Text overlays essential

## Common Mistakes to Avoid

### 1. Burying the Lead
❌ Long setup before stating value proposition
✅ Lead with benefit in first 30 characters

### 2. Feature Dumping
❌ "5 modes, 3 speeds, 2 settings, LED display"
✅ "Gets your smoothie perfectly creamy in 30 seconds"

### 3. Generic CTAs
❌ "Click here" or "Learn more"
✅ "Get Your Free Skincare Guide" or "Start Saving Today"

### 4. Forgetting Mobile
❌ Writing for desktop experience
✅ Test on mobile device, optimize for thumb-scrollers

### 5. No Social Proof
❌ Making claims without backing them up
✅ Include statistics, testimonials, trust indicators

### 6. Unclear Value Proposition
❌ "We're the best solution for your needs"
✅ "Save 10 hours per week on data entry with AI automation"

## Best Practices Checklist

- [ ] Value proposition in first 30 characters
- [ ] Clear benefit statement (not just features)
- [ ] Social proof or credibility indicator
- [ ] Specific, actionable CTA
- [ ] Mobile-optimized character count
- [ ] Emoji usage strategic (1-2 max, when appropriate)
- [ ] Urgency/scarcity element (if applicable)
- [ ] Tested on actual mobile device
- [ ] Aligned with landing page message
- [ ] Appropriate for funnel stage

## Integration with Other Skills

- **hook-optimizer:** Apply hook frameworks to primary text opening
- **creative-analyzer:** Pair strong copy with high-performing creative
- **audience-builder:** Tailor messaging to specific audience segments

For copywriting templates by industry, see references/copy-templates.md
For A/B testing frameworks, see references/testing-methodology.md
