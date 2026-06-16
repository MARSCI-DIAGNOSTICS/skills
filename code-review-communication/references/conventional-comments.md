# Conventional Comments Reference

A standardized system for labeling code review comments to clarify intent and reduce miscommunication.

## The Problem

Code review comments are often ambiguous:

- Is this a blocker or just a thought?
- Does the author need to change this or is it optional?
- Is this criticism or feedback?

Conventional Comments solve this by prefixing each comment with a clear label.

## Format

```text
[label] (decorations): [subject]

[discussion]
```

**Components:**

- **label** (required): The type of comment
- **decorations** (optional): Additional context like `(non-blocking)`
- **subject** (required): Brief summary
- **discussion** (optional): Detailed explanation

## Labels

### praise

Highlight something positive. Helps balance critical feedback and reinforces good patterns.

```text
praise: This is a really elegant solution to the caching problem.

praise: Great test coverage - I especially like how you handled the edge cases.
```

**When to use:**

- When you see genuinely good code
- To reinforce patterns you want repeated
- At least once per review (find something positive)

### nitpick

Minor, stylistic issues. Low priority, often personal preference.

```text
nitpick (non-blocking): I'd prefer camelCase for this variable name.

nitpick: Trailing whitespace on line 42.
```

**When to use:**

- Style preferences not enforced by linter
- Minor inconsistencies
- "If I'm being picky..." situations

**Important:** Always mark as `(non-blocking)` unless there's a specific reason.

### suggestion

A recommendation to improve the code. Not required but worth considering.

```text
suggestion: Consider using `Array.from()` here - it handles edge cases better.

suggestion (non-blocking): You could extract this into a helper function for reusability.
```

**When to use:**

- Alternative approaches that might be better
- Opportunities for improvement
- "You could also..." ideas

### issue

Something that must be fixed before merging. Use sparingly.

```text
issue (blocking): This will throw a null pointer exception when user is undefined.

issue: Missing authentication check - anyone could access this endpoint.
```

**When to use:**

- Bugs that will cause production issues
- Security vulnerabilities
- Breaking changes
- Missing required functionality

### question

Need clarification or understanding. Expects a response.

```text
question: What happens if the file doesn't exist? Should we handle that case?

question: Is this intentionally different from how we handle it in UserService?
```

**When to use:**

- Genuine confusion about the approach
- Checking if edge cases are handled
- Understanding the reasoning

### thought

Sharing perspective without requiring action. Just information.

```text
thought: I've seen this pattern cause issues with race conditions in the past. Might be worth keeping an eye on.

thought: This reminds me of a similar approach in the payment service - might be worth consolidating later.
```

**When to use:**

- Sharing experience or context
- Future considerations
- "FYI" information

## Decorations

Add decorations in parentheses after the label:

### (non-blocking)

Explicitly optional. The author can ignore this without discussion.

```text
nitpick (non-blocking): Could use more descriptive variable names.
```

### (blocking)

Must be resolved before merge. Use for critical issues.

```text
issue (blocking): SQL injection vulnerability - must use parameterized queries.
```

### (if-minor)

Only address if it's a trivial fix. Don't spend significant time.

```text
suggestion (if-minor): Could add a brief comment explaining the algorithm.
```

## Best Practices

### Always Label

Every comment should have a label. This removes ambiguity.

| Unlabeled (Ambiguous) | Labeled (Clear) |
| --------------------- | --------------- |
| "Use camelCase here" | "nitpick (non-blocking): Use camelCase here" |
| "This could cause issues" | "issue: This could cause a race condition" |
| "Nice!" | "praise: Clean solution, easy to follow" |

### Be Specific

Vague feedback is unhelpful. Be specific about what and why.

| Vague | Specific |
| ----- | -------- |
| "This is confusing" | "question: What does `processData` do with null inputs?" |
| "Needs improvement" | "suggestion: Consider extracting the validation logic" |
| "Wrong" | "issue: This returns null but caller expects empty array" |

### Suggest Solutions

When pointing out problems, offer solutions when possible.

````text
issue: This loop is O(n²) which will be slow for large datasets.

Consider using a Map for O(1) lookups:
```js
const userMap = new Map(users.map(u => [u.id, u]));
```
````

### Balance Criticism

If you have several critical comments, look for something to praise. Reviews that are 100% criticism feel demoralizing even when valid.

## Anti-Patterns to Avoid

### The Drive-By Comment

❌ Just "Fix this" with no context

✅ Explain what's wrong and suggest a solution

### The Passive-Aggressive Question

❌ "Did you even test this?"

✅ "question: What test cases did you run? I want to make sure we cover X."

### The Preferences-as-Requirements

❌ Marking style preferences as blocking

✅ Use `nitpick (non-blocking)` for preferences

### The Nitpick Storm

❌ 20 nitpicks about formatting

✅ One comment suggesting running the formatter, then focus on substance

## Integration Tips

### Team Adoption

1. Share this reference with your team
2. Start using labels yourself (lead by example)
3. Gently remind others when comments are ambiguous
4. Add labels to your PR template or guidelines

### With GitHub/GitLab

Most platforms support markdown in comments. Format as:

```markdown
**nitpick (non-blocking):** Consider using a more descriptive name here.
```

Or use plain text with the label prefix.

## Sources

- [conventionalcomments.org](https://conventionalcomments.org/)
- [Graphite: Conventional Comments Guide](https://graphite.dev/guides/conventional-comments)
