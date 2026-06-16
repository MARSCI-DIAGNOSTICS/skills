# Conversion Patterns -- Complete Reference

> Comprehensive guide to high-converting landing page components: hero sections, CTA design, social proof, pricing tables, and trust signals. All patterns include specific measurements, research-backed rationale, and checkable audit items.

---

## 1. Hero Section Anatomy

The hero section is the single highest-impact area of any landing page. Apply the **3-in-3 Rule**: answer three questions within three seconds of page load.

### Three Questions Every Hero Must Answer

1. **What is this?** -- The headline must immediately communicate what the product or service does.
2. **Why should I care?** -- The subheadline must connect the product to the visitor's pain or desired outcome.
3. **What should I do next?** -- A single, prominent CTA button must make the next step unmistakable.

### Hero Section Components

#### Headline
- Limit to 6-12 words
- Lead with the primary user benefit, not the product feature
- Address the visitor's pain point directly
- Avoid vague business jargon ("Transform Your Business", "Next-Gen Solutions", "Empower Your Team")
- Good: "Manage all your projects in one place"
- Bad: "AI-Powered Project Management Platform"
- Test: read the headline to someone unfamiliar with the product; if they cannot explain what it does, rewrite it

#### Subheadline
- Limit to 1-2 sentences (15-30 words)
- Expand on the headline with specifics
- Include a quantifiable claim where possible ("Used by 10,000+ teams", "Save 10 hours per week")
- Bridge the gap between the headline benefit and the CTA action

#### Primary Visual
- Use a product screenshot, short demo video (under 60 seconds), or custom illustration
- The visual must reinforce the value proposition, not decorate the page
- Never use generic stock photography (people shaking hands, abstract graphics)
- Product screenshots should show the actual UI in a realistic usage context
- If using video, provide a poster image so the hero is complete before the video loads
- Auto-playing video must be muted by default

#### Background
- Maintain high contrast between the headline text and background
- Avoid busy background images that compete with headline readability
- If using a background image, apply a gradient or color overlay to ensure text legibility
- Test headline readability at multiple viewport widths

### Hero Section Audit Checklist

- [ ] Headline is 6-12 words and communicates a clear user benefit
- [ ] Subheadline expands on the headline with specifics (15-30 words)
- [ ] Exactly one primary CTA button is present in the hero
- [ ] CTA text is action-oriented and starts with a verb
- [ ] Hero section is fully visible without scrolling on a 1280x800 viewport
- [ ] Visual element (screenshot, video, illustration) relates directly to the product
- [ ] Largest Contentful Paint (LCP) for the hero is under 2.5 seconds
- [ ] Headline passes the "stranger test" -- someone unfamiliar can explain what the product does
- [ ] No generic stock photography is used
- [ ] Background provides sufficient contrast for text readability (minimum 4.5:1 for body text)

---

## 2. CTA Placement and Design

The call-to-action is the conversion mechanism. Every design decision in its vicinity should reduce friction and increase visibility.

### Placement Rules

- **Above the fold (mandatory)**: The primary CTA must be visible without scrolling on standard viewports (1280x800 desktop, 375x812 mobile)
- **Repeat at logical intervals**: Place CTAs after key persuasion blocks -- after the feature section, after social proof, and in the page footer
- **Long-scroll pages**: Include a minimum of 3 CTA instances distributed throughout the page
- **Proximity to value statements**: Position CTAs immediately after persuasive content (testimonials, feature benefits, pricing comparison)
- **CTAs above the fold outperform below-fold CTAs by 304%**

### Visual Design Specifications

| Property | Minimum Requirement | Recommended |
|----------|-------------------|-------------|
| Button height | 44px (WCAG touch target) | 48-56px for primary CTA |
| Button width | Content-dependent | Minimum 200px for primary, or full-width on mobile |
| Contrast ratio (button vs. background) | 3:1 (WCAG non-text) | 4.5:1 or higher |
| Text contrast (button label vs. button fill) | 4.5:1 (WCAG AA normal text) | 7:1 for maximum readability |
| Border radius | 4-8px (standard), or brand-consistent | Match design system tokens |
| Padding | 12px vertical, 24px horizontal minimum | 16px vertical, 32px horizontal |
| Font weight | Semibold (600) minimum | Bold (700) for maximum prominence |

### CTA Copy Formulas

Apply the **Verb + Value + Qualifier** pattern:

| Formula Component | Example |
|------------------|---------|
| Verb + Value | "Start free trial" |
| Verb + Value + Qualifier | "Start my free trial -- no credit card" |
| First-person phrasing | "Start my free trial" (+90% vs. "Start your free trial") |
| Outcome-oriented | "Get my custom report" |
| Specificity | "Start your 14-day free trial" |

