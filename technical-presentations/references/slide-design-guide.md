# Slide Design Guide for Technical Presentations

Comprehensive guidance for creating effective slides that support your technical message without overwhelming your audience.

## Core Philosophy

**Slides are visual aids, not speaker notes.**

Your slides should:

- Reinforce key points visually
- Provide structure for both you and the audience
- Be scannable in seconds
- Support your narrative, not replace it

Your slides should NOT:

- Contain everything you plan to say
- Be read verbatim during the presentation
- Overwhelm with text or data
- Distract from your spoken message

## The Fundamental Rules

### Rule 1: One Idea Per Slide

Each slide should communicate a single concept. If you find yourself using "and" in the slide title, consider splitting it.

**Test:** Can someone grasp the slide's main point in 3 seconds?

**Example - Before (bad):**

```text
Title: Performance Improvements and Database Optimization

• Query caching reduced load by 40%
• Connection pooling improved throughput
• Indexes added to frequently accessed tables
• Migrated to read replicas for reporting
• Implemented batch processing for bulk operations
```

**Example - After (good):**

Slide 1:

```text
Title: Query Caching Cut Load by 40%

[Diagram showing before/after request flow with cache]
```

Slide 2:

```text
Title: Database Optimization Stack

• Connection pooling → throughput
• Strategic indexes → query speed
• Read replicas → reporting isolation
```

### Rule 2: Minimal Text

**Maximum guidelines:**

- Title: 5-8 words
- Bullets: 5-7 words each
- Bullets per slide: 3-5 maximum
- Body text: Almost never use paragraphs

**Why:** Audiences read faster than you speak. Text-heavy slides create competition between reading and listening.

**Instead of text, use:**

- Diagrams and flowcharts
- Screenshots with callouts
- Code snippets (highlighted)
- Simple data visualizations
- Icons and symbols

### Rule 3: Visual Hierarchy

Guide the eye with intentional design:

**Size hierarchy:**

1. Title (largest) - What this slide is about
2. Key message (medium) - The main takeaway
3. Supporting details (smaller) - Evidence or elaboration

**Color hierarchy:**

- Primary color for key elements
- Secondary color for supporting elements
- Muted tones for background/context
- Accent color for emphasis (use sparingly)

**Whitespace:**

- Don't fill every inch of the slide
- Margins create breathing room
- Whitespace directs attention to content

### Rule 4: Consistency Throughout

**Maintain across all slides:**

- Font families (1-2 maximum)
- Color palette (3-5 colors)
- Layout patterns (title position, content areas)
- Bullet styles
- Code formatting
- Diagram conventions

**Why:** Consistency reduces cognitive load. Audiences shouldn't wonder "what's different?" when moving between slides.

### Rule 5: Readable from the Back

**Minimum font sizes:**

| Element | Minimum Size | Recommended |
| ------- | ------------ | ----------- |
| Title | 32pt | 36-44pt |
| Body text | 24pt | 28-32pt |
| Code | 18pt | 20-24pt |
| Footnotes | 14pt | Avoid if possible |

**Test:** View your slides from 10-15 feet away. Can you read everything?

## Slide Types and Templates

### Title Slide

**Purpose:** Set context, establish credibility

**Elements:**

- Presentation title (clear, specific)
- Your name and role
- Company/context (if relevant)
- Date (for archival purposes)
- Optional: Conference/event name

**Tips:**

- Title should hint at value proposition
- Avoid generic titles ("Introduction to X")
- Include your contact info if slides will be shared

### Agenda Slide

**Purpose:** Set expectations (use sparingly, after hook)

**When to use:**

- Longer presentations (30+ minutes)
- Multiple distinct sections
- When audience needs to know what's coming

**When to skip:**

- Short presentations (under 20 minutes)
- When you haven't hooked them yet
- Lightning talks

**Format:**

```text
What We'll Cover

1. The Problem We Faced
2. How We Solved It
3. Results and Lessons
4. What You Can Apply Today
```

