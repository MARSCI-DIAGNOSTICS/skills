---
name: setup-lsp
description: Set up LSP servers for the current project - auto-detects languages, researches recommendations, configures .lsp.json
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Skill, AskUserQuestion, mcp__perplexity__search, mcp__context7__query-docs
argument-hint: "[language|--auto|--check|--research <lang>]"
---

# Setup LSP Command

Interactive LSP server setup for Claude Code projects.

## Initialization

1. Load the `lsp-management` skill for server recommendations and configuration patterns.
2. Check for existing `.lsp.json` in project root.
3. Parse command arguments to determine mode.

## Argument Parsing

| Argument | Mode | Description |
| --- | --- | --- |
| *(none)* | Interactive | Scan project, ask user what to configure |
| `--auto` | Automatic | Auto-detect and configure without prompts |
| `--check` | Check | Report installed LSPs and available updates |
| `--research <lang>` | Research | Query MCP for latest recommendations for a language |
| `<language>` | Single | Configure LSP for specific language only |

## Mode: Interactive (Default)

When no arguments provided:

### Step 1: Scan Project

Scan for file extensions to detect languages in use:

```bash
# Find all unique file extensions
find . -type f -name "*.*" | sed 's/.*\.//' | sort -u
```

Or use Glob to find specific language files:

- `**/*.py` - Python
- `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` - TypeScript/JavaScript
- `**/*.go` - Go
- `**/*.rs` - Rust
- `**/*.cs` - C#
- `**/*.c`, `**/*.cpp`, `**/*.h` - C/C++

### Step 2: Present Findings

Use AskUserQuestion to let user choose:

```text
"I detected the following languages in your project: Python, TypeScript, C#. What would you like to do?"

Options:
1. "Configure all detected languages (Recommended)" - Set up LSPs for all
2. "Select specific languages to configure" - Choose which ones
3. "Research latest recommendations first" - Query MCP before configuring
4. "Check existing configuration" - Review current .lsp.json
```

### Step 3: Configure Selected Languages

For each language to configure:

1. Load server recommendation from `lsp-management` skill
2. Check if server is installed (run `<command> --version`)
3. If not installed, show installation command from skill
4. Generate `.lsp.json` entry

### Step 4: Generate Configuration

Create or update `.lsp.json` with generated entries.

If `.lsp.json` exists, use AskUserQuestion:

```text
"A .lsp.json already exists. How should I handle this?"

Options:
1. "Merge with existing configuration (Recommended)" - Add new entries, keep existing
2. "Replace existing configuration" - Overwrite completely
3. "Show me what would change" - Diff preview
```

### Step 5: Verification

After configuration:

1. Show final `.lsp.json` content
2. Suggest running `/audit-lsp` to validate
3. Note that Claude Code restart may be needed to pick up changes

## Mode: Automatic (--auto)

When `--auto` flag is provided:

1. Scan project for languages (same as Interactive Step 1)
2. For each detected language:
   - Use recommended server from skill
   - Check if installed
   - If not installed, warn but continue
3. Generate/merge `.lsp.json`
4. Report results

No AskUserQuestion prompts in this mode.

## Mode: Check (--check)

When `--check` flag is provided:

1. Read existing `.lsp.json`
2. For each configured server:
   - Check if command is available
   - Get current version
   - Query for latest version (if feasible)
3. Report status table:

```text
| Server | Installed | Version | Status |
| --- | --- | --- | --- |
| pyright | ✓ | 1.1.350 | Up to date |
| typescript-language-server | ✓ | 4.3.0 | Update available (4.4.0) |
| csharp-ls | ✗ | - | Not installed |
```

## Mode: Research (--research <lang>)

When `--research <language>` is provided:

1. Query MCP servers for latest recommendations:

   ```text
   mcp__perplexity__search: "best <language> language server 2026 LSP"
   mcp__context7__query-docs: "<language> LSP server"
   ```

2. Compare with skill's recommendations
3. Present findings to user
4. Ask if they want to proceed with configuration

## Mode: Single Language

When a language name is provided (e.g., `/setup-lsp python`):

1. Look up language in skill's server database
2. Check if server is installed
3. If not installed, provide installation command
4. Generate/update `.lsp.json` entry for that language only

## Server Installation Detection

To check if a server is installed:

```bash
# Try running with version flag
<command> --version 2>/dev/null && echo "installed" || echo "not installed"
```

Common commands:

| Server | Check Command |
| --- | --- |
| pyright | `pyright-langserver --version` |
| typescript-language-server | `typescript-language-server --version` |
| gopls | `gopls version` |
| rust-analyzer | `rust-analyzer --version` |
| csharp-ls | `csharp-ls --version` |
| clangd | `clangd --version` |

## Example Outputs

### Interactive Session

