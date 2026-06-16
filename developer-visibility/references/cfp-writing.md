# CFP Writing Guide

Complete guide to writing conference proposals (Calls for Papers) that get accepted.

## Why Your Talk Proposal Gets Rejected

Before diving into how to write good proposals, understand why most get rejected:

| Rejection Reason | What It Looks Like |
| --- | --- |
| **Too generic** | "Introduction to React" (done a thousand times) |
| **No unique angle** | Same content as official docs |
| **Unclear takeaways** | Vague promises, no concrete outcomes |
| **Wrong fit** | Topic doesn't match conference audience |
| **Boring title** | Sounds like a textbook chapter |
| **No credibility signal** | Why should we believe you can deliver? |

## The CFP Title Formula

Your title is your first impression. It determines if reviewers even read your abstract.

### Formula

**Structure:** `[What we did] + [Problem/Solution] + [Why it matters]`

Or: `[Intriguing hook] + [Specific context]`

### Title Patterns That Work

#### Pattern 1: The Story Hook

Implies a journey with conflict and resolution.

**Examples:**

- "We Migrated to Microservices and Regretted It (For a While)"
- "How Our AI Onboarding Bot Confused Three New Devs—And What We Changed"
- "We Fine-Tuned ChatGPT, Then It Started Correcting Our CTO"

#### Pattern 2: The Unexpected Outcome

Subverts expectations.

**Examples:**

- "The Weirdest DevOps Hack I Ever Built—And Why It Worked"
- "How Deleting 10,000 Lines of Code Made Us Ship Faster"
- "Why Our Most Productive Engineer Writes the Least Code"

#### Pattern 3: The Specific Metric

Concrete results are compelling.

**Examples:**

- "From 30-Second Deploys to 30-Minute Confidence: Our CI/CD Journey"
- "How We Reduced Our Cloud Bill by 40% Without Sacrificing Performance"
- "Zero to 10 Million Users: Scaling Lessons That Actually Work"

#### Pattern 4: The Honest Confession

Vulnerability is memorable.

**Examples:**

- "All the Ways I've Broken Production (And How to Not Be Me)"
- "My First Year as a Tech Lead: Everything I Did Wrong"
- "The Debug Session That Took Three Days for a Typo"

### Titles to Avoid

❌ "Introduction to [Technology]" - Too generic
❌ "Best Practices for [X]" - Vague, overused
❌ "[Technology] Deep Dive" - What specifically?
❌ "How to [Basic Thing]" - Sounds like a tutorial, not a talk
❌ "[Technology]: A Comprehensive Overview" - Sounds like documentation

## The Abstract Structure

A good abstract has five components:

### 1. Hook (1-2 sentences)

Why should anyone care? What's the problem or opportunity?

### 2. Context (2-3 sentences)

What was the situation? Who are you, and why are you credible?

### 3. Approach (2-3 sentences)

What did you do? What was your methodology?

### 4. Results (1-2 sentences)

What happened? What did you learn?

### 5. Takeaways (3 bullet points)

What will attendees walk away with? Be specific.

### Abstract Template

```text
[HOOK: Compelling opening that establishes relevance]

[CONTEXT: Brief setup - the problem, the situation, who was involved]

[APPROACH: What you did, the journey, key decisions made]

[RESULTS: What happened, lessons learned, outcomes]

Attendees will walk away with:
• [Specific, actionable takeaway 1]
• [Specific, actionable takeaway 2]
• [Specific, actionable takeaway 3]

This talk is ideal for [target audience] who are [dealing with what situation].
```

### Example Abstract

**Title:** "We Migrated to Microservices and Regretted It (For a While)"

