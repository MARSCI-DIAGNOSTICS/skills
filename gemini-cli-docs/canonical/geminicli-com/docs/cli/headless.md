---
source_url: http://geminicli.com/docs/cli/headless
source_type: llms-txt
content_hash: sha256:0c76556026820577ca1ead8c836c590a079e637100bff9790c0f1599d0f9f172
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"7f8819c16e2fd07eb102b5a5dee23cac9c90b3c14a6e081f03245482d5bfb7b6"'
last_modified: '2026-03-16T19:53:24Z'
---

# Headless mode reference

Headless mode provides a programmatic interface to Gemini CLI, returning
structured text or JSON output without an interactive terminal UI.

## Technical reference

Headless mode is triggered when the CLI is run in a non-TTY environment or when
providing a query with the `-p` (or `--prompt`) flag.

### Output formats

You can specify the output format using the `--output-format` flag.

#### JSON output

Returns a single JSON object containing the response and usage statistics.

- **Schema:**
  - `response`: (string) The model's final answer.
  - `stats`: (object) Token usage and API latency metrics.
  - `error`: (object, optional) Error details if the request failed.

#### Streaming JSON output

Returns a stream of newline-delimited JSON (JSONL) events.

- **Event types:**
  - `init`: Session metadata (session ID, model).
  - `message`: User and assistant message chunks.
  - `tool_use`: Tool call requests with arguments.
  - `tool_result`: Output from executed tools.
  - `error`: Non-fatal warnings and system errors.
  - `result`: Final outcome with aggregated statistics and per-model token usage
    breakdowns.

## Exit codes

The CLI returns standard exit codes to indicate the result of the headless
execution:

- `0`: Success.
- `1`: General error or API failure.
- `42`: Input error (invalid prompt or arguments).
- `53`: Turn limit exceeded.

## Next steps

- Follow the [Automation tutorial](/docs/cli/tutorials/automation) for practical
  scripting examples.
- See the [CLI reference](/docs/cli/cli-reference) for all available flags.
