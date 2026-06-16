---
source_url: http://geminicli.com/docs/tools/memory
source_type: llms-txt
content_hash: sha256:e3681c4e02d71cf18b927ca9ff620b464ff8a618e49ef58050ee6687c2275af3
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"2369057e69f0624cbb0c865f05b2f114a716725fa799a335b7b92b16d03e066b"'
last_modified: '2026-03-02T02:03:05Z'
---

# Memory tool (`save_memory`)

The `save_memory` tool allows the Gemini agent to persist specific facts, user
preferences, and project details across sessions.

## Technical reference

This tool appends information to the `## Gemini Added Memories` section of your
global `GEMINI.md` file (typically located at `~/.gemini/GEMINI.md`).

### Arguments

- `fact` (string, required): A clear, self-contained statement in natural
  language.

## Technical behavior

- **Storage:** Appends to the global context file in the user's home directory.
- **Loading:** The stored facts are automatically included in the hierarchical
  context system for all future sessions.
- **Format:** Saves data as a bulleted list item within a dedicated Markdown
  section.

## Use cases

- Persisting user preferences (for example, "I prefer functional programming").
- Saving project-wide architectural decisions.
- Storing frequently used aliases or system configurations.

## Next steps

- Follow the [Memory management guide](/docs/cli/tutorials/memory-management)
  for practical examples.
- Learn how the [Project context (GEMINI.md)](/docs/cli/gemini-md) system loads
  this information.