Avoid generic labels: "Submit", "Click here", "Learn more", "Sign up", "Get started"

### Secondary CTA
- Offer a lower-commitment alternative: "Watch a 2-minute demo", "See pricing", "Read the case study"
- Style as outline or ghost button (no fill, border only) to create clear visual hierarchy
- Position adjacent to or below the primary CTA
- Never make the secondary CTA visually equal to the primary

### Friction Reduction Near CTAs

- Display "No credit card required" directly below the CTA if applicable
- Show security badges and privacy assurance text ("256-bit SSL encrypted")
- Include a micro-testimonial quote near the CTA ("Saved us 40 hours per month -- Sarah, VP Ops")
- Minimize form fields: Name + Email for initial conversion (each additional field reduces conversion by approximately 7-10%)
- Surround the CTA with whitespace -- uncluttered CTAs see 232% higher conversion rates

### CTA Audit Checklist

- [ ] Primary CTA is visible above the fold on desktop (1280x800) and mobile (375x812)
- [ ] CTA button meets minimum size of 44x44px (48px+ recommended)
- [ ] CTA button contrast ratio against background is at least 3:1
- [ ] CTA label text contrast against button fill is at least 4.5:1
- [ ] CTA text uses the Verb + Value pattern and starts with a verb
- [ ] CTA text uses first-person phrasing where appropriate ("Start my..." not "Start your...")
- [ ] CTA is repeated at least 2-3 times on long-scroll pages
- [ ] Secondary CTA is visually subordinate (outline or ghost button)
- [ ] Friction-reducing text appears near the CTA ("No credit card required", trust badges)
- [ ] Form fields adjacent to CTA are limited to 3 or fewer
- [ ] CTA area has sufficient whitespace -- no competing elements crowd the button
- [ ] CTA is functional on mobile with adequate touch target spacing (8px minimum between targets)

---

## 3. Social Proof Patterns

Social proof leverages the psychological principle that people follow the actions of others when uncertain. Place social proof strategically to build credibility at decision points.

### Types of Social Proof (Ranked by Impact)

#### Logo Bar
- Display 4-6 recognizable customer logos in a horizontal row
- Accompany with a qualifier: "Trusted by [Company], [Company], and 500+ teams"
- **Placement**: Immediately below the hero section (within the first 2 viewport heights)
- Use grayscale logos for visual consistency; colorize on hover if desired
- Ensure logos are legible at small sizes (minimum 60px wide on mobile)

#### Testimonials
- Include name, headshot photo, job title, and company name (minimum viable attribution)
- Prioritize specific, quantified results: "Reduced onboarding time by 40%" outperforms "Great product!"
- Include 2-4 testimonials per landing page, distributed across sections
- Vary testimonial sources: mix roles (CEO, developer, manager), company sizes, and industries
- Consider video testimonials for high-value pages (30-60 seconds each)
- **Placement**: After the feature sections and before pricing

#### Case Studies
- Link to detailed case study pages with measurable outcomes
- Format the link as a brief summary: "[Company] reduced churn by 35% in 6 months. Read the case study."
- Include 1-2 case study links mid-page
- **Placement**: Between social proof and pricing, or alongside relevant feature sections

#### Aggregate Numbers
- Display real, verifiable numbers: "10,000+ teams", "99.9% uptime", "4.8/5 on G2 (500+ reviews)"
- Never inflate or fabricate statistics -- users are increasingly sophisticated at detecting inauthenticity
- **Placement**: Hero area, logo bar, or dedicated metrics strip

#### Third-Party Badges
- G2 Leader, Capterra Top Rated, Product Hunt badge, SOC 2 compliance, GDPR compliance
- Link badges to actual review profiles or certification pages
- **Placement**: Near the footer CTA and adjacent to pricing tables

### Social Proof Audit Checklist

- [ ] Logo bar is present within the first 2 viewport heights
- [ ] Logo bar displays 4-6 recognizable customer logos
- [ ] Logo bar includes a qualifying statement ("Trusted by..." or "Used by...")
- [ ] Testimonials include name, photo, job title, and company (minimum)
- [ ] At least one testimonial includes a specific, quantified result
- [ ] Testimonial sources are diverse (different roles, company sizes, industries)
- [ ] Third-party review badges (G2, Capterra, etc.) link to actual review profiles
- [ ] Social proof appears before the pricing section
- [ ] Aggregate numbers are real and verifiable
- [ ] No fabricated or misleading social proof is present
- [ ] Testimonials do not use generic phrases without attribution

---

## 4. Pricing Table Design

