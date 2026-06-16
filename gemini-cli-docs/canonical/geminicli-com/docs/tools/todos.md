---
source_url: http://geminicli.com/docs/tools/todos
source_type: llms-txt
content_hash: sha256:9518f9f816cf2f2a723065f6942fe61fa53f19cd78b9cf3f608a70b0cda840ee
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"cc8f9df6c6532c8fb355301b914b20b36be700bd7bcbc38194771221b157ef28"'
last_modified: '2026-03-22T19:06:33Z'
---

# Todo tool (`write_todos`)

The `write_todos` tool allows the Gemini agent to maintain an internal list of
subtasks for multi-step requests.

## Technical reference

The agent uses this tool to manage its execution plan and provide progress
updates to the CLI interface.

### Arguments

- `todos` (array of objects, required): The complete list of tasks. Each object
  includes:
  - `description` (string): Technical description of the task.
  - `status` (enum): `pending`, `in_progress`, `completed`, `cancelled`, or
    `blocked`.

## Technical behavior

- **Interface:** Updates the progress indicator above the CLI input prompt.
- **Exclusivity:** Only one task can be marked `in_progress` at any time.
- **Persistence:** Todo state is scoped to the current session.
- **Interaction:** Users can toggle the full list view using **Ctrl+T**.

## Use cases

- Breaking down a complex feature implementation into manageable steps.
- Coordinating multi-file refactoring tasks.
- Providing visibility into the agent's current focus during long-running tasks.

## Next steps

- Follow the [Task planning tutorial](/docs/cli/tutorials/task-planning) for
  usage details.
- Learn about [Session management](/docs/cli/session-management) for context.
