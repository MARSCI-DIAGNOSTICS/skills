---
source_url: https://cursor.com/help/ai-features/terminal
source_type: llms-txt
content_hash: sha256:3daf50ce70913a5cc90754e5c279af6b4d30ea85d61f22e446bffc4f37d13034
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Terminal integration

Cursor's AI works inside the terminal too. Generate commands with natural language, and let Agent run terminal commands as part of larger tasks.

## Can Agent run terminal commands on its own?

Yes. When Agent needs to install dependencies, run tests, or check build output, it runs terminal commands automatically. On macOS and Linux, commands run in a sandbox that blocks unauthorized file access and network activity by default.

You can configure how Agent runs commands in **Cursor Settings > Agents > Auto-Run**: run in sandbox, ask every time, or run everything.

## What is the Cursor CLI?

The Cursor CLI brings Agent to your terminal as a standalone tool. It supports Agent, Plan, and Ask modes without opening the editor. Install it with:

```bash
curl https://cursor.com/install -fsS | bash
```

Learn more in the [CLI help article](https://cursor.com/help/integrations/cli.md) or at [cursor.com/cli](https://cursor.com/cli).

## Related

- [Terminal reference](https://cursor.com/docs/agent/tools/terminal.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
