---
name: lint-md
description: Run markdown linting validation on files using markdownlint-cli2
argument-hint: [target-files-or-instructions]
allowed-tools: Read, Bash, Skill
---

# Lint Markdown Command

Run markdown linting validation on all or targeted markdown files using markdownlint-cli2.

## Instructions

**Use the code-quality:markdown-linting skill to handle the complete linting workflow.**

The markdown-linting skill provides:

- **Validation using markdownlint-cli2** (CLI tool or npm scripts)
- **Auto-fix capabilities** for fixable linting issues
- **Configuration guidance** for `.markdownlint-cli2.jsonc`
- **Rule explanations** and troubleshooting
- **VS Code integration** and GitHub Actions setup (optional/advanced)

**Simply invoke the skill and follow its guidance:**

```text
Use the code-quality:markdown-linting skill to run linting validation.

{IF ARGUMENTS PROVIDED}
Target the following files/folders: {ARGUMENTS}

The user provided: "{ARGUMENTS}"
This could be:
- Specific file paths (e.g., "README.md", "docs/setup.md")
- Folder paths (e.g., "docs/", ".claude/skills/")
- Glob patterns (e.g., "docs/**/*.md", "*.md")
- Natural language descriptions (e.g., "only skill documentation", "git-related docs")

Interpret the targeting instructions and construct the appropriate markdownlint-cli2 command.
{ENDIF}

{IF NO ARGUMENTS}
Run validation on all markdown files in the project (default behavior).
{ENDIF}

Follow the skill's workflow:
1. Determine the appropriate linting command (npx or npm scripts)
2. Execute validation on targeted or all markdown files
3. Report results (errors found or clean validation)
4. **Automatically run auto-fix** if fixable issues are detected (DO NOT ask for confirmation)
5. Report what was fixed and any remaining unfixable issues
6. Explain any rule violations found
```

**IMPORTANT**: Do NOT run linting commands directly without consulting the skill. The markdown-linting skill ensures:

- Proper command construction (npx vs npm scripts)
- Configuration compliance (respects `.markdownlint-cli2.jsonc`)
- Rule explanations and context
- Auto-fix guidance for fixable issues
- Proper error interpretation and reporting

Let the skill guide the complete workflow.

## CRITICAL: NO AUTOMATED SCRIPTS

> **⚠️ SCRIPTS ARE STRICTLY PROHIBITED FOR MARKDOWN LINTING FIXES ⚠️**

**NEVER use automated scripts to fix markdown files.** This includes:

- Python/Bash scripts that modify multiple files at once
- Regex-based find-and-replace operations across files
- Any automated tool that makes bulk changes without human review per-change

### Why This Policy Exists

**A) Scripts are dangerous - we have seen real issues:**

1. **Context blindness**: Scripts cannot understand semantic context (e.g., a code block showing tool output vs actual code)
2. **Over-application**: Scripts apply fixes uniformly, even where inappropriate
3. **Cascading damage**: One wrong assumption affects hundreds of files, requiring painful manual cleanup
4. **False language detection**: Adding `text` or other language specifiers to blocks that intentionally have none

**B) Manual fixes are slower but more accurate and safer:**

While manually fixing linting errors one-by-one takes longer, it ensures:

- Each change is reviewed in context before application
- Semantic meaning is preserved (not just syntactic correctness)
- Edge cases are handled appropriately
- No collateral damage to unrelated content

**The speed/accuracy trade-off is worth it.** A script that "saves time" but requires hours of cleanup is a net loss.

### Nested Code Blocks: A Critical Complexity

Documentation often contains **markdown within markdown** - examples showing how to write markdown, skill documentation with code samples, templates, etc. This creates nested structures that scripts cannot handle correctly:

**Example: A skill showing how to write a code block:**

`````markdown
Here's how to create a Python code block:

````markdown
```python
def hello():
    print("Hello, world!")
```
````
`````

In this example:

