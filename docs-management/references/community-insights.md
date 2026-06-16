# Community Insights: Claude Code Design Philosophy

This reference captures clarifications from Anthropic employees and Claude Code creators that inform design decisions. These insights supplement official documentation with context and philosophy.

## Source Attribution

Insights are attributed with date and source type:

- **Boris Cherny** - Claude Code creator
- **Anthropic Employee** - Team members with direct knowledge

---

## Skills vs Commands (v2.1.3+)

**Source:** Boris Cherny (January 2026)

### Unified Implementation, Conceptual Distinction

> "Skills and slash commands are the same thing" at the implementation level, but maintain a conceptual distinction:

| Aspect | Commands | Skills |
| ------ | -------- | ------ |
| **Semantics** | Imperative "do something *now*" | Knowledge + procedures package |
| **Trigger** | User-triggered (explicit `/command`) | Model-triggered (discovered by description) |
| **Invocation** | Appended per invocation | Load once per session |

### Model-Driven Invocation (Future Direction)

> "The model will do most invocation. Design for model discoverability."

**Implications:**

- Write skill descriptions that help the model understand when to invoke
- Include trigger keywords the model will recognize
- Focus on what the skill does and when to use it

### `user-invocable: false` Field

> "Use `user-invocable: false` to make it so only the model can invoke a skill."

**When to use:**

- Meta-skills that the model should discover automatically
- Knowledge packages that don't need user-initiated triggers
- Skills where the model should decide when they're relevant

**Effect:** Hides the skill from the `/` menu while allowing model discovery via description matching.

---

## Context Isolation (`context: fork`)

**Source:** Anthropic Employee (January 2026)

### Parent Context "Prompt-Injection"

> "The parent context will 'prompt-inject' the subagent. Use `context: fork` when you want an uncorrelated context window."

**When to use `context: fork`:**

- Unbiased criticism or review (don't want parent opinions influencing)
- Independent analysis (separate context window)
- Unrelated tasks (prevent context bleeding)
- When agent should "think more independently"

**How it works:**

- Creates isolated sub-agent context
- Prevents parent conversation from influencing responses
- Agent operates with fresh context

---

## Skill Design Best Practices

**Source:** Boris Cherny (January 2026)

### Description Quality

Good descriptions enable model discoverability:

```yaml
# Good - keyword-rich, explains purpose and scope
description: Central authority for Claude Code hooks. Covers hook events,
  configuration, matchers, decision control. Use when working with
  PreToolUse, PostToolUse, UserPromptSubmit hooks.

# Bad - vague, no keywords
description: Helps with hooks.
```

### Classification Decision Tree

1. **Does it require user initiation?** (network, disk, audit)
   - Yes → Command
   - No → Continue

2. **Does it provide knowledge/procedures the model should discover?**
   - Yes → Skill with `user-invocable: false`
   - No → Continue

3. **Does user explicitly invoke it for specific actions?**
   - Yes → Skill with `user-invocable: true` (default)
   - No → Consider if it should be a skill at all

---

## Agent Field

**Source:** Boris Cherny (January 2026)

When using `context: fork`, specify the agent type:

```yaml
---
name: my-skill
context: fork
agent: code-reviewer
---
```

The `agent` field specifies which agent type handles the forked execution.

---

## Design Philosophy Summary

1. **Model-first design:** Write for model discoverability, not just user menus
2. **Semantic clarity:** Commands = imperative now, Skills = knowledge package
3. **Context awareness:** Use `context: fork` when independence matters
4. **Description quality:** Invest in keyword-rich, purpose-clear descriptions

---

**Last Updated:** 2026-01-10
**Sources:** Boris Cherny Twitter/X threads, Anthropic employee Discord discussions (January 2026)
