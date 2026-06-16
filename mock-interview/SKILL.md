---
name: mock-interview
description: Run an interactive system design mock interview - simulates a real interview with problem statement, follow-ups, and structured feedback
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion
argument-hint: "<type: general|ml|data|staff> [problem-hint]"
---

# Mock Interview Command

This command runs a full interactive system design mock interview, simulating a real interview experience with problem presentation, follow-up questions, and structured feedback.

## Purpose

Provide realistic interview practice including:

1. Problem selection based on type and level
2. Timed interview simulation
3. Realistic follow-up questions and pushback
4. Structured feedback on performance
5. Specific improvement recommendations

## Interview Types

| Type | Focus | Interviewer Agent |
|------|-------|-------------------|
| `general` | Classic system design (URL shortener, Twitter, etc.) | architecture-critic |
| `ml` | ML systems (recommendation, search, fraud detection) | ml-interviewer |
| `data` | Data systems (pipelines, warehouses, streaming) | data-architect |
| `staff` | Staff+ level with hard pushback | senior-staff-interviewer |

## Workflow

### Phase 1: Interview Setup

**Parse arguments:**

- Determine interview type (default: general)
- Extract any problem hints or preferences
- Set difficulty level based on type

**Ask about preferences if needed:**

```text
Interview Setup:

1. Interview Type:
   - General system design (classic problems)
   - ML system design (recommendation, search, etc.)
   - Data engineering (pipelines, warehouses)
   - Staff+ level (rigorous, pushback-heavy)

2. Time Constraint:
   - 30 minutes (focused)
   - 45 minutes (standard)
   - 60 minutes (comprehensive)

3. Problem Preference:
   - Surprise me (recommended)
   - Specific domain: [e-commerce, social, fintech, etc.]
```

### Phase 2: Problem Presentation

**Select and present problem based on type:**

For `general`:

```text
Problem Examples:
- Design a URL shortening service like bit.ly
- Design a rate limiter for an API
- Design a distributed cache system
- Design a notification service
- Design a file sharing service like Dropbox
```

For `ml`:

```text
Problem Examples:
- Design a content recommendation system
- Design a search ranking system
- Design a fraud detection system
- Design a RAG-based chatbot
- Design an LLM serving infrastructure
```

For `data`:

```text
Problem Examples:
- Design a real-time analytics pipeline
- Design a data warehouse for an e-commerce company
- Design an event sourcing system
- Design a change data capture system
- Design a feature store
```

For `staff`:

```text
Problem Examples:
- Design a payment processing system ($100B scale)
- Design a global social media feed
- Design a multi-region database system
- Design a real-time bidding system
- Design a distributed transaction coordinator
```

**Present the problem:**

```text
═══════════════════════════════════════════════════════════════
                    SYSTEM DESIGN INTERVIEW
═══════════════════════════════════════════════════════════════

Problem: [Problem Statement]

[1-2 paragraphs with requirements and context]

Constraints:
- [Key constraint 1]
- [Key constraint 2]
- [Scale indicator if applicable]

You have [X] minutes. You may ask clarifying questions.
When ready, begin by gathering requirements.

═══════════════════════════════════════════════════════════════
```

### Phase 3: Spawn Interviewer Agent

Based on interview type, spawn the appropriate agent:

- `general` → spawn `architecture-critic` agent in interviewer mode
- `ml` → spawn `ml-interviewer` agent
- `data` → spawn `data-architect` agent in interviewer mode
- `staff` → spawn `senior-staff-interviewer` agent

**Agent instructions:**

```text
Conduct a system design interview for the following problem:

[Problem statement]

Interview parameters:
- Duration: [X] minutes
- Level: [Type/Level]
- Mode: Interactive interview

Interview phases:
1. Requirements (5 min) - Let candidate ask clarifying questions
2. High-level design (10 min) - Evaluate system components
3. Deep dive (15 min) - Probe 2-3 components in depth
4. Trade-offs (5 min) - Discuss alternatives and evolution

During the interview:
- Push back on surface-level answers
- Ask follow-up questions
- Simulate realistic time pressure
- Note strengths and areas for improvement

At the end, provide structured feedback.
```

