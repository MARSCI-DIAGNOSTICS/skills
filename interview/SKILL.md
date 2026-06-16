---
name: interview
description: Conduct an AI-led requirements elicitation interview with a stakeholder. Uses LLMREI research-backed patterns for effective requirement capture.
argument-hint: "[stakeholder-role] [--context <project-context>] [--mode <autonomy-mode>] [--domain <domain-name>]"
allowed-tools: Read, Glob, Grep, Write, Skill, AskUserQuestion
---

# Interview Command

Conduct a structured requirements elicitation interview using AI-led LLMREI patterns.

## Usage

```bash
/requirements-elicitation:interview "Product Manager" --context "checkout redesign"
/requirements-elicitation:interview "End User" --mode guided --domain "e-commerce"
/requirements-elicitation:interview "Technical Lead" --mode semi-auto
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| stakeholder-role | Yes | Role of the person being interviewed (e.g., "Product Manager", "End User") |
| --context | No | Project or feature context for the interview |
| --mode | No | Autonomy mode: `guided`, `semi-auto`, `full-auto` (default: `semi-auto`) |
| --domain | No | Domain name for organizing output files |

## Workflow

### Step 1: Initialize Interview Context

Parse arguments and set up interview:

```yaml
interview_setup:
  stakeholder_role: "{from argument}"
  project_context: "{from --context or ask}"
  autonomy_mode: "{from --mode or default}"
  domain: "{from --domain or derive from context}"
  session_id: "INT-{timestamp}"
```

### Step 2: Load Interview Skill

Invoke the `requirements-elicitation:interview-conducting` skill to load question pathways and structure.

### Step 3: Determine Interview Mode

**If Real Stakeholder (default):**

- Stakeholder is the human in the chat
- Use AskUserQuestion for structured questions
- Allow natural conversation flow

**If Simulated (--simulate flag or no human response):**

- Spawn appropriate persona agent
- Conduct interview with simulated stakeholder
- Mark all requirements with lower confidence

### Step 4: Conduct Interview

Spawn the `requirements-interviewer` agent with the interview context.

The agent will:

1. Open the interview and establish rapport
2. Gather context about the stakeholder's role
3. Explore requirements systematically
4. Validate understanding through summarization
5. Close with next steps

### Step 5: Save Results

Save interview results to:

```text
.requirements/{domain}/interviews/INT-{session-id}.yaml
```

### Step 6: Report Summary

Display:

- Number of requirements elicited
- Key themes identified
- Gaps or follow-up items
- Path to saved interview file

## Examples

### Basic Interview

```bash
/requirements-elicitation:interview "Product Manager"
```

Starts a semi-autonomous interview with a Product Manager, asking for project context.

### Guided Interview with Context

```bash
/requirements-elicitation:interview "Security Officer" --context "authentication system" --mode guided
```

Starts a guided interview where each question is approved before asking.

### Full-Auto Interview for Exploration

```bash
/requirements-elicitation:interview "Developer" --mode full-auto --domain "api-redesign"
```

Conducts a complete interview autonomously, presenting the summary at the end.

## Output

### During Interview

For guided mode:

```text
AI: "I suggest asking: 'What security concerns do you have about the current system?'
     Do you approve this question?"
```

For semi-auto mode:

```text
AI: [Conducts segment]
    "Interview progress: Context gathering complete.
     3 requirements identified so far.
     Ready to explore functional requirements. Continue?"
```

### After Interview

```yaml
Interview Complete: INT-20251225-143022

Stakeholder: Product Manager
Duration: ~25 minutes
Mode: semi-auto

Requirements Elicited: 12
  - Functional: 8
  - Non-Functional: 3
  - Constraints: 1

Key Themes:
  - User authentication improvements
  - Performance during peak hours
  - Mobile responsiveness

Gaps Identified: 2
  - Accessibility requirements not discussed
  - Disaster recovery needs clarification

Saved to: .requirements/checkout/interviews/INT-20251225-143022.yaml

Next Steps:
  - Review extracted requirements
  - Schedule follow-up for gaps
  - Run /requirements-elicitation:gaps for completeness check
```

## Integration

### Follow-Up Commands

After an interview:

```bash
# Check for gaps in elicited requirements
/requirements-elicitation:gaps

# Simulate other stakeholder perspectives
/requirements-elicitation:simulate "security" --personas technical,compliance

# Research domain-specific requirements
/requirements-elicitation:research "PCI-DSS compliance"

# Export to specification format
/requirements-elicitation:export --to canonical
```

### With Multiple Stakeholders

Conduct multiple interviews, then consolidate:

```bash
/requirements-elicitation:interview "Product Manager" --domain "checkout"
/requirements-elicitation:interview "Developer" --domain "checkout"
/requirements-elicitation:interview "End User" --domain "checkout"

# Then discover consolidates all sources
/requirements-elicitation:discover "checkout" --sources interviews
```