- The outer fence uses 4 backticks (`````markdown`)
- The inner fence uses 3 backticks (` ```python `)
- A script seeing ` ``` ` might incorrectly add language specifiers or break the nesting

**Common nested patterns to watch for:**

- ` ```{language} ` - Regular code block with syntax highlighting
- ` ````markdown ` - Wrapper showing markdown examples (uses 4+ backticks)
- Code blocks inside code blocks (documentation about documentation)
- Example output that should NOT have language specifiers

**Scripts cannot reliably distinguish:**

- Which backtick fence is the "real" one vs an example
- Whether a bare ` ``` ` is intentional (raw output) or needs a language
- The semantic purpose of each code block

### Real-World Failure Example

A script added `text` language specifiers to code blocks showing MCP tool output, Notion searches, and other non-code examples. These blocks were intentionally bare (no language) to show raw output. The script's "fix" required hundreds of manual edits to undo.

### The ONLY Acceptable Approach

1. Run `markdownlint-cli2 --fix` for safe, built-in auto-fixes (trailing spaces, blank lines)
2. For "unfixable" errors, use the **Edit tool** to make targeted, contextual fixes one at a time
3. **Review each change before applying** - understand WHY the error exists
4. **Look at surrounding context** - is this a nested code block? An example? Raw output?
5. If a fix seems mechanical/repetitive, **STOP and ask the user** before proceeding

### If You Even Consider Using a Script

1. **STOP immediately**
2. **Ask the user explicitly**: "I'm considering automating this with a script. Are you sure? Scripts have caused painful cleanup in the past."
3. **Only proceed if user explicitly confirms** AND you've triple-checked the script logic
4. **Test on ONE file first** and show the user the diff before bulk application

## Examples

### Example 1: Lint All Files

```text
User: /code-quality:lint-md

Claude: [Invokes code-quality:markdown-linting skill]
Running linting on all markdown files...

$ npm run lint:md
# or
$ npx markdownlint-cli2 "**/*.md"

All markdown files pass linting validation
```

### Example 2: Lint Specific Folder

```text
User: /code-quality:lint-md docs/

Claude: [Invokes code-quality:markdown-linting skill with targeting]
Running linting on docs/ folder...

$ npx markdownlint-cli2 "docs/**/*.md"

Found 3 linting errors in docs/setup.md:
- Line 45: MD022/blanks-around-headings
- Line 78: MD009/no-trailing-spaces
- Line 102: MD022/blanks-around-headings

Auto-fixing...
$ npx markdownlint-cli2 "docs/**/*.md" --fix
All issues fixed
```

### Example 3: Lint Specific Files

```text
User: /code-quality:lint-md README.md CLAUDE.md

Claude: [Invokes code-quality:markdown-linting skill with targeting]
Running linting on specified files...

$ npx markdownlint-cli2 README.md CLAUDE.md

README.md: No issues found
CLAUDE.md: 2 issues found (auto-fixable)
- Line 23: MD009/no-trailing-spaces
- Line 67: MD012/no-multiple-blanks

Auto-fixing...
$ npx markdownlint-cli2 README.md CLAUDE.md --fix
All issues fixed
```

### Example 4: Natural Language Targeting

```text
User: /code-quality:lint-md only the skill documentation

Claude: [Invokes code-quality:markdown-linting skill with interpretation]
Interpreting target: "only the skill documentation"
Targeting: .claude/skills/**/*.md

$ npx markdownlint-cli2 ".claude/skills/**/*.md"

Checking 9 skill files...
All skill documentation passes linting validation
```

### Example 5: Glob Pattern

```text
User: /code-quality:lint-md .claude/**/*.md

Claude: [Invokes code-quality:markdown-linting skill with pattern]
Running linting on .claude/**/*.md pattern...

$ npx markdownlint-cli2 ".claude/**/*.md"

Found issues in 2 files:
- .claude/memory/workflows.md: 1 issue (MD022)
- .claude/skills/lint-md/SKILL.md: 3 issues (MD009, MD012, MD022)

Total: 4 fixable issues

Auto-fixing...
$ npx markdownlint-cli2 ".claude/**/*.md" --fix
All issues fixed
```

## Command Design Notes

This command is designed to work with the code-quality:markdown-linting skill, which provides the actual linting logic, rule explanations, and troubleshooting guidance. This command focuses on:

- **Argument interpretation**: Parsing user-provided targeting instructions
- **Delegation**: Invoking the markdown-linting skill with context
- **Simplicity**: Minimal orchestration, maximum skill leverage

The markdown-linting skill handles:

- **Linting execution**: Running markdownlint-cli2 with correct arguments
- **Result interpretation**: Explaining errors and violations
- **Auto-fix guidance**: Offering and executing fixes
- **Configuration**: Respecting `.markdownlint-cli2.jsonc` settings
- **Troubleshooting**: Helping resolve linting issues

This separation of concerns keeps both the command and skill focused and maintainable.
