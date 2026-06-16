---
name: create-runbook
description: Generate operational runbook from system analysis. Use for incident response, operational procedures, troubleshooting guides, and emergency protocols.
allowed-tools: Read, Glob, Grep, Write, Skill
argument-hint: <topic> [--type incident|operational|troubleshooting|emergency] [--service <name>]
---

# Create Operational Runbook

Generate a runbook for operational procedures, incident response, or troubleshooting.

## Process

### 1. Parse Arguments

Extract from user input:

- **Topic**: Procedure name (required) - e.g., "database failover", "deploy to production"
- **Type**: `incident`, `operational`, `troubleshooting`, `emergency` (default: `operational`)
- **Service**: Specific service/system (optional)

### 2. Analyze Context

Based on the topic and type, gather relevant information:

**For incident runbooks:**

- What alerts trigger this runbook?
- What are common causes?
- What metrics indicate the issue?
- What are the resolution steps?

**For operational runbooks:**

- What is the procedure?
- What are the prerequisites?
- What are the verification steps?
- What could go wrong?

**For troubleshooting runbooks:**

- What symptoms indicate the issue?
- What diagnostic steps are needed?
- What are common fixes?
- When to escalate?

**For emergency runbooks:**

- What constitutes the emergency?
- What immediate actions are required?
- Who needs to be notified?
- What is the recovery process?

### 3. Load Skill and Generate

1. Load the `runbook-creation` skill for templates
2. Select appropriate template based on `type` argument
3. Generate runbook with:
   - Comprehensive metadata
   - Step-by-step procedures
   - Decision trees where applicable
   - Troubleshooting sections
   - Escalation paths

### 4. Create File

Determine file location:

```text
Priority order:
1. docs/runbooks/{type}/RB-{number}-{slug}.md
2. docs/operations/runbooks/RB-{number}-{slug}.md
3. runbooks/RB-{number}-{slug}.md
```

Numbering:

- Find existing runbooks, increment number
- Or use date-based: RB-2025-01-{sequence}

### 5. Populate Content

Generate content sections based on type:

**All types include:**

- Metadata table (ID, category, service, owner, dates)
- Overview (purpose, when to use, expected outcome)
- Prerequisites
- Main procedure with numbered steps
- Troubleshooting section
- Escalation path

**Type-specific sections:**

| Type | Additional Sections |
|------|---------------------|
| incident | Alert details, impact assessment, communication templates |
| operational | Rollback procedure, verification checklist |
| troubleshooting | Symptom/cause matrix, diagnostic commands |
| emergency | Immediate actions, notification list, recovery steps |

## Output Content

### Incident Runbook Structure

```markdown
# Incident Runbook: {TOPIC}

| Property | Value |
|----------|-------|
| **ID** | RB-INC-{NUMBER} |
| **Alert** | [Alert name] |
| **Severity** | [SEV1/2/3/4] |
| **Service** | {SERVICE} |
| **Owner** | [Team] |
| **Last Updated** | {DATE} |

## Alert Details
[Alert trigger conditions]

## Immediate Actions (First 5 Minutes)
1. Acknowledge alert
2. Assess impact
3. Initial communication

## Diagnosis
[Decision tree and diagnostic steps]

## Resolution
[Step-by-step fix procedures]

## Verification
[How to confirm resolution]

## Communication
[Status update templates]

## Post-Incident
[Cleanup and follow-up tasks]
```

### Operational Runbook Structure

```markdown
# Runbook: {TOPIC}

| Property | Value |
|----------|-------|
| **ID** | RB-OPS-{NUMBER} |
| **Category** | Operational |
| **Service** | {SERVICE} |
| **Owner** | [Team] |
| **Last Updated** | {DATE} |
| **Estimated Duration** | [Time] |

## Overview
[Purpose and when to use]

## Prerequisites
[Access, tools, knowledge needed]

## Procedure

### Step 1: [Name]
[Detailed instructions with commands]

### Step 2: [Name]
[Detailed instructions]

## Verification
[How to confirm success]

## Rollback
[How to undo if needed]

## Troubleshooting
[Common issues and fixes]
```

## Example Invocations

```text
/create-runbook "database failover"
→ Creates operational runbook for database failover procedure

/create-runbook "high error rate" type=incident service="api-gateway"
→ Creates incident runbook for API gateway error rate alerts

/create-runbook "pod crash loop" type=troubleshooting service="order-service"
→ Creates troubleshooting guide for order service pod crashes

/create-runbook "security breach response" type=emergency
→ Creates emergency runbook for security incidents
```

## Content Generation Guidelines

When generating runbook content:

### Commands

- Include actual, tested commands
- Use environment variables for sensitive data
- Add expected output examples

### Decision Points

- Use clear flowchart notation
- Cover all branches (success and failure)
- Include "when in doubt" guidance

### Timing

- Estimate time for each step
- Note SLA implications
- Include "if taking too long" escalation

### Communication

- Provide copy-paste templates
- Include notification channels
- Specify stakeholder expectations

## Post-Creation Guidance

After creating the runbook:

1. **Fill in specifics** - Replace placeholders with actual commands/URLs
2. **Validate commands** - Test all commands in non-production
3. **Review with SME** - Have subject matter expert verify
4. **Test execution** - Do a dry run of the procedure
5. **Train team** - Ensure operators know it exists
6. **Schedule review** - Set calendar reminder for quarterly review

## Quality Criteria

Generated runbook must:

- [ ] Have unique identifier
- [ ] Include all required metadata
- [ ] Provide actionable step-by-step instructions
- [ ] Include verification steps after each major action
- [ ] Cover failure scenarios and rollback
- [ ] Define escalation path and contacts
- [ ] Be testable in non-production environment
