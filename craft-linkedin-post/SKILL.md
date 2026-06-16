---
name: craft-linkedin-post
description: Generate an engaging LinkedIn post using proven storytelling frames. Use when you want to share learnings, celebrate wins, or build professional visibility.
argument-hint: [topic, story, or idea to share]
allowed-tools: Read, AskUserQuestion
---

# Craft LinkedIn Post

Generate an engaging LinkedIn post optimized for developer audiences using proven storytelling frameworks.

## Arguments

`$ARGUMENTS` - The topic, story idea, or content you want to share

## Workflow

### Step 1: Gather Context

If `$ARGUMENTS` is insufficient, use AskUserQuestion to gather:

**Question 1: Post Type** (header: "Post Type")

- Learning/Mistake (share what you learned the hard way)
- Behind the Build (how you built something)
- Win/Milestone (celebrate an achievement)
- Opinion/Take (share a perspective)
- Quick Tip (tactical advice)

**Question 2: Goal** (header: "Goal")

- Build authority (establish expertise)
- Start discussion (spark conversation)
- Share value (help others)
- Announce something (news, milestone)
- Connect (relate to audience)

### Step 2: Select Storytelling Frame

Based on post type, apply the appropriate frame:

#### Frame 1: Learning the Hard Way

```text
[Bold opening about the mistake]

Last [timeframe], I [what you did wrong].

Here's what happened:
→ [Consequence 1]
→ [Consequence 2]
→ [Consequence 3]

The lesson: [Key insight]

What's a lesson you learned the hard way?
```

#### Frame 2: Behind the Build

```text
[What you built and why it matters]

Here's what nobody tells you about building [X]:

1. [Surprising challenge + how you solved it]
2. [Unexpected discovery]
3. [What you'd do differently]

The biggest lesson: [Key insight]

Have you built something similar?
```

#### Frame 3: Before/After

```text
[The dramatic contrast]

Before: [Specific pain point]
After: [Specific improvement]

Here's what changed:

Step 1: [First change]
Step 2: [Second change]
Step 3: [Third change]

The key insight: [What made the biggest difference]
```

#### Frame 4: Contrarian Take

```text
Unpopular opinion: [Your view]

I know this goes against [common wisdom].

But here's what I've seen:
→ [Evidence 1]
→ [Evidence 2]
→ [Evidence 3]

[Nuanced conclusion]

What's your experience?
```

#### Frame 5: Quick Win

```text
A simple trick that [benefit]:

[Describe the technique]

Why it works:
→ [Reason 1]
→ [Reason 2]

I use this [when/how often].

What's your go-to hack?
```

### Step 3: Craft the Hook

The first 1-2 lines determine if people click "see more."

**Hook Techniques:**

| Type | Example |
| --- | --- |
| Dramatic moment | "At 2 AM, I got the call no engineer wants." |
| Surprising statement | "Our most productive engineer writes the least code." |
| Honest confession | "I deleted 10,000 lines of code. My manager thanked me." |
| Bold claim | "Everyone's doing microservices wrong. Including us." |
| Question | "Why do we still write documentation nobody reads?" |

### Step 4: Apply Formatting Best Practices

**Structure:**

- One sentence per line
- Use line breaks liberally (no walls of text)
- Bullet points with → or • for lists
- Bold key phrases sparingly
- End with a question or CTA

**Length:**

- Optimal: 150-300 words
- Too short: Lacks substance
- Too long: People won't finish

**Engagement elements:**

- End with a question that invites sharing
- Tag relevant people (if appropriate)
- 3-5 relevant hashtags (at end)

### Step 5: Generate Post

Produce a complete, ready-to-post LinkedIn update:

```markdown
## LinkedIn Post

---

[Hook line that makes people want to click "see more"]

[Second line that builds on the hook]

[Body content using selected storytelling frame]

[Key insight or takeaway]

[CTA - Question that invites engagement]

#hashtag1 #hashtag2 #hashtag3

---

### Optimization Notes
- **Hook strength:** [Assessment]
- **Storytelling frame:** [Which frame used]
- **Engagement prompt:** [What you're asking]
- **Best posting time:** [Suggestion based on audience]
```

### Step 6: Offer Variations

After presenting the post, offer:

1. **Hook alternatives** - Different opening approaches
2. **Tone adjustment** - More/less formal or casual
3. **Length variants** - Shorter version or expanded version
4. **Different frame** - Same content, different structure

## Example Usage

```bash
# With topic
/soft-skills:craft-linkedin-post I learned why you shouldn't deploy on Friday

# With story idea
/soft-skills:craft-linkedin-post We reduced our deploy time from 30 minutes to 3 minutes

# Start with questions
/soft-skills:craft-linkedin-post
```

## Output

Present a complete, ready-to-post LinkedIn update with:

1. **The post itself** - Formatted and ready to copy
2. **Hook assessment** - Strength of the opening
3. **Hashtag suggestions** - Relevant tags
4. **Posting tips** - Timing and engagement advice
5. **Alternative versions** - If applicable

## Quality Checklist

Before posting:

- [ ] Hook makes people want to click "see more"
- [ ] Contains specific details (not generic statements)
- [ ] Has emotional texture (not just facts)
- [ ] Clear takeaway for the reader
- [ ] Ends with engagement prompt
- [ ] Formatted with line breaks (no walls of text)
- [ ] 3-5 relevant hashtags

## Anti-Patterns to Avoid

- Generic statements without specifics
- Corporate jargon ("leveraging synergies")
- All wins, no vulnerability
- Missing call-to-action
- Walls of text (no line breaks)
- More than 5-7 hashtags
- Tagging people who didn't contribute
