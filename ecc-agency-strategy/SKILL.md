---
name: ecc-agency-strategy
description: "OpenClaw bridge skill for agency strategy. Use when requests involve agency strategy, market positioning, strategic options, or go-to-market direction and need OpenClaw-native execution with explicit verification."
---

# ecc-agency-strategy

## Purpose
Apply `strategy` guidance from upstream references in an OpenClaw-native workflow.

## Trigger Conditions
- User request clearly matches `strategy` capability.
- Task benefits from specialized domain guidance plus execution steps.

## When NOT to Use
- Generic tasks better handled by broader `ecc-cmd-*` workflows.
- Requests unrelated to `strategy` specialization.

## Workflow
1. Read upstream reference snapshot in `references/upstream-path.txt`.
2. Extract relevant guidance for the current objective.
3. Translate to OpenClaw tool-backed steps.
4. Execute incrementally and verify outcomes.

## Output Format
- Objective
- Chosen approach
- Actions executed
- Verification evidence
- Risks/next steps

## Guardrails
- Preserve upstream intent without assuming harness-specific runtime semantics.
- Prefer deterministic checks and concise, evidence-backed conclusions.
