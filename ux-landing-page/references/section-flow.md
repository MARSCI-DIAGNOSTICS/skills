# Section Flow and Page Architecture -- Complete Reference

> Comprehensive guide to landing page section ordering, above-the-fold optimization, page speed impact on conversion, Core Web Vitals targets, mobile-first considerations, and feature section design patterns. All recommendations include psychological justification and checkable audit items.

---

## 1. Optimal Section Ordering

Structure landing pages in the following sequence. Each section has a specific psychological role that builds momentum toward conversion. Changing the order weakens the persuasion chain.

### The Conversion Flow

#### Section 1: Hero
**Psychological Role**: Orientation and relevance confirmation.

Visitors decide within 3-5 seconds whether a page is relevant. The hero must pass the "3-in-3 test" -- answer What is this? Why should I care? What do I do next? -- in 3 seconds or less.

- Place the headline, subheadline, primary CTA, and supporting visual within the initial viewport
- The headline carries the heaviest weight; make it benefit-driven and jargon-free
- A single CTA prevents decision paralysis (Hick's Law)

#### Section 2: Logo Bar / Social Proof Teaser
**Psychological Role**: Credibility establishment through social validation.

Immediately after the hero, demonstrate that credible organizations already trust the product. This leverages the bandwagon effect and reduces perceived risk before the visitor invests further attention.

- Display 4-6 recognizable customer logos
- Add a qualifying statement: "Trusted by [Company], [Company], and 500+ teams"
- Position within the first 2 viewport heights
- Grayscale logos maintain visual consistency

#### Section 3: Problem Statement
**Psychological Role**: Empathy and pain amplification.

Before presenting the solution, articulate the problem the visitor faces. This creates emotional resonance and signals that the product was built with understanding of their specific situation. The Problem-Agitation-Solution (PAS) framework works here: state the problem, then amplify the emotional cost of leaving it unsolved.

- Use "you" language to address the visitor directly
- Describe the pain in the visitor's own words (drawn from customer research)
- Quantify the cost of the problem where possible ("Teams waste 15 hours per week on manual reporting")
- Limit to 2-4 short paragraphs or a set of 3-4 pain-point cards

#### Section 4: Solution Overview
**Psychological Role**: Relief and hope.

Transition from the problem to the product as the solution. Position the product as the bridge between the visitor's current frustration and their desired outcome. Maintain benefit-first framing.

- Lead with the outcome: "With [Product], your team reclaims 15 hours every week"
- Show the product in context: a screenshot or short video demonstrating the core workflow
- Keep it concise: 1-2 sentences of copy plus a visual
- Include a secondary CTA if the solution section runs long

#### Section 5: Key Features (3-6 Feature Blocks)
**Psychological Role**: Evidence and justification.

After establishing the emotional connection (problem + solution), provide logical evidence that the product delivers. Features serve as proof points for the benefits promised earlier. Lead each feature block with the outcome, then explain the enabling feature.

- Use alternating left-right layout for visual rhythm and engagement
- Structure each block consistently: icon or visual + benefit headline + 2-3 sentence description
- Limit to 3-6 primary features on the landing page; link to a full features page for completeness
- Show the actual product UI (screenshots, GIFs) rather than abstract illustrations

#### Section 6: Social Proof (Detailed)
**Psychological Role**: Risk reduction through peer validation.

After features have built the logical case, social proof provides third-party validation. Testimonials from people similar to the visitor carry the most weight (in-group bias). Specific, quantified results outperform generic praise.

- Include 2-4 testimonials with full attribution (name, photo, title, company)
- Prioritize quantified outcomes: "Reduced churn by 35% in 6 months"
- Vary the sources: different roles, company sizes, and industries
- Link to detailed case studies for visitors who need deeper validation
- Include third-party review badges (G2, Capterra) if available

#### Section 7: Pricing
**Psychological Role**: Commitment decision.

Pricing comes after full persuasion -- the visitor understands the problem, the solution, the features, and the social proof. Placing pricing too early (before value is established) increases sticker shock. Placing it too late risks frustrating visitors who want to self-qualify.

- Display 2-3 plans with the recommended plan highlighted
- Default to annual billing to show the lower per-month price
- Include a CTA button on every plan card
- Add "No credit card required", "Cancel anytime", or "30-day money-back guarantee"

#### Section 8: FAQ
**Psychological Role**: Objection handling.

Address the remaining doubts that prevent conversion. The FAQ section acts as a silent salesperson, resolving concerns the visitor has not articulated. Anticipate objections from customer research and support ticket analysis.

- Address 5-8 top objections: pricing, cancellation, security, data ownership, onboarding effort, integration compatibility, support availability
- Use an accordion (expand/collapse) pattern to keep the section scannable
- Write answers that resolve the objection and reinforce confidence

#### Section 9: Final CTA
**Psychological Role**: Decision closure.

The final CTA captures visitors who have scrolled the entire page and are now fully informed. Repeat the primary call-to-action with a brief summary of the value proposition and any urgency framing (genuine limited offers, not fake countdowns).

- Include the same CTA button style and text as the hero
- Add a brief reassurance: "Join 10,000+ teams. Start your free trial today."
- Place trust signals (security badge, risk reversal) adjacent to the CTA
- This section should be visually distinct (contrasting background) to signal a clear endpoint

### Section Flow Audit Checklist

- [ ] Page follows the persuasion sequence: Hero, Social Proof Teaser, Problem, Solution, Features, Testimonials, Pricing, FAQ, Final CTA
- [ ] Each section has a single, clear purpose
- [ ] No section is missing from the flow (gaps break the persuasion chain)
- [ ] Problem section appears before Solution section (empathy before pitch)
- [ ] Social proof appears before Pricing (credibility before commitment)
- [ ] FAQ section addresses at least 5 common objections
- [ ] Final CTA section is visually distinct and includes trust signals
- [ ] Section transitions are logical and progressive (no jarring topic jumps)
- [ ] Primary CTA appears in at least 3 locations throughout the page (hero, mid-page, footer)

---

## 2. Above-the-Fold Optimization

The above-the-fold area is the most valuable real estate on any landing page. Optimize every pixel for clarity and conversion.

### Definition and Viewport Targets

"Above the fold" is the content visible without scrolling on the initial page load. Target these standard viewports:

| Device | Viewport | Priority |
|--------|----------|----------|
| Desktop (standard) | 1280x800 | Primary design target |
| Desktop (full HD) | 1920x1080 | Secondary |
| Mobile (iPhone) | 375x812 | Equal priority to desktop |
| Mobile (Android) | 390x844 | Test coverage |
| Tablet (iPad) | 768x1024 | Tertiary |

### Above-the-Fold Essentials

Include all of these elements within the initial viewport on both desktop and mobile:

1. **Headline**: Benefit-driven, 6-12 words
2. **Subheadline**: Supporting context, 1-2 sentences
3. **Primary CTA button**: Visually dominant, action-oriented text
4. **Supporting visual**: Product screenshot, illustration, or video poster frame
5. **Navigation**: Minimal -- strip down to logo + 1-2 links (pricing, login) to prevent leakage

### Single Goal per Page

Every landing page must have **one primary conversion goal**. Remove competing navigation, sidebar links, and distracting secondary content that leaks visitors away from the conversion funnel.

- Strip out full site navigation on campaign-specific landing pages
- If full navigation must remain (e.g., pricing page on main site), visually de-emphasize it
- Every link on the page should either lead toward the conversion goal or provide essential context (privacy policy, terms)
- Measure success with a single primary KPI: the conversion rate for the primary CTA

### Above-the-Fold Audit Checklist

- [ ] Headline is visible without scrolling on 1280x800 desktop viewport
- [ ] Headline is visible without scrolling on 375x812 mobile viewport
- [ ] Primary CTA button is visible without scrolling on both desktop and mobile
- [ ] Above-the-fold area contains no more than 1 primary CTA
- [ ] Navigation is minimal (no full site nav on campaign landing pages)
- [ ] No extraneous elements compete with the headline and CTA for attention
- [ ] Visual hierarchy guides the eye from headline to subheadline to CTA
- [ ] Page has a single primary conversion goal
- [ ] All above-the-fold elements render within 2.5 seconds (LCP target)

---

## 3. Page Speed and Performance Impact

Page speed is a direct conversion lever. Slow pages lose visitors before the content can persuade them.

### Speed-Conversion Relationship

| Load Time | Conversion Impact | Context |
|-----------|------------------|---------|
| Under 1 second | Baseline (optimal) | Top-performing pages |
| 1-2 seconds | Minimal impact | Acceptable for most pages |
| 2-3 seconds | ~7-14% conversion loss | Start of measurable decline |
| 3-5 seconds | ~21-28% conversion loss | Significant visitor abandonment |
| 5+ seconds | 3x fewer conversions vs. 1s | Critical performance failure |

**Key finding**: Pages loading in 1 second convert 3x more than pages loading in 5 seconds. Every additional second of load time reduces conversions by approximately 7%.

### Core Web Vitals Targets

Google's Core Web Vitals are the industry standard for measuring user experience performance. Meet these thresholds:

| Metric | Target (Good) | Needs Improvement | Poor |
|--------|--------------|-------------------|------|
| **Largest Contentful Paint (LCP)** | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **Cumulative Layout Shift (CLS)** | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **Interaction to Next Paint (INP)** | < 200ms | 200ms - 500ms | > 500ms |

### Optimization Techniques

#### Image Optimization
- Serve images in WebP or AVIF format (30-50% smaller than JPEG/PNG)
- Lazy-load all images below the fold (`loading="lazy"`)
- Set explicit width and height attributes on all images to prevent layout shift
- Use responsive images with `srcset` and `sizes` attributes
- Compress hero images to under 200KB where possible

#### JavaScript Optimization
- Defer non-critical JavaScript (`defer` or `async` attributes)
- Remove unused JavaScript (tree-shaking, code splitting)
- Avoid render-blocking scripts in the document head
- Lazy-load third-party scripts (analytics, chat widgets, social embeds)

#### CSS Optimization
- Inline critical CSS for above-the-fold content
- Defer non-critical CSS loading
- Remove unused CSS rules
- Minimize CSS file size through minification

#### Server and Network
- Use a CDN for static assets
- Enable HTTP/2 or HTTP/3
- Implement server-side caching
- Use preconnect for critical third-party origins (`<link rel="preconnect">`)

### Page Speed Audit Checklist

- [ ] Largest Contentful Paint (LCP) is under 2.5 seconds
- [ ] Cumulative Layout Shift (CLS) is under 0.1
- [ ] Interaction to Next Paint (INP) is under 200ms
- [ ] Hero image is optimized (WebP/AVIF, under 200KB, explicit dimensions)
- [ ] Below-fold images use lazy loading
- [ ] No render-blocking JavaScript in the document head
- [ ] Critical CSS is inlined for above-the-fold content
- [ ] Third-party scripts are lazy-loaded or deferred
- [ ] CDN is serving static assets
- [ ] All images have explicit width and height attributes (prevents CLS)
- [ ] Font files are preloaded or use `font-display: swap` to prevent FOIT

---

## 4. Mobile-First Considerations

With 58%+ of global web traffic on mobile devices and Google using mobile-first indexing exclusively, every landing page must be designed and optimized for mobile as the primary experience.

### Mobile Layout Principles

- **Design mobile first**: Start with the smallest viewport and progressively enhance for larger screens
- **Stack vertically**: Convert multi-column desktop layouts to single-column stacks on mobile
- **Prioritize content**: Not everything on the desktop page belongs on mobile; question every element's necessity
- **Thumb zone**: Place primary CTAs in the lower third of the screen where thumbs naturally reach
- **Full-width CTAs on mobile**: Expand primary CTA buttons to full viewport width (with padding) for easy tapping

### Mobile-Specific Patterns

| Pattern | Desktop | Mobile |
|---------|---------|--------|
| CTA size | 44px+ height, auto width | 48px+ height, full-width |
| Form layout | May use 2-column for short fields | Always single-column |
| Navigation | Minimal top bar (logo, login, CTA) | Hamburger for secondary nav, expose primary CTA |
| Feature sections | Side-by-side (image + text) | Stacked (image above text) |
| Pricing cards | Side-by-side (3 across) | Stacked or horizontal scroll |
| Testimonials | Grid or side-by-side | Single column or horizontal carousel |
| Logo bar | Horizontal row | 2 rows or horizontal scroll |
| FAQ | Full-width accordion | Full-width accordion (same) |

### Mobile Typography

- Body text minimum: **16px** (prevents iOS auto-zoom on input focus)
- Headline scaling: use a smaller type scale ratio on mobile (e.g., 1.2 Minor Third vs. 1.333 Perfect Fourth on desktop)
- Line length: 35-45 characters per line on mobile for optimal readability
- Use `clamp()` for fluid typography that scales between breakpoints

### Mobile Touch Targets

- Minimum tappable area: **44x44px** (WCAG), **48x48px** recommended (Material Design)
- Minimum spacing between adjacent targets: **8px**
- Never place small interactive elements (links, icons) adjacent without sufficient spacing
- Form inputs must be tall enough for comfortable tapping (minimum 44px height)

### Mobile Performance

- Mobile networks are slower and less reliable than desktop connections
- Target total page weight under **1.5MB** on mobile
- Serve appropriately sized images per breakpoint (do not serve desktop-sized images on mobile)
- Minimize the number of HTTP requests
- Consider a lighter hero treatment on mobile (static image instead of video)

### Mobile Audit Checklist

- [ ] Page is designed mobile-first (not desktop-first scaled down)
- [ ] All content is accessible and readable on 375px viewport width
- [ ] Primary CTA is full-width on mobile with minimum 48px height
- [ ] Body text is at least 16px on mobile
- [ ] No horizontal scrolling occurs at any mobile viewport width
- [ ] Touch targets are at least 44x44px with 8px minimum spacing
- [ ] Form inputs are single-column and at least 44px tall
- [ ] Images are responsive and appropriately sized for mobile
- [ ] Total page weight is under 1.5MB on mobile
- [ ] Primary CTA is reachable within the thumb zone (lower third of screen)
- [ ] Sticky elements (headers, banners) consume no more than 15% of mobile viewport height
- [ ] Video autoplays only on sufficient bandwidth or is replaced with a poster image on mobile

---

## 5. Feature Section Design Patterns

Feature sections provide the logical evidence that the product delivers on the hero's promise. Structure them for maximum persuasion and scannability.

### Benefit-First Structure

Lead every feature block with the user outcome, then explain the enabling feature:

**Pattern**: Outcome headline -> 2-3 sentence explanation -> Visual evidence

- Good: "Save 10 hours per week" (headline) + "Automated reporting pulls data from all your tools and generates dashboards instantly." (explanation) + screenshot of the reporting UI
- Bad: "Automated Reporting" (headline) + "Our AI-powered engine uses machine learning to aggregate data streams." (explanation)

### Layout Patterns

#### Alternating Left-Right
- Image on left, text on right for the first block; reverse for the second; alternate throughout
- Creates visual rhythm and maintains engagement through the section
- Use consistent alignment grids across all blocks

#### Icon Grid (3 or 6-up)
- Icon + heading + short description in a 3-column grid
- Best for presenting many features concisely (3, 6, or 9 features)
- Each card should be self-contained and consistent in content length

#### Bento Grid
- Modern marketing pattern using an asymmetric grid with varying card sizes
- Larger cards for hero features, smaller cards for secondary features
- Effective for visual variety and attention hierarchy

### Feature Section Audit Checklist

- [ ] Each feature block leads with a benefit-oriented headline (outcome, not feature name)
- [ ] Visual evidence (screenshot, GIF, video) accompanies each feature
- [ ] 3-6 primary features are highlighted on the landing page
- [ ] Layout pattern is consistent across all feature blocks
- [ ] Feature descriptions are concise (2-3 sentences maximum per block)
- [ ] Features link to detailed sub-pages or documentation where applicable
- [ ] Real product UI is shown rather than abstract illustrations (where possible)
- [ ] Feature order prioritizes the most compelling / most-requested features first
- [ ] A "See all features" link is present if more than 6 features exist
- [ ] Feature section includes at least one CTA (midway or at the end)