```text
User: /setup-lsp

Claude: Scanning project for languages...

Found: Python (.py), TypeScript (.ts, .tsx), JSON (.json)

I detected Python, TypeScript, and JSON files. What would you like to do?

[User selects "Configure all detected languages"]

Checking server installations...
✓ pyright-langserver is installed (1.1.350)
✓ typescript-language-server is installed (4.3.0)
✓ vscode-json-language-server is installed (1.3.4)

Generated .lsp.json:
{
  "pyright": { ... },
  "typescript": { ... },
  "json": { ... }
}

Configuration complete! Run /audit-lsp to validate.
```

### Auto Mode

```text
User: /setup-lsp --auto

Claude: Auto-detecting languages and configuring LSP...

Detected: Python, TypeScript
Configured: pyright, typescript-language-server
Created: .lsp.json

Done. Restart Claude Code to activate LSP servers.
```

### Research Mode

```text
User: /setup-lsp --research rust

Claude: Researching Rust LSP servers...

[Queries MCP servers]

Current recommendation: rust-analyzer
- Official Rust project
- Comprehensive features
- Active development

Alternative: None (rust-analyzer is de facto standard)

Would you like me to configure rust-analyzer for your project?
```

## Error Handling

### No Languages Detected

```text
"I couldn't detect any programming languages in this project.
Would you like to manually specify a language to configure?"
```

### Server Not Installed

```text
"pyright-langserver is not installed. Install it with:
  npm install -g pyright

Would you like me to proceed with the configuration anyway?
(The LSP won't work until the server is installed)"
```

### Invalid .lsp.json

```text
"The existing .lsp.json has syntax errors.
Would you like me to:
1. Fix the syntax and proceed
2. Back up and create a new configuration
3. Show me the errors"
```

## Project Configuration Detection

**CRITICAL:** `.lsp.json` tells Claude Code how to START the LSP server, but project config files tell the LSP server how to ANALYZE code.

After detecting languages, check for required project-level configs:

| Language | Required Project Config | Check Method |
| --- | --- | --- |
| Python | `pyrightconfig.json` OR `[tool.pyright]` in `pyproject.toml` | Glob for file, parse TOML section |
| TypeScript/JavaScript | `tsconfig.json` | Glob for file |
| C# | `*.sln` or `*.csproj` | Glob for solution/project files |
| Go | `go.mod` | Glob for file |
| Rust | `Cargo.toml` | Glob for file |

### Step: Project Config Verification

After language detection and before generating `.lsp.json`:

1. For each detected language, check if project config exists
2. If missing, report: "Python detected but no `pyrightconfig.json` found"
3. Ask user: "Would you like me to generate project configs for full LSP support?"

### Step: Project Config Generation

When project config is missing:

1. Query MCP for latest best practices:

   ```text
   mcp__perplexity__search: "pyrightconfig.json best practices 2026 typeCheckingMode"
   mcp__perplexity__search: "tsconfig.json 2026 NodeNext strict ES2024"
   mcp__context7__query-docs: Query /microsoft/pyright or /websites/typescriptlang
   ```

2. Generate config based on project structure + MCP research
3. Present to user with explanation of key settings
4. **Prompt for confirmation** before writing file
5. Write file to project root

### MCP-Validated Project Config Templates

Query MCP servers before generating to get current best practices. Here are baseline templates:

#### Python (pyrightconfig.json)

```json
{
  "include": ["src", "plugins"],
  "exclude": ["**/node_modules", "**/__pycache__", "**/.venv"],
  "venvPath": ".",
  "venv": ".venv",
  "typeCheckingMode": "standard",
  "pythonVersion": "3.13",
  "pythonPlatform": "All"
}
```

**Key settings to query MCP:**

- `typeCheckingMode`: "off" | "basic" | "standard" | "strict" | "all"
- `pythonVersion`: Check current stable version (3.13/3.14)

#### TypeScript (tsconfig.json)

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2024"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Key settings to query MCP:**

- `module/moduleResolution`: Modern options like "NodeNext"
- `target/lib`: Current ES versions

#### C# (.sln for root detection)

C# LSP servers (csharp-ls) require a `.sln` or `.csproj` file for root detection. If none exists:

```text
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.31903.59
MinimumVisualStudioVersion = 10.0.40219.1
Global
 GlobalSection(SolutionProperties) = preSolution
  HideSolutionNode = FALSE
 EndGlobalSection
EndGlobal
```

**Requirements to query MCP:**

- .NET SDK version (currently 10.0 LTS)
- csharp-ls version requirements

## Semantic Features Troubleshooting

If diagnostics work but hover/goToDefinition/documentSymbol don't:

1. **Check project config exists** - LSP servers need project configs for semantic features
2. **Verify ENABLE_LSP_TOOL=1** - Required environment variable for Claude Code LSP
3. **Restart Claude Code** - LSP servers may need to re-index after config changes
4. **Check server logs** - Look for initialization errors

## Important Notes

- This command creates/modifies `.lsp.json` in the project root
- Project configs (pyrightconfig.json, tsconfig.json, etc.) enable full semantic features
- Claude Code must be restarted to pick up new LSP configurations
- Use `/audit-lsp` after setup to validate the configuration
- The `lsp-management` skill provides all server recommendations
- Set `ENABLE_LSP_TOOL=1` environment variable for LSP tool access