### Content Slide (Standard)

**Purpose:** Deliver one key point with support

**Layout options:**

**Title + Bullets:**

```text
[TITLE: Action-oriented statement]

• Key point 1
• Key point 2
• Key point 3
```

**Title + Visual:**

```text
[TITLE: What the visual shows]

[DIAGRAM/CHART/SCREENSHOT]

Optional: Brief caption or key insight
```

**Title + Split:**

```text
[TITLE: Comparison or progression]

[LEFT SIDE]     [RIGHT SIDE]
Before          After
Problem         Solution
Old way         New way
```

### Diagram/Architecture Slide

**Purpose:** Show relationships, flow, or structure

**Best practices:**

- Simplify ruthlessly (remove non-essential elements)
- Use consistent shapes for consistent concepts
- Label everything (don't assume knowledge)
- Show flow direction with arrows
- Limit to 7±2 elements per diagram
- Use color coding meaningfully

**Build-up technique:**

- Start with empty canvas
- Add elements progressively (animations or multiple slides)
- End with complete diagram
- This guides audience through complexity

### Code Slide

**Purpose:** Show implementation details

**Essential practices:**

- Syntax highlighting (always)
- Large font (18pt minimum, 20-24pt preferred)
- Maximum 10-15 lines per slide
- Highlight the key lines (bold, color, or arrow)
- Remove boilerplate (show only essential code)
- Add comments for context

**Format:**

```text
[TITLE: What this code demonstrates]

┌─────────────────────────────────────┐
│ // Highlighted line explanation     │
│ const cache = new LRUCache({        │
│   max: 500,                         │
│ → maxAge: 1000 * 60 * 15           │ ← This is the key line
│ });                                 │
└─────────────────────────────────────┘

Optional: One sentence of context below
```

**Anti-patterns to avoid:**

- Full file dumps
- Tiny font to fit more code
- No syntax highlighting
- No indication of what to look at
- Screenshots of code (prefer formatted text)

### Data/Chart Slide

**Purpose:** Support a claim with evidence

**Best practices:**

- One chart per slide
- Clear title stating the insight (not just "Revenue Data")
- Label axes and data points
- Highlight the key data point
- Provide context (what's good? what's bad?)
- Cite sources if external data

**Chart title patterns:**

- Bad: "Response Time Data"
- Good: "Response Time Dropped 60% After Optimization"

- Bad: "User Growth"
- Good: "We Reached 1M Users in 6 Months"

### Quote Slide

**Purpose:** Provide evidence, credibility, or emotional anchor

**Format:**

```text
"The quote goes here. Keep it short.
One to three sentences maximum."

— Attribution Name, Role/Context
```

**Tips:**

- Large, readable font
- Plenty of whitespace
- Source attribution is essential
- Use sparingly (1-2 per presentation)

### Summary/Takeaway Slide

**Purpose:** Reinforce key messages

**Format:**

```text
Key Takeaways

1. First main point (action-oriented)
2. Second main point (specific)
3. Third main point (memorable)
```

**Tips:**

- Maximum 3 takeaways (people can't remember more)
- Action-oriented language
- Specific enough to be useful
- Can be repeated at the end as a reminder

### Q&A Slide

**Purpose:** Signal transition to questions

**Options:**

- Simple "Questions?" with contact info
- Summary + "Questions?"
- "Let's Discuss" with discussion prompts
- Contact info + resources for follow-up

## Color and Typography

### Choosing Colors

**Start with your constraints:**

- Company brand colors (if required)
- Conference theme (if applicable)
- Venue lighting (dark room = high contrast needed)

**Safe color palette:**

- Background: White or very light gray
- Text: Dark gray (#333) rather than pure black
- Accent: One bold color for emphasis
- Secondary: One muted color for supporting elements

**For dark themes:**

- Background: Dark gray (#1a1a1a) rather than pure black
- Text: Off-white (#f0f0f0)
- Same accent principles apply

**Accessibility:**

- Ensure sufficient contrast (4.5:1 ratio minimum)
- Don't rely on color alone (add labels, patterns)
- Test for common color blindness (red-green)

### Typography Best Practices

**Font selection:**

- Sans-serif for body text (easier to read on screen)
- Limit to 2 font families maximum
- Use weight (bold) and size for hierarchy, not many fonts

**Recommended fonts:**

- Sans-serif: Inter, Roboto, Open Sans, Lato
- Monospace (code): JetBrains Mono, Fira Code, Source Code Pro

**Line spacing:**

- 1.3-1.5 line height for body text
- More space between elements than within

## Diagrams and Visuals

### When to Use Diagrams

**Use diagrams for:**

- System architecture
- Data flow
- Process steps
- Relationships between components
- Before/after comparisons
- Hierarchies and structures

**Skip diagrams when:**

- A simple list works better
- The concept is straightforward
- You don't have time to design it well

### Diagram Design Principles

**Simplify ruthlessly:**

- Remove decorative elements
- Eliminate non-essential components
- Use standard shapes consistently
- Limit connections/arrows

**Visual grammar:**

- Rectangles: Components, services, systems
- Circles/ovals: Data, events, states
- Diamonds: Decisions
- Arrows: Flow, relationships, dependencies
- Dashed lines: Optional, async, or weak connections

**Labeling:**

- Every element should be labeled
- Use consistent terminology
- Include brief descriptions if needed
- Consider adding a legend for complex diagrams

### Screenshots and Screencasts

**For screenshots:**

- Crop to relevant area only
- Add callouts/annotations for key areas
- Increase contrast if needed
- Consider device frames for context

**For embedded video/GIFs:**

- Keep short (10-30 seconds)
- No audio (you're narrating live)
- Loop if appropriate
- Have static fallback if tech fails

## Common Anti-Patterns

### The Wall of Text

**Problem:** Paragraph after paragraph of text

**Fix:** Extract key points into bullets, move details to speaker notes

### The Data Dump

**Problem:** Multiple charts crammed into one slide

**Fix:** One chart per slide, each supporting a specific claim

### The Rainbow

**Problem:** Too many colors with no meaning

**Fix:** Limit to 3-5 colors, each with purpose

### The Tiny Code

**Problem:** Full code file in 10pt font

**Fix:** Show only essential lines, increase font, highlight key parts

### The Template Nightmare

**Problem:** Default PowerPoint template that looks like 2005

**Fix:** Use modern, minimal template or build your own

### The Animation Circus

**Problem:** Every element flies in from different directions

**Fix:** Minimal, purposeful animations only (or none)

## Tools and Resources

### Recommended Tools

**Presentation software:**

- Google Slides (collaboration, free)
- PowerPoint (features, compatibility)
- Keynote (design, Mac)
- Reveal.js (developers, version control)
- Marp (Markdown-based)

**Diagram tools:**

- Excalidraw (hand-drawn style, free)
- Mermaid (text-based, version control friendly)
- draw.io (full-featured, free)
- Figma (design-focused)

**Code formatting:**

- Carbon (carbon.now.sh)
- Ray.so
- Syntax highlighting in presentation tool

### Template Resources

- **Slidesgo** - Free professional templates
- **Canva** - Easy customization
- **Google Slides templates** - Built-in options
- **Company templates** - Use if available (consistency)

## Checklist Before Presenting

- [ ] All text readable from back of room
- [ ] One main idea per slide
- [ ] Consistent design throughout
- [ ] Code is highlighted and readable
- [ ] Diagrams are labeled
- [ ] Colors are accessible
- [ ] No typos (have someone else check)
- [ ] Speaker notes added (if using)
- [ ] Tested on presentation equipment
- [ ] Backup copy available (USB, cloud, email to self)

---

**Related:** Return to `technical-presentations` skill for the complete framework, or see `demo-playbook.md` for live demo guidance.
