---
name: ux-landing-page
description: Use this skill whenever the user mentions landing page, marketing page, conversion page, hero section, pricing page, CTA, call-to-action, social proof, testimonials, signup form, above the fold, conversion rate, lead generation, or any page whose primary goal is converting visitors. Also use when reviewing or building any customer-facing marketing page, product page, or campaign page — even if the user doesn't explicitly say "landing page". If the page has a signup button or pricing table, this skill applies.
---

# Landing Page UX and Conversion Optimization

This skill provides a complete framework for designing, evaluating, and optimizing landing pages for maximum conversion. It covers the full anatomy of a high-converting landing page, from hero section through final CTA, and integrates conversion rate optimization (CRO) research with UX best practices.

Apply these principles to any page whose primary purpose is converting visitors into leads, trial users, or customers -- including marketing pages, product pages, pricing pages, and campaign-specific landing pages.

---

## Optimal Section Flow

Structure every landing page in this sequence. Each section builds psychological momentum toward conversion:

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | **Hero** | Answer three questions in three seconds: What is this? Why should I care? What do I do next? |
| 2 | **Logo Bar / Social Proof Teaser** | Establish credibility immediately with recognizable customer logos or a single compelling metric |
| 3 | **Problem Statement** | Agitate the pain the visitor experiences; demonstrate understanding of their situation |
| 4 | **Solution Overview** | Present the product as the answer to the stated problem; connect pain to relief |
| 5 | **Key Features (3-6)** | Benefit-first feature blocks with visual evidence (screenshots, GIFs, short videos) |
| 6 | **Social Proof (Detailed)** | Testimonials with names, photos, titles, and quantified results; case study links |
| 7 | **Pricing** | 2-3 plans with highlighted recommendation, annual/monthly toggle, CTA per plan |
| 8 | **FAQ** | Address top 5-8 objections: cancellation, security, support, data ownership |
| 9 | **Final CTA** | Repeat the primary call-to-action with urgency framing and trust signals |

> Detailed psychological justification for each section, above-the-fold optimization rules, page speed impact, and mobile-first considerations: see `references/section-flow.md`

---

## Hero Section Formula

Apply the **3-in-3 Rule**: answer three questions in three seconds.

1. **Headline** (6-12 words): Lead with the primary benefit, not the feature. Address the visitor's pain point directly. "Manage all your projects in one place" outperforms "AI-Powered Project Management Platform."
2. **Subheadline** (1-2 sentences): Expand on the headline with specifics. Include a quantifiable claim where possible.
3. **Single Primary CTA**: One prominent button with action-oriented, first-person text. "Start my free trial" outperforms "Submit" by up to 90%.
4. **Visual**: Product screenshot, demo video, or illustration that reinforces the value proposition. Never use generic stock photos.
5. **Social Proof Teaser**: Logo bar of 4-6 recognizable customers or a single stat ("10,000+ teams trust us") near the CTA.

Ensure the entire hero section is visible without scrolling on a 1280x800 viewport. Largest Contentful Paint must be under 2.5 seconds.

---

## CTA Design Formula

Apply these rules to every call-to-action on the page:

**Placement**: Place the primary CTA above the fold. Repeat it at logical intervals -- after features, after social proof, and in the footer. Long-scroll pages need a minimum of 2-3 CTA instances.

**Visual Prominence**: The CTA must be the most visually prominent element in its section. Minimum button size of 44x44px (WCAG touch target). Use high contrast against the background (minimum 3:1 ratio).

**Copy Formula**: Verb + Value + Qualifier. Examples:
- "Start my free trial" (first-person phrasing outperforms second-person by 90%)
- "Get started free -- no credit card required"
- "Download the report"

**Friction Reduction**: Keep initial conversion forms to 3 fields or fewer. Each additional field reduces conversion by approximately 7-10%. Name + Email is often sufficient for first touch.

