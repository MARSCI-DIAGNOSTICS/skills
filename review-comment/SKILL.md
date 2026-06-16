---
name: review-comment
description: Generate a well-structured code review comment using Conventional Comments format. Helps give clear, actionable feedback on PRs.
argument-hint: [describe the issue or observation]
allowed-tools: Read, AskUserQuestion
---

# Code Review Comment Generator

Generate constructive code review comments using the Conventional Comments format for clarity and professionalism.

## Instructions

Based on the user's description of an issue or observation, generate a well-formatted code review comment.

### Step 1: Understand the Issue

Ask the user for:

1. **What's the issue or observation?** - What did they notice in the code?
2. **Context** - What file/function/line is this about?
3. **Severity** - Is this blocking (must fix) or non-blocking (nice to have)?
4. **Suggested fix** - Do they have a recommendation? (optional)

If the user has already provided this information, proceed directly to generating the comment.

### Step 2: Classify the Comment

Determine the appropriate label:

| Label | Use when... |
| ----- | ----------- |
| `praise` | Highlighting something done well |
| `nitpick` | Minor style or preference issue |
| `suggestion` | Improvement idea, not required |
| `issue` | Bug or problem that needs fixing |
| `question` | Need clarification or understanding |
| `thought` | Sharing perspective, no action needed |

Determine decoration:

- `(blocking)` - Must fix before merge
- `(non-blocking)` - Optional, author can ignore
- `(if-minor)` - Only if it's a quick fix

### Step 3: Generate the Comment

Format: `[label] (decoration): [subject]`

```markdown
## Review Comment

**Label:** [label]
**Decoration:** (blocking/non-blocking)
**Location:** [file:line if known]

---

### Comment

**[label] ([decoration]):** [Brief subject line]

[Explanation of why this matters]

[Suggested fix if applicable]

---

### Alternative Phrasings

If you'd like different tone options:

**More direct:**
> [Direct version]

**More gentle:**
> [Softer version]

---

### Tips

- [Any context about how this might be received]
- [Alternative approaches if the author disagrees]
```

## Examples

### Example 1: Bug

**User input:** "They're not handling null when the user doesn't exist"

**Generated comment:**

````markdown
**issue (blocking):** Null pointer exception when user not found

`getUserById` can return `undefined` when the user doesn't exist, but we're accessing `.name` directly without a check.

This will crash the application when someone tries to look up a deleted user.

**Suggested fix:**
```javascript
const user = getUserById(id);
if (!user) {
  throw new UserNotFoundError(id);
}
return user.name;
```
````

### Example 2: Nitpick

**User input:** "Variable names are kind of vague"

**Generated comment:**

```markdown
**nitpick (non-blocking):** Consider more descriptive variable names

`x` and `tmp` don't convey what these values represent. Names like `userCount` and `pendingRequests` would make this easier to understand at a glance.

No action required if you prefer to keep them - just a readability thought.
```

### Example 3: Praise

**User input:** "Really clean error handling"

**Generated comment:**

```markdown
**praise:** Excellent error handling coverage

Love how you've handled each error case explicitly with meaningful error messages. This will make debugging production issues much easier. The separation of retriable vs. fatal errors is especially nice.
```

## Tone Calibration

The generated comment should:

- Focus on the code, not the person
- Explain "why" for non-obvious feedback
- Include a suggestion when pointing out problems
- Use collaborative language ("we", "let's", "consider")

## Related Resources

- `code-review-communication` skill - Full frameworks for code review
- `references/conventional-comments.md` - Complete label taxonomy
