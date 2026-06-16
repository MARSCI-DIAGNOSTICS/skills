---
name: structure-presentation
description: Create a structured presentation outline using the What-Why-How framework. Use when preparing talks, demos, or technical presentations.
argument-hint: [presentation topic or title]
allowed-tools: Read, AskUserQuestion
---

# Structure Presentation

Generate a well-structured presentation outline optimized for technical audiences using proven frameworks.

## Arguments

`$ARGUMENTS` - The presentation topic, title, or subject matter

## Workflow

### Step 1: Gather Context

If `$ARGUMENTS` is insufficient, use AskUserQuestion to gather:

**Question 1: Presentation Type** (header: "Type")

- Technical deep-dive (architecture, implementation details)
- Demo or walkthrough (showing how something works)
- Decision pitch (proposing a solution or technology)
- Knowledge sharing (teaching concepts or patterns)
- Status update (progress, roadmap, results)

**Question 2: Audience** (header: "Audience")

- Technical peers (developers, engineers)
- Mixed technical/non-technical (stakeholders, cross-functional)
- Leadership (executives, decision-makers)
- External (customers, conference attendees)

**Question 3: Duration** (header: "Duration")

- Lightning talk (5-10 minutes)
- Standard slot (20-30 minutes)
- Deep dive (45-60 minutes)
- Workshop (90+ minutes)

**Question 4: Setting** (header: "Setting")

- Internal meeting (team, department)
- All-hands or company-wide
- Conference or meetup
- Customer-facing

### Step 2: Apply What-Why-How Framework

Structure the presentation using this proven framework:

#### WHAT (The Hook - 10% of time)

- **Grab attention** in the first 30 seconds
- State the problem or opportunity clearly
- Make the audience care immediately
- One sentence summary of what you'll cover

**Hook Techniques:**

- Provocative question ("What if we could...")
- Surprising statistic or fact
- Relatable pain point
- Bold statement

#### WHY (The Context - 30% of time)

- **Background** - Why does this matter?
- **Stakes** - What happens if we don't act?
- **Opportunity** - What's possible?
- **Relevance** - Why should the audience care?

**Structure Options:**

- Problem → Impact → Opportunity
- Before → After → How we got there
- Pain → Solution → Benefits

#### HOW (The Solution - 50% of time)

- **Approach** - How does it work?
- **Evidence** - Why should they believe you?
- **Demo** - Show, don't just tell
- **Specifics** - Concrete details, not abstractions

**For Technical Talks:**

- Architecture diagram
- Code walkthrough
- Live demo (if applicable)
- Performance data / metrics

#### CLOSE (Call to Action - 10% of time)

- **Summary** - Key takeaways (3 max)
- **Next steps** - What should they do?
- **Resources** - Where to learn more
- **Q&A** - Leave time for questions

### Step 3: Apply Presentation Best Practices

**Slide Design (if applicable):**

- One idea per slide
- 5-7 words per bullet (max)
- Visual > Text
- Consistent design language

**Timing Guidelines:**

| Duration | Slides | Content Depth |
| --- | --- | --- |
| 5-10 min | 5-10 | One main point + support |
| 20-30 min | 15-25 | 3-4 main points |
| 45-60 min | 30-40 | Deep dive, multiple sections |

**Engagement Techniques:**

- Ask questions (rhetorical or real)
- Use stories and examples
- Vary pace and energy
- Make eye contact
- Pause for emphasis

### Step 4: Generate Outline

Produce a complete presentation structure:

```markdown
## Presentation Outline

**Title:** [Compelling title]
**Duration:** [X minutes]
**Audience:** [Target audience]

---

### Opening Hook (X min)

**Attention Grabber:**
> "[Opening line/question/statistic]"

**The Promise:**
> "By the end of this talk, you'll understand [key outcome]"

---

### WHY This Matters (X min)

1. **The Problem/Opportunity**
   - [Key point]
   - [Supporting detail]

2. **The Stakes**
   - [What happens without action]
   - [Cost of status quo]

3. **The Vision**
   - [What's possible]
   - [Benefits to audience]

---

### HOW It Works (X min)

1. **[First main section]**
   - Key point
   - Evidence/example
   - [SLIDE: Visual suggestion]

2. **[Second main section]**
   - Key point
   - Evidence/example
   - [SLIDE: Visual suggestion]

3. **[Third main section]**
   - Key point
   - Evidence/example
   - [DEMO: If applicable]

---

### Call to Action (X min)

**Key Takeaways:**
1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]

**Next Steps:**
- [Specific action for audience]

**Resources:**
- [Link/reference 1]
- [Link/reference 2]

---

### Q&A (X min)

**Anticipated Questions:**
1. [Likely question] → [Prepared answer]
2. [Likely question] → [Prepared answer]
```

### Step 5: Offer Refinements

After presenting the outline, offer:

1. **Depth adjustment** - Add/remove sections
2. **Audience calibration** - More/less technical
3. **Slide suggestions** - Visual ideas for each section
4. **Speaker notes** - Talking points for each slide
5. **Practice run** - Walk through the timing

## Example Usage

```bash
# With topic
/soft-skills:structure-presentation Migrating from Monolith to Microservices

# Conference talk
/soft-skills:structure-presentation How We Reduced API Latency by 90%

# Decision pitch
/soft-skills:structure-presentation Why We Should Adopt Kubernetes

# Start with questions
/soft-skills:structure-presentation
```

## Output

Present complete presentation outline with:

1. **Title and metadata** (duration, audience, type)
2. **Opening hook** - Attention-grabbing opener
3. **What-Why-How structure** - Full outline
4. **Key takeaways** - Summary points
5. **Slide suggestions** - Visual guidance
6. **Timing breakdown** - Minutes per section

## Anti-Patterns to Avoid

- Starting with "Today I'm going to talk about..."
- Agenda slides that bore the audience
- Too many bullet points per slide
- Reading slides verbatim
- No clear takeaways
- Running over time
- Skipping Q&A