**Secondary CTA**: Offer a lower-commitment alternative ("Watch a 2-minute demo", "See pricing") with visually subordinate styling (outline or ghost button).

> Complete CTA patterns, social proof placement, pricing table design, and trust signal specifications: see `references/conversion-patterns.md`

---

## Social Proof Placement

Social proof is the most powerful trust-building mechanism on a landing page. Place it strategically to reduce perceived risk at each decision point.

**Logo Bar** (immediately below hero): Display 4-6 recognizable customer logos with a qualifier: "Trusted by [Company], [Company], and 500+ teams." Position within the first 2 viewport heights. Use grayscale logos for visual consistency.

**Testimonials** (after feature sections, before pricing): Include name, headshot photo, job title, and company name as minimum attribution. Prioritize specific, quantified results -- "Reduced onboarding time by 40%" outperforms "Great product!" Include 2-4 testimonials per page, varying roles and company sizes.

**Case Studies**: Link to detailed case study pages mid-page with a brief summary: "[Company] reduced churn by 35% in 6 months. Read the case study."

**Third-Party Badges**: G2 Leader, Capterra Top Rated, SOC 2, GDPR compliance. Link badges to actual review profiles. Place near the footer CTA and adjacent to pricing tables.

**Numbers**: Display real, verifiable aggregate metrics -- "10,000+ teams", "99.9% uptime", "4.8/5 on G2." Never inflate or fabricate statistics. Personalized social proof ("Companies like yours use...") converts 202% better than generic CTAs.

---

## Pricing Table Quick Reference

Apply Hick's Law to pricing: limit to 2-3 plans maximum. Three plans create natural anchoring (low, recommended, high). Four or more causes decision fatigue.

**Recommended Plan**: Highlight the middle tier with visual emphasis -- a "Most Popular" badge, different background color, larger card, or distinct border. The recommended plan's CTA should be the most visually prominent.

**Annual/Monthly Toggle**: Default to annual billing (lower per-month price). Show savings explicitly: "Save 20%" or "$240/year (save $48)."

**Plan Card Anatomy**: Each card needs a plan name indicating target audience ("Starter", "Team", "Enterprise"), the price in large type, a one-sentence tagline, 5-8 key features with checkmarks, a CTA button, and trust text ("14-day free trial", "Cancel anytime").

**Show Real Prices**: Display actual pricing, not "Contact us" (unless truly enterprise). Visible pricing builds trust and enables self-service conversion. Place a FAQ section immediately below pricing to address common objections: cancellation policy, what counts as a user, upgrade and downgrade terms.

---

## Form Optimization

Forms are the conversion bottleneck. Minimize fields and friction at every opportunity.

- Forms with 3 fields see conversion rates around 25%; 6+ fields drop to approximately 15%
- Reducing form fields from 11 to 4 increased conversions by 120% (HubSpot)
- Single-column form layouts improve completion rates by 15.4% over multi-column
- Multi-step forms can increase conversions by up to 300% compared to long single-page forms
- Inline validation reduces form errors by 22% compared to post-submission validation
- Use appropriate input types (`type="email"`, `type="tel"`) for mobile keyboard optimization
- Place trust signals adjacent to form fields: "We never share your email" below the email input

---

## Key CRO Metrics and Benchmarks

Reference these numbers when evaluating and prioritizing landing page improvements:

| Metric | Value | Source |
|--------|-------|--------|
| CTA above fold vs. below fold | +304% conversion | CRO research aggregate |
| Personalized vs. generic CTA | +202% conversion | HubSpot |
| Whitespace surrounding CTA | +232% conversion | CRO research |
| First-person CTA phrasing | +90% vs. second-person | A/B testing studies |
| Form: 3 fields vs. 6+ fields | 25% vs. 15% conversion rate | Form optimization studies |
| Reducing form fields (11 to 4) | +120% conversions | HubSpot |
| Single-column vs. multi-column form | +15.4% completion rate | UX research |
| Page load 1s vs. 5s | 3x more conversions | Google/performance studies |
| Each extra second of load time | -7% conversions | Performance research |
| Average SaaS landing page signup | 2-5% | Industry benchmark |
| Top-performing SaaS signup | >11% | Industry benchmark |
| Mobile-friendly button sizing | +90% clicks | CRO research |
| Video CTA vs. static CTA | +380% clicks | CRO research |

