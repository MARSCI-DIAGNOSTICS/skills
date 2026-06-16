# Receiving Code Review Feedback

A guide to receiving code review feedback gracefully, learning from it, and maintaining professional relationships.

## The Right Mindset

### Code is Not You

The most important shift: **your code is not your identity**.

When someone critiques your code, they're not critiquing you as a person or engineer. They're helping improve a shared artifact that you both care about.

| Unhelpful Thought | Reframe |
| ----------------- | ------- |
| "They think I'm incompetent" | "They caught something I missed" |
| "They're nitpicking everything" | "They care about quality" |
| "This is embarrassing" | "Everyone gets feedback, that's how we grow" |
| "They don't understand my approach" | "I should explain my reasoning" |

### Assume Good Intent

Reviewers are (almost always) trying to help. Even harsh-sounding feedback usually comes from a place of wanting to improve the codebase.

Before reacting defensively:

- Pause and re-read the comment
- Assume the reviewer wants to help
- Consider if they're right (even if poorly phrased)
- Ask for clarification if truly unclear

### Everyone Gets Feedback

Senior engineers, staff engineers, CTOs - everyone gets code review feedback. It's not a sign of weakness; it's how professional software development works.

The best engineers are the ones who:

- Welcome feedback openly
- Ask for more scrutiny on risky changes
- Thank reviewers for catching issues
- Learn and don't repeat the same mistakes

## Practical Responses

### When They're Right

The easiest case - just acknowledge and fix:

```text
"Good catch, fixed in the latest commit."

"You're right, I missed that edge case. Added a test and handled it."

"Thanks for the suggestion - that's cleaner. Updated."
```

No need to over-explain or apologize excessively. A simple acknowledgment shows professionalism.

### When You Disagree

Disagreement is normal and healthy. Handle it professionally:

1. **Understand first**: Make sure you understand their point before disagreeing
2. **Explain your reasoning**: Share why you chose your approach
3. **Stay objective**: Focus on trade-offs, not preferences
4. **Be open to being wrong**: You might learn something

```text
"I see your point about X. I went with this approach because of Y trade-off.
What do you think about that consideration?"

"That's a valid concern. I chose this pattern because [reason].
Happy to change if you feel strongly, but wanted to explain my thinking."

"Interesting - I hadn't considered that. Let me think about it and
I'll follow up with my thoughts."
```

### When You Need Clarification

It's completely fine to ask for more details:

```text
"Could you elaborate on what you mean by 'this could cause issues'?
I want to make sure I understand the concern."

"Are you suggesting we change the interface, or just the implementation?
I want to make sure I address the right thing."

"What would you expect this to look like? I'm not sure I follow."
```

### When Feedback Is Harsh

Sometimes feedback is poorly phrased. Options:

1. **Address the substance, ignore the tone**: Focus on the technical point
2. **Ask for clarification neutrally**: "Could you help me understand what you're looking for?"
3. **Take it offline**: "This seems like a bigger discussion - want to hop on a call?"
4. **Talk to your manager**: If it's a pattern, escalate appropriately

Do NOT:

- Respond in kind with harsh comments
- Get into a public argument in the PR
- Ignore the feedback entirely
- Assume malice without evidence

## Learning from Feedback

### Track Patterns

If you keep getting the same feedback, that's a signal:

| Repeated Feedback | What to Learn |
| ----------------- | ------------- |
| Missing tests | Write tests first (TDD) |
| Edge cases | Spend more time on error handling |
| Code style | Configure your linter |
| Documentation | Document as you code |
| Performance | Consider performance earlier |

### Ask for Specific Feedback

When you want to improve in an area, ask specifically:

```text
"I'm working on improving my error handling - would you mind
paying extra attention to that in this review?"

"I tried a new pattern here for state management.
Would love your thoughts on whether this is a good approach."

"I'm not confident about the database query performance.
Could you take a close look at that section?"
```

### Thank Your Reviewers

A simple thank you goes a long way:

```text
"Thanks for the thorough review!"

"Really appreciate you catching that - would have been a nasty bug."

"Great suggestion, I learned something new."
```

## When to Take It Offline

Some discussions are better had synchronously:

- Fundamental disagreements about approach
- Complex trade-offs that need whiteboarding
- Emotional/tense exchanges
- Reviews that are going in circles
- Architecture decisions that affect others

Suggest:

```text
"This is a good discussion - want to hop on a quick call to hash it out?"

"I think we're talking past each other. Let's sync up for 10 minutes?"
```

## Common Scenarios

### The Nitpick Storm

When you get many small comments:

1. Fix the obvious ones quickly
2. Address patterns once (e.g., "I'll run the formatter")
3. Ask if any are blocking

### The Fundamental Redesign

When the reviewer wants a major change:

1. Understand their concerns fully
2. Discuss trade-offs of both approaches
3. Consider if a smaller change addresses the core issue
4. Involve others if it's a big decision
5. Don't take it personally - better to catch design issues now

### The Silent Approval

When you get approved with no comments:

- Could mean the code is great
- Could mean the reviewer didn't look closely
- Consider asking: "Any thoughts on the approach?"

### The Delayed Review

When reviews take too long:

- Ping politely after reasonable time
- Offer to walk through the PR
- Keep PRs small to make review easier
- Don't take it personally

## Building a Feedback Culture

### As a Reviewee

- Request reviews promptly
- Provide context in PR descriptions
- Respond to feedback quickly
- Thank reviewers genuinely
- Learn from patterns in feedback

### As a Reviewer

- Review promptly
- Use Conventional Comments
- Balance criticism with praise
- Explain the "why" behind suggestions
- Be kind but honest
