---
source_url: http://geminicli.com/docs/tools/activate-skill
source_type: llms-txt
content_hash: sha256:e3882a1c0387de563bd88024f23e419360d9a0bbf4d9de6a457652aa4bc1ddfc
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"4f5e79aace1dd6a0acaafb4d5342063d1804304c26c9a05b121e3a0adbe5cf86"'
last_modified: '2026-03-02T02:03:05Z'
---

# Activate skill tool (`activate_skill`)

The `activate_skill` tool lets Gemini CLI load specialized procedural expertise
and resources when they are relevant to your request.

## Description

Skills are packages of instructions and tools designed for specific engineering
tasks, such as reviewing code or creating pull requests. Gemini CLI uses this
tool to "activate" a skill, which provides it with detailed guidelines and
specialized tools tailored to that task.

### Arguments

`activate_skill` takes one argument:

- `name` (enum, required): The name of the skill to activate (for example,
  `code-reviewer`, `pr-creator`, or `docs-writer`).

## Usage

The `activate_skill` tool is used exclusively by the Gemini agent. You cannot
invoke this tool manually.

When the agent identifies that a task matches a discovered skill, it requests to
activate that skill. Once activated, the agent's behavior is guided by the
skill's specific instructions until the task is complete.

## Behavior

The agent uses this tool to provide professional-grade assistance:

- **Specialized logic:** Skills contain expert-level procedures for complex
  workflows.
- **Dynamic capability:** Activating a skill can grant the agent access to new,
  task-specific tools.
- **Contextual awareness:** Skills help the agent focus on the most relevant
  standards and conventions for a particular task.

## Next steps

- Learn how to [Use Agent Skills](/docs/cli/skills).
- See the [Creating Agent Skills](/docs/cli/creating-skills) guide.