---

## Copywriting for Conversion (Quick Reference)

Apply these headline formulas when writing landing page copy:

**PAS (Problem-Agitation-Solution)**
1. State the problem the visitor faces
2. Agitate the emotional cost of not solving it
3. Present the product as the solution

**AIDA (Attention-Interest-Desire-Action)**
1. Grab attention with a bold claim or question
2. Build interest with specifics and evidence
3. Create desire through benefits and social proof
4. Drive action with a clear, compelling CTA

**4U Formula for Headlines**
- **Useful**: Does it promise a clear benefit?
- **Urgent**: Is there a reason to act now?
- **Unique**: Does it differentiate from alternatives?
- **Ultra-specific**: Does it include concrete details (numbers, timeframes)?

**Benefit vs. Feature Rule**: Always lead with the outcome ("Save 10 hours per week"), then explain the enabling feature ("with automated reporting"). Features tell; benefits sell.

> Full copywriting reference with value proposition frameworks, microcopy patterns, button label formulas, and error message guidelines: see `references/copywriting-ux.md`

---

## Landing Page Anti-Patterns

Flag these issues as high-severity problems in any audit:

- **Competing CTAs**: Multiple calls-to-action with equal visual weight that split visitor attention
- **Navigation leakage**: Keeping full site navigation on a landing page, allowing visitors to drift away from the conversion goal
- **Jargon-heavy headline**: Technical or vague headlines ("Transform Your Business", "Next-Gen Platform") that fail the 3-in-3 test
- **No CTA above the fold**: Forcing visitors to scroll before encountering the primary conversion point
- **Fake urgency**: Manufactured countdown timers or fabricated scarcity claims that erode trust
- **Slow loading**: Hero images or videos that push LCP beyond 2.5 seconds
- **Text walls**: Dense paragraphs without visual breaks, subheadings, or bullet points
- **Testimonials without attribution**: Quotes missing name, photo, title, and company feel fabricated
- **Hidden pricing**: "Contact us for pricing" on pages targeting self-service conversion
- **Desktop-only optimization**: Ignoring that 58%+ of traffic arrives on mobile devices

---

## Core Web Vitals Targets

Enforce these performance thresholds on every landing page:

| Metric | Target | Impact |
|--------|--------|--------|
| Largest Contentful Paint (LCP) | < 2.5 seconds | Primary loading metric; directly affects bounce rate |
| Cumulative Layout Shift (CLS) | < 0.1 | Visual stability; layout shifts erode trust |
| Interaction to Next Paint (INP) | < 200ms | Responsiveness; sluggish interactions reduce conversion |

Optimize images (use WebP/AVIF, lazy-load below-fold images), minimize render-blocking JavaScript, and serve critical CSS inline. Every 1-second delay in load time reduces conversions by approximately 7%.

---

## Reference Files

For detailed, audit-ready content on each topic, consult:

| File | Contents |
|------|----------|
| `references/conversion-patterns.md` | Hero section anatomy, CTA specifications, social proof patterns, pricing table design, and trust signal placement with checkable audit items |
| `references/section-flow.md` | Optimal section ordering with psychological justification, above-the-fold rules, page speed impact, Core Web Vitals targets, and mobile-first considerations |
| `references/copywriting-ux.md` | Headline formulas (PAS, AIDA, 4U), value proposition frameworks, benefit-vs-feature writing, microcopy patterns, CTA copy formulas, and form label guidelines |