### Phase 4: Interview Execution

The interviewer agent conducts the interview:

**Throughout the interview:**

- Present clarifying questions when candidate drives
- Provide incomplete information initially
- Probe deeper on interesting areas
- Challenge assumptions
- Track time and give updates
- Note key decisions and reasoning

**Example interactions:**

```text
Interviewer: "What questions do you have about the requirements?"

[After clarifying questions]

Interviewer: "Good questions. Let's start with your high-level design.
How would you approach this system?"

[After high-level design]

Interviewer: "Interesting choice with [component]. Let's dive deeper.
How would you handle [specific scenario]?"

[Probing]

Interviewer: "What happens when [failure scenario]?"
Interviewer: "How does this scale to 10x the load?"
Interviewer: "Why did you choose X over Y?"
```

### Phase 5: Feedback Delivery

After the interview, provide structured feedback:

```text
═══════════════════════════════════════════════════════════════
                    INTERVIEW FEEDBACK
═══════════════════════════════════════════════════════════════

## Overall Assessment

Rating: [Strong Hire / Hire / Lean Hire / No Hire]
Level: [Appropriate for: Junior / Mid / Senior / Staff]

## Strengths

1. [Strength 1 with specific example]
2. [Strength 2 with specific example]
3. [Strength 3 with specific example]

## Areas for Improvement

1. [Area 1 with specific recommendation]
2. [Area 2 with specific recommendation]
3. [Area 3 with specific recommendation]

## Component Coverage

| Component | Coverage | Depth |
|-----------|----------|-------|
| [Component 1] | [Good/Partial/Missing] | [Shallow/Adequate/Deep] |
| [Component 2] | [Good/Partial/Missing] | [Shallow/Adequate/Deep] |

## Key Moments

✓ Good: [Positive moment]
✓ Good: [Positive moment]
✗ Miss: [Missed opportunity]
✗ Miss: [Missed opportunity]

## Recommendations for Practice

1. [Specific topic to study]
2. [Skill to develop]
3. [Pattern to practice]

## Resources

- [Relevant skill to load]
- [Related practice problem]

═══════════════════════════════════════════════════════════════
```

## Usage Examples

```bash
# General system design interview
/sd:mock-interview general

# ML-focused interview
/sd:mock-interview ml

# Data engineering interview
/sd:mock-interview data

# Staff+ level rigorous interview
/sd:mock-interview staff

# Specific domain preference
/sd:mock-interview general e-commerce

# ML interview with specific focus
/sd:mock-interview ml "recommendation system"
```

## Interview Best Practices (For Candidates)

The command will share these at the start:

```text
Interview Tips:

1. START with clarifying questions
   - Don't jump to solutions
   - Understand requirements and constraints

2. STRUCTURE your approach
   - Start high-level, then dive deep
   - Use diagrams (describe them clearly)

3. THINK aloud
   - Share your reasoning
   - Discuss trade-offs as you go

4. MANAGE time
   - Don't spend too long on one area
   - Cover breadth before depth

5. ACKNOWLEDGE uncertainty
   - It's okay to say "I'd need to research X"
   - Better than guessing incorrectly
```

## Output

The command produces:

1. **Interactive Interview** - Realistic interview simulation
2. **Structured Feedback** - Detailed performance assessment
3. **Practice Recommendations** - Specific next steps

## Related Skills

This command leverages:

- `design-interview-methodology` - Interview framework
- `estimation-techniques` - Capacity calculations
- `quality-attributes-taxonomy` - NFR coverage

## Related Agents

Spawned based on interview type:

- `architecture-critic` - General system design
- `ml-interviewer` - ML systems
- `data-architect` - Data engineering
- `senior-staff-interviewer` - Staff+ level
