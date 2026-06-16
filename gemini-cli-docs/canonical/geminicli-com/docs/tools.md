---
source_url: http://geminicli.com/docs/tools
source_type: llms-txt
content_hash: sha256:2e724e031f1abf064572901a787878f29f823bb059a0ed9b38afe7b959cb207d
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"5c31de85b93159552f48104c8738abcd4493c2067d24836a1b0e2477fbfceaae"'
last_modified: '2026-03-02T02:03:05Z'
---

# Gemini CLI tools

Gemini CLI uses tools to interact with your local environment, access
information, and perform actions on your behalf. These tools extend the model's
capabilities beyond text generation, letting it read files, execute commands,
and search the web.

## User-triggered tools

You can directly trigger these tools using special syntax in your prompts.

- **[File access](/docs/tools/file-system#read_many_files) (`@`):** Use the `@` symbol
  followed by a file or directory path to include its content in your prompt.
  This triggers the `read_many_files` tool.
- **[Shell commands](/docs/tools/shell) (`!`):** Use the `!` symbol followed by a
  system command to execute it directly. This triggers the `run_shell_command`
  tool.

## Model-triggered tools

The Gemini model automatically requests these tools when it needs to perform
specific actions or gather information to fulfill your requests. You do not call
these tools manually.

### File management

These tools let the model explore and modify your local codebase.

- **[Directory listing](/docs/tools/file-system#list_directory) (`list_directory`):**
  Lists files and subdirectories.
- **[File reading](/docs/tools/file-system#read_file) (`read_file`):** Reads the
  content of a specific file.
- **[File writing](/docs/tools/file-system#write_file) (`write_file`):** Creates or
  overwrites a file with new content.
- **[File search](/docs/tools/file-system#glob) (`glob`):** Finds files matching a glob
  pattern.
- **[Text search](/docs/tools/file-system#search_file_content)
  (`search_file_content`):** Searches for text within files using grep or
  ripgrep.
- **[Text replacement](/docs/tools/file-system#replace) (`replace`):** Performs precise
  edits within a file.

### Agent coordination

These tools help the model manage its plan and interact with you.

- **Ask user (`ask_user`):** Requests clarification or missing information from
  you via an interactive dialog.
- **[Memory](/docs/tools/memory) (`save_memory`):** Saves important facts to your
  long-term memory (`GEMINI.md`).
- **[Todos](/docs/tools/todos) (`write_todos`):** Manages a list of subtasks for
  complex plans.
- **[Agent Skills](/docs/cli/skills) (`activate_skill`):** Loads specialized
  procedural expertise when needed.
- **[Browser agent](/docs/core/subagents#browser-agent-experimental)
  (`browser_agent`):** Automates web browser tasks through the accessibility
  tree.
- **Internal docs (`get_internal_docs`):** Accesses Gemini CLI's own
  documentation to help answer your questions.

### Information gathering

These tools provide the model with access to external data.

- **[Web fetch](/docs/tools/web-fetch) (`web_fetch`):** Retrieves and processes content
  from specific URLs.
- **[Web search](/docs/tools/web-search) (`google_web_search`):** Performs a Google
  Search to find up-to-date information.

## How to use tools

You use tools indirectly by providing natural language prompts to Gemini CLI.

1.  **Prompt:** You enter a request or use syntax like `@` or `!`.
2.  **Request:** The model analyzes your request and identifies if a tool is
    required.
3.  **Validation:** If a tool is needed, the CLI validates the parameters and
    checks your security settings.
4.  **Confirmation:** For sensitive operations (like writing files), the CLI
    prompts you for approval.
5.  **Execution:** The tool runs, and its output is sent back to the model.
6.  **Response:** The model uses the results to generate a final, grounded
    answer.

## Security and confirmation

Safety is a core part of the tool system. To protect your system, Gemini CLI
implements several safeguards.

- **User confirmation:** You must manually approve tools that modify files or
  execute shell commands. The CLI shows you a diff or the exact command before
  you confirm.
- **Sandboxing:** You can run tool executions in secure, containerized
  environments to isolate changes from your host system. For more details, see
  the [Sandboxing](/docs/cli/sandbox) guide.
- **Trusted folders:** You can configure which directories allow the model to
  use system tools.

Always review confirmation prompts carefully before allowing a tool to execute.

## Next steps

- Learn how to [Provide context](/docs/cli/gemini-md) to guide tool use.
- Explore the [Command reference](/docs/reference/commands) for tool-related
  slash commands.
