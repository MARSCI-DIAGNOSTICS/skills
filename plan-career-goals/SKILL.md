---
name: plan-career-goals
description: Create structured career goals with timelines, actions, milestones, and accountability measures.
argument-hint: <target role or aspiration>
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, Skill
---

# Plan Career Goals Command

Generate a structured career goal plan with actionable steps, milestones, and accountability measures.

## Workflow

### Step 1: Understand the Aspiration

If `$ARGUMENTS` provided, use as target aspiration.

If no arguments, ask:

- "What career goal or aspiration would you like to plan for?"

Examples:

- "Get promoted to Senior Engineer"
- "Transition to a tech lead role"
- "Move into machine learning"
- "Increase compensation by 30%"

### Step 2: Gather Context

Ask clarifying questions to understand current state:

**Current State:**

- What is your current role/level?
- How long have you been at this level?
- What are your main strengths?
- What feedback have you received?

**Target State:**

- What specifically does success look like?
- What timeline are you considering?
- What constraints do you have?
- What resources are available?

### Step 3: Load Career Strategy Skill

Invoke the `soft-skills:career-strategy` skill to load goal-setting framework and planning guidance.

### Step 4: Perform Gap Analysis

Analyze the gap between current and target state:

```markdown
## Gap Analysis: [Current] → [Target]

### Current State
- **Level:** [Current level]
- **Strengths:** [Key strengths]
- **Experience:** [Relevant experience]

### Target State
- **Goal:** [Specific target]
- **Timeline:** [Target date]
- **Success Criteria:** [How you'll know you've arrived]

### Gap Assessment

| Dimension | Current | Target | Gap Priority |
| --------- | ------- | ------ | ------------ |
| [Skill 1] | [Level] | [Level] | High/Medium/Low |
| [Skill 2] | [Level] | [Level] | High/Medium/Low |
| [Experience] | [Current] | [Needed] | High/Medium/Low |
```

### Step 5: Generate Goal Plan

Create structured plan using `career-goal` output style:

```markdown
## Career Goal Plan

### Goal Statement
[Specific, measurable goal with timeline]

### Why This Goal
[Connection to long-term vision]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

### Timeline
**Start:** [Date]
**Target Completion:** [Date]
**Duration:** [X months]

### Quarterly Milestones

**Q1: [Focus Area]**
- [ ] [Specific milestone]
- [ ] [Specific milestone]
- Checkpoint: [How to assess progress]

**Q2: [Focus Area]**
- [ ] [Specific milestone]
- [ ] [Specific milestone]
- Checkpoint: [How to assess progress]

**Q3: [Focus Area]**
- [ ] [Specific milestone]
- [ ] [Specific milestone]
- Checkpoint: [How to assess progress]

**Q4: [Focus Area]**
- [ ] [Specific milestone]
- [ ] [Specific milestone]
- Checkpoint: [How to assess progress]

### Action Plan

**High Priority Actions:**
1. **[Action]** - By [date]
   - Why: [Connection to goal]
   - Resources: [What you need]

2. **[Action]** - By [date]
   - Why: [Connection to goal]
   - Resources: [What you need]

**Supporting Actions:**
- [Action] - [Timeframe]
- [Action] - [Timeframe]

### Quick Wins (Start This Week)
- [ ] [Something achievable immediately]
- [ ] [Something achievable immediately]

### Resources Needed
- **Learning:** [Courses, books, mentors]
- **Experiences:** [Projects, stretch assignments]
- **Support:** [Manager, mentor, sponsor]
- **Time:** [Hours/week commitment]

### Accountability

**Share With:**
- Manager: [Conversation to have]
- Mentor: [Support to request]
- Peer: [Accountability partner]

**Check-in Cadence:**
- Weekly: [Self-review activity]
- Monthly: [Review meeting with...]
- Quarterly: [Milestone assessment]

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| [Risk 1] | H/M/L | H/M/L | [Plan] |
| [Risk 2] | H/M/L | H/M/L | [Plan] |

### Adjustment Triggers

Reassess this plan if:
- [ ] Major change in role or company
- [ ] Significant feedback changes direction
- [ ] Opportunity or obstacle emerges
- [ ] Progress significantly ahead/behind
```

### Step 6: Offer Follow-Up

After generating plan:

1. **Save the plan:** "Would you like me to save this to a file?"
2. **Discuss with manager:** "Would you like talking points for your manager 1:1?"
3. **Related goals:** "Would you like to plan additional goals?"

## Output Style

Use the `career-goal` output style for structured formatting.

## Example Invocation

```text
/soft-skills:plan-career-goals Get promoted to Senior Engineer within 12 months
```

## Related

- `career-strategy` skill - Goal setting framework
- `career-strategy` skill - Level expectations and career paths
- `career-goal` output style - Structured goal format
- `career-coach` agent - Interactive career guidance