```text
Everyone said microservices would solve our scaling problems. So we broke
apart our monolith—and immediately created 47 new ones.

At [Company], our 12-person engineering team spent 18 months migrating from
a Django monolith to a microservices architecture. Six months in, we were
slower, more confused, and questioning everything. But we pushed through,
and here's what we found on the other side.

This talk covers our migration journey: the architectural decisions that
seemed smart (but weren't), the tooling choices that saved us, and the
organizational changes that actually mattered more than the technical ones.
I'll share the specific metrics from before, during, and after—including
the quarter where our velocity dropped 60%.

Attendees will walk away with:
• A realistic migration checklist based on painful lessons learned
• Warning signs that you're not ready for microservices (we ignored them)
• The organizational prerequisites that matter more than technical skills

This talk is ideal for tech leads and senior engineers considering or
currently navigating a microservices migration.
```

## Credibility Signals

Conference reviewers need to believe you can deliver. Include subtle credibility:

### In Your Bio

- Relevant job title and company
- Years of experience in the topic
- Previous speaking experience (any level)
- Related content you've created (blogs, talks)

### In Your Abstract

- Specific details (numbers, timelines, team size)
- Named technologies and tools
- Honest admission of challenges
- Clear evidence you've actually done this

## Targeting the Right Conference

### Research Before Submitting

1. **Read past talk titles** - What topics get accepted?
2. **Watch previous talks** - What style/depth is expected?
3. **Check the audience** - Junior devs? Staff engineers? Specific technology users?
4. **Note the format** - Lightning talks? 45-minute deep dives? Workshops?

### Conference Types

| Type | Typical Talks | Best For |
| --- | --- | --- |
| **Language/Framework** | Technical deep dives, new features | Specific expertise |
| **Methodology** | Process, culture, practices | Cross-functional topics |
| **Industry** | Domain-specific challenges | Vertical expertise |
| **Local/Regional** | Broad, beginner-friendly | First-time speakers |
| **Enterprise** | Case studies, scale challenges | Industry experience |

### Tailor Your Proposal

Same core topic, different angles for different conferences:

**DevOps Conference:**
> "How We Reduced Deployment Anxiety with GitOps and Feature Flags"

**JavaScript Conference:**
> "Building a Feature Flag System in Node.js That Actually Works"

**Leadership Conference:**
> "Empowering Teams to Ship Fearlessly: A Cultural Approach to Deployment Safety"

## Starting Small

You don't need to start at KubeCon.

### Progression Path

1. **Internal talks** - Team meetings, brown bags, tech shares
2. **Local meetups** - Language/framework user groups
3. **Lightning talks** - 5-10 minute conference slots
4. **Online events** - Virtual meetups, webinars
5. **Regional conferences** - Smaller, more accessible
6. **Major conferences** - Submit once you have a track record

### Finding Opportunities

- **Papercall.io** - Aggregator of open CFPs
- **ConfsWorld** - Conference discovery
- **Meetup.com** - Local tech meetups
- **Dev community Slacks** - Often share CFP opportunities
- **Conference Twitter accounts** - Follow and watch for announcements

## After You Submit

### If Accepted

1. **Confirm quickly** - Slots go to alternates
2. **Start early** - Don't procrastinate on slides
3. **Practice** - Run through at least 3x before the event
4. **Prepare for Q&A** - Anticipate questions

### If Rejected

1. **Ask for feedback** - Some conferences provide it
2. **Don't take it personally** - Competition is fierce
3. **Refine and resubmit** - Same talk can work elsewhere
4. **Build your track record** - Start smaller if needed

## CFP Checklist

Before submitting, verify:

- [ ] Title is compelling and specific (not generic)
- [ ] Abstract follows Hook-Context-Approach-Results-Takeaways structure
- [ ] Takeaways are specific and actionable (not vague)
- [ ] Target audience is clear
- [ ] Credibility signals are present (experience, specifics)
- [ ] Proposal matches conference audience and format
- [ ] Bio is relevant and concise
- [ ] All required fields are completed
- [ ] Spelling and grammar are checked

---

**Related:** Return to `developer-visibility` skill for the full framework, or see `storytelling-frames.md` for content structure patterns.
