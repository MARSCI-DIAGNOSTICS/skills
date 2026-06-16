---
name: brand-statement
description: Develop your personal brand statement using the Skills x Interests x Market Needs framework. Use when crafting your professional positioning, LinkedIn headline, or elevator pitch.
argument-hint: "[optional: your current role or focus area]"
allowed-tools: Read, AskUserQuestion
---

# Develop Personal Brand Statement

Guide an interactive discovery process to craft an authentic personal brand statement that positions you effectively.

## Arguments

`$ARGUMENTS` - Optional context about your current role, focus area, or career goals

## Workflow

### Step 1: The Niche Discovery Framework

Guide through the **Skills x Interests x Market Needs** exercise:

#### Part A: Skills Inventory

Use AskUserQuestion to gather (allow multiple selections):

**Question 1: Technical Strengths** (header: "Tech Skills", multiSelect: true)

- Backend development
- Frontend development
- DevOps/Infrastructure
- System design/Architecture
- Data/Analytics
- Security
- Mobile development
- AI/ML

**Question 2: Soft Skills** (header: "Soft Skills", multiSelect: true)

- Teaching/Explaining
- Writing/Documentation
- Public speaking
- Mentoring
- Project leadership
- Cross-team collaboration
- Problem decomposition
- Stakeholder communication

Then ask: "What do colleagues consistently ask you for help with?"

#### Part B: Interests Exploration

**Question 3: What Energizes You** (header: "Interests", multiSelect: true)

- Building tools that save others time
- Solving complex technical problems
- Teaching and growing others
- Improving processes and efficiency
- Exploring new technologies
- Building communities
- Creating content (writing, speaking)
- Debugging and firefighting

Then ask: "What would you do even if you weren't paid for it?"

#### Part C: Market Needs Analysis

**Question 4: Industry Trends** (header: "Market", multiSelect: true)

- AI/ML implementation
- Platform engineering
- Developer experience
- Security/DevSecOps
- Cloud optimization
- Remote team effectiveness
- Code quality/Architecture
- Observability/Reliability

Then ask: "What problems do you see companies paying consultants to solve?"

### Step 2: Find the Overlap

Analyze responses to identify niche:

```text
        ┌─────────────────┐
        │     SKILLS      │
        │  [User's tech   │
        │   strengths]    │
        └────────┬────────┘
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
  ┌───────┐  ┌───────┐  ┌───────┐
  │       │  │ YOUR  │  │       │
  │       │◄─┤ NICHE ├─►│       │
  │       │  │       │  │       │
  └───┬───┘  └───────┘  └───┬───┘
      │                     │
      ▼                     ▼
┌─────────────┐   ┌─────────────┐
│  INTERESTS  │   │   MARKET    │
│ [What they  │   │   NEEDS     │
│   enjoy]    │   │ [Demand]    │
└─────────────┘   └─────────────┘
```

Identify 2-3 potential niches where circles overlap.

### Step 3: Craft the Brand Statement

Use the formula:

> "I help **[target audience]** achieve **[specific outcome]** by **[your unique approach]**"

**Components:**

| Component | What to Include |
| --- | --- |
| **Target audience** | Be specific: role + context |
| **Specific outcome** | Concrete result they want |
| **Unique approach** | Your methodology, perspective, or experience |

### Step 4: Generate Statement Options

Produce 3-5 variations:

```markdown
## Personal Brand Statement Options

### Option 1: The Educator
> "I help [audience] understand [complex topic] by breaking it down into practical, actionable steps."

### Option 2: The Problem Solver
> "I help [audience] overcome [specific challenge] through [your methodology]."

### Option 3: The Translator
> "I help [technical audience] and [non-technical audience] work better together by [bridging method]."

### Option 4: The Builder
> "I help [audience] ship [outcome] faster by creating [tools/processes/systems]."

### Option 5: The Guide
> "I help [audience] navigate [transition/challenge] based on lessons from [your experience]."
```

### Step 5: Context-Specific Variations

Generate versions for different contexts:

```markdown
## Brand Statement Variants

### LinkedIn Headline (120 characters max)
[Role] | [Specialization] | [Value hook]

### Twitter/X Bio (160 characters max)
[Concise version with personality]

### Elevator Pitch (30 seconds)
"I'm a [role] who specializes in [niche]. I help [audience] by [approach]. Recently, I [credibility example]."

### Full Bio (100 words)
[Expanded version for conference submissions, about pages]

### One-Liner (10 words)
[The most distilled version]
```

### Step 6: Validation Questions

Before finalizing, check:

```markdown
## Validation Checklist

Test your statement against these criteria:

- [ ] **Natural:** Can you say it in conversation without feeling awkward?
- [ ] **Memorable:** Would someone remember this after meeting you?
- [ ] **Differentiated:** Does this distinguish you from others in your field?
- [ ] **Authentic:** Does this reflect who you actually are?
- [ ] **Actionable:** Does it suggest what you can do for someone?
- [ ] **Believable:** Can you back this up with evidence?
```

## Example Output

```markdown
## Your Personal Brand Discovery

### Niche Identified
Based on your inputs, your sweet spot appears to be:
**Helping backend teams build reliable systems at scale**

This combines:
- **Skills:** Distributed systems, system design, debugging
- **Interests:** Solving complex problems, teaching others
- **Market:** Reliability engineering, platform teams

---

### Primary Brand Statement

> "I help backend teams build systems that don't page them at 3 AM by sharing battle-tested patterns from scaling startups to millions of users."

---

### Context Variants

**LinkedIn Headline:**
> Senior Backend Engineer | Distributed Systems | Helping teams build reliable systems at scale

**Elevator Pitch:**
> I'm a backend engineer who specializes in distributed systems and reliability. I help teams build systems that scale without keeping them up at night. Last year, I led our team from 99.9% to 99.99% uptime while reducing on-call incidents by 60%.

**One-Liner:**
> I help teams build systems that scale reliably.

---

### Suggested Next Steps

1. Update your LinkedIn headline
2. Refresh your GitHub bio
3. Use this framing in your next intro
4. Start content on this niche topic
```

## Example Usage

```bash
# With context
/soft-skills:brand-statement I'm a senior backend engineer interested in developer experience

# Career transition
/soft-skills:brand-statement Moving from individual contributor to tech lead

# Start fresh
/soft-skills:brand-statement
```

## Output

Present complete brand discovery with:

1. **Niche identification** - Where your circles overlap
2. **Primary brand statement** - The main positioning
3. **Context variants** - LinkedIn, elevator pitch, bio versions
4. **Validation checklist** - Tests for the statement
5. **Next steps** - Where to apply it

## Common Archetypes

If struggling to find a niche, consider these developer archetypes:

| Archetype | Brand Statement Pattern |
| --- | --- |
| **The Educator** | "I help [learners] master [topic] through [teaching style]" |
| **The Builder** | "I help [users] accomplish [outcome] by building [tools]" |
| **The Optimizer** | "I help [teams] improve [metric] through [methodology]" |
| **The Translator** | "I help [group A] and [group B] work better together" |
| **The Guide** | "I help [audience] navigate [transition] based on [experience]" |
| **The Fixer** | "I help [teams] solve [problem type] that others find impossible" |