Pricing tables are the final decision gate before conversion. Apply choice architecture principles to guide visitors toward the recommended plan.

### Structure Rules

- **2-3 plans maximum**: Three plans create natural anchoring (low, recommended, high). Two is acceptable. Four or more causes decision fatigue (Hick's Law).
- **Highlight the recommended plan**: Use visual emphasis -- a "Most Popular" or "Recommended" badge, a different background color, a larger card, or a distinct border. This should be the middle tier.
- **Annual/monthly toggle**: Default to annual billing (lower per-month price). Show savings explicitly: "Save 20%" or "$240/year (save $48)."
- **Show real prices**: Display actual pricing, not "Contact us" (unless truly enterprise-scale). Visible pricing builds trust and enables self-service conversion.

### Plan Card Anatomy

Each pricing plan card must include:
1. **Plan name**: Indicate the target audience ("Starter", "Team", "Enterprise" -- not "Bronze", "Silver", "Gold")
2. **Price**: Large, prominent monthly price with annual alternative shown
3. **Tagline**: One sentence describing who this plan is for ("For small teams getting started")
4. **Feature list**: 5-8 key features with checkmarks; highlight differentiating features between tiers
5. **CTA button**: Action-oriented text on every plan card ("Start free trial", "Contact sales")
6. **Trust signals**: "14-day free trial", "No credit card required", "Cancel anytime"

### Feature Comparison Matrix

- Show a comparison table below the plan cards for detailed feature-by-feature comparison
- Use checkmarks and X marks for binary features
- Use text values for graduated features ("5 users", "Unlimited users")
- Highlight differentiating features with a background color or bold text
- Limit visible rows to 8-12; collapse additional features behind "Show all features"
- Freeze the plan header row for scrollable comparison tables

### Pricing Section Audit Checklist

- [ ] 2-3 pricing tiers are displayed (4 maximum)
- [ ] One plan is visually highlighted as recommended ("Most Popular" badge)
- [ ] Monthly/annual toggle is present with savings shown explicitly
- [ ] Every plan card has its own CTA button
- [ ] Recommended plan's CTA is the most visually prominent
- [ ] Feature comparison shows at least 5 differentiating features
- [ ] Plan names indicate target audience, not abstract tiers
- [ ] Actual prices are shown (not "Contact us" for self-service plans)
- [ ] Trust signals appear near pricing ("Free trial", "Cancel anytime", "Money-back guarantee")
- [ ] FAQ section addresses common pricing objections (located below or adjacent to pricing)
- [ ] Annual default view shows per-month price to enable comparison

---

## 5. Trust Signals

Trust signals reduce perceived risk at conversion points. Place them where visitors experience the most anxiety -- near forms, CTAs, and payment inputs.

### Trust Signal Categories

#### Security Indicators
- SSL/TLS badge ("256-bit SSL Encrypted")
- Payment processor logos (Stripe, PayPal, Visa, Mastercard)
- SOC 2, ISO 27001, or GDPR compliance badges
- "Your data is encrypted and never shared" reassurance text

#### Risk Reversal
- "14-day free trial -- no credit card required"
- "30-day money-back guarantee"
- "Cancel anytime -- no long-term contracts"
- "Free plan available -- upgrade when you're ready"

#### Authority Signals
- "Featured in [Publication]" with logos
- Industry certifications and awards
- Partnership badges (AWS, Google Cloud, Microsoft)
- Team credentials ("Built by engineers from Google, Stripe, and Meta")

#### Social Validation
- Real-time activity indicators ("523 teams signed up this month")
- Review aggregates ("4.8/5 from 1,200+ reviews on G2")
- Customer count ("Trusted by 10,000+ companies worldwide")

### Placement Guidelines

| Trust Signal Type | Primary Placement | Secondary Placement |
|------------------|------------------|---------------------|
| Security badges | Adjacent to payment forms | Footer |
| Risk reversal text | Below primary CTA | Pricing section |
| Authority badges | Below hero logo bar | About section |
| Social validation | Hero section, near CTA | Pricing section |
| Review badges | Adjacent to testimonials | Footer |

### Trust Signal Audit Checklist

- [ ] Security indicators are visible near all form inputs and payment areas
- [ ] At least one risk-reversal statement appears near the primary CTA
- [ ] Third-party badges link to verifiable external sources
- [ ] Trust signals are placed near conversion friction points, not buried in the footer
- [ ] No fabricated or unverifiable trust claims are present
- [ ] Payment security logos are displayed on any page collecting payment information
- [ ] Privacy assurance text is present near email capture forms
- [ ] "Cancel anytime" or equivalent text is present near pricing CTAs
