---
name: track-win
description: Document an accomplishment in brag document format with proper categorization and impact metrics.
argument-hint: <accomplishment description>
allowed-tools: Read, Write, AskUserQuestion, Skill
---

# Track Win Command

Transform an accomplishment description into a well-structured brag document entry with categorization, quantification, and impact metrics.

## Workflow

### Step 1: Parse Accomplishment

Take the accomplishment description from `$ARGUMENTS`.

If no arguments provided, ask the user:

- "What accomplishment would you like to document?"

### Step 2: Extract Details

If the accomplishment lacks detail, ask probing questions:

**Scope Questions:**

- What specifically did you do?
- What was your role vs others' contributions?
- How long did this take?

**Impact Questions:**

- What problem did this solve?
- Who benefited from this work?
- What metrics changed as a result?

**Context Questions:**

- What tools, technologies, or approaches did you use?
- What challenges did you overcome?
- What skills did this demonstrate?

### Step 3: Apply Achievement Formula

Transform the description using the formula:

#### Action Verb + Specific Task + Quantifiable Result

Generate 2-3 variations of the achievement bullet, each emphasizing different aspects:

- Technical contribution
- Business impact
- Leadership/collaboration

### Step 4: Categorize the Win

Load guidance from `promotion-preparation` skill and categorize:

**Impact Type:** (select one)

- Delivery - Shipped something
- Quality - Improved reliability/reduced bugs
- Efficiency - Made things faster/cheaper
- Innovation - Created new approaches
- Leadership - Enabled others
- Collaboration - Worked across teams

**Scope Level:** (select one)

- Individual - Personal contribution
- Team - Team-wide impact
- Multi-Team - Cross-team impact
- Org-Wide - Organizational impact

**Competencies Demonstrated:** (select 1-3)

- Technical/Implementation
- Design
- Operations
- Product
- Leadership
- Communication

### Step 5: Suggest Quantification

If the win lacks metrics, suggest approaches to quantify:

**Time metrics:**

- Hours/days saved
- Time to completion
- Reduction in wait time

**Money metrics:**

- Cost savings
- Revenue impact
- Avoided expenses

**Scale metrics:**

- Users affected
- Requests handled
- Transactions processed

**Improvement metrics:**

- Percentage change
- Before/after comparison
- Frequency change

### Step 6: Generate Output

Format the win using the `achievement-bullet` output style:

```markdown
## [Win Title]

**Summary:** [One sentence]

**Achievement Bullets:**
- [Variation 1 - technical focus]
- [Variation 2 - business impact focus]
- [Variation 3 - leadership/collaboration focus]

**Categorization:**
- Impact Type: [Type]
- Scope Level: [Level]
- Competencies: [List]

**Quantified Impact:**
- [Metric 1]
- [Metric 2]

**Skills Demonstrated:**
- [Skill 1]
- [Skill 2]

**Date:** [Today's date in YYYY-MM-DD format]

**Evidence/Links:**
- [Where can this be verified? PR, doc, dashboard, etc.]
```

### Step 7: Offer Next Steps

After generating the entry, offer:

1. **Append to brag document:** If user has a brag document, offer to append
2. **Create brag document:** If none exists, offer to create one in `.claude/temp/`
3. **Copy to clipboard:** Offer formatted output for pasting elsewhere
4. **Track another:** Ask if they have more wins to document

## Output Style

Use the `achievement-bullet` output style for the formatted entry.

## Example Invocations

**Basic:**

```text
/soft-skills:track-win "Fixed the payment retry bug"
```

**With detail:**

```text
/soft-skills:track-win "Fixed the payment retry bug that was causing 2% of transactions to fail, worked with the payments team to identify the race condition, implemented distributed locking solution"
```

**Vague (will prompt for details):**

```text
/soft-skills:track-win "Helped with the migration"
```

## Related

- `/soft-skills:promotion-preparation` - Build full promotion case from wins
- `promotion-preparation` skill - Win categorization framework
