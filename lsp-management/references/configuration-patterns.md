# LSP Configuration Patterns

Common `.lsp.json` configuration patterns for Claude Code.

## File Location

Place `.lsp.json` in your project root directory. Claude Code reads this file on startup.

## Basic Structure

```json
{
  "server-name": {
    "command": "executable",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ext": "language-id"
    }
  }
}
```

## Complete Field Reference

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `command` | string | Yes | - | Server executable command |
| `args` | string[] | Yes | - | Command arguments |
| `extensionToLanguage` | object | Yes | - | File extension to language ID mapping |
| `restartOnCrash` | boolean | No | `true` | Auto-restart on crash |
| `maxRestarts` | number | No | `3` | Max restart attempts |

## Single Language Configuration

### Python with Pyright

```json
{
  "pyright": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

### TypeScript/JavaScript

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

### Go

```json
{
  "gopls": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go",
      ".mod": "go.mod",
      ".sum": "go.sum"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

### Rust

```json
{
  "rust-analyzer": {
    "command": "rust-analyzer",
    "args": [],
    "extensionToLanguage": {
      ".rs": "rust"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

### C\#

```json
{
  "csharp": {
    "command": "csharp-ls",
    "args": [],
    "extensionToLanguage": {
      ".cs": "csharp",
      ".csx": "csharp"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

### C/C++

```json
{
  "clangd": {
    "command": "clangd",
    "args": ["--background-index"],
    "extensionToLanguage": {
      ".c": "c",
      ".h": "c",
      ".cpp": "cpp",
      ".hpp": "cpp",
      ".cc": "cpp",
      ".cxx": "cpp"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

## Multi-Language Configuration

### Web Development Stack

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact"
    }
  },
  "json": {
    "command": "vscode-json-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".json": "json",
      ".jsonc": "jsonc"
    }
  },
  "yaml": {
    "command": "yaml-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".yaml": "yaml",
      ".yml": "yaml"
    }
  }
}
```

### Full-Stack .NET

```json
{
  "csharp": {
    "command": "csharp-ls",
    "args": [],
    "extensionToLanguage": {
      ".cs": "csharp",
      ".csx": "csharp"
    }
  },
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    }
  },
  "json": {
    "command": "vscode-json-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".json": "json"
    }
  }
}
```

### Python Data Science

```json
{
  "pyright": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    }
  },
  "yaml": {
    "command": "yaml-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".yaml": "yaml",
      ".yml": "yaml"
    }
  },
  "json": {
    "command": "vscode-json-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".json": "json"
    }
  }
}
```

### DevOps / Infrastructure

```json
{
  "yaml": {
    "command": "yaml-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".yaml": "yaml",
      ".yml": "yaml"
    }
  },
  "json": {
    "command": "vscode-json-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".json": "json"
    }
  },
  "bash": {
    "command": "bash-language-server",
    "args": ["start"],
    "extensionToLanguage": {
      ".sh": "shellscript",
      ".bash": "shellscript"
    }
  }
}
```

## Language ID Reference

Common language IDs used in `extensionToLanguage`:

| Language | ID | Extensions |
| --- | --- | --- |
| Python | `python` | `.py`, `.pyi` |
| TypeScript | `typescript` | `.ts` |
| TypeScript React | `typescriptreact` | `.tsx` |
| JavaScript | `javascript` | `.js` |
| JavaScript React | `javascriptreact` | `.jsx` |
| Go | `go` | `.go` |
| Rust | `rust` | `.rs` |
| C# | `csharp` | `.cs`, `.csx` |
| C | `c` | `.c`, `.h` |
| C++ | `cpp` | `.cpp`, `.hpp`, `.cc`, `.cxx` |
| Java | `java` | `.java` |
| Ruby | `ruby` | `.rb` |
| PHP | `php` | `.php` |
| Lua | `lua` | `.lua` |
| YAML | `yaml` | `.yaml`, `.yml` |
| JSON | `json` | `.json` |
| JSONC | `jsonc` | `.jsonc` |
| Markdown | `markdown` | `.md` |
| Shell | `shellscript` | `.sh`, `.bash` |

## Best Practices

### 1. Always Include restartOnCrash

```json
{
  "restartOnCrash": true,
  "maxRestarts": 3
}
```

This ensures LSP servers recover from crashes gracefully.

### 2. Use --stdio Transport

Most LSP servers support `--stdio` transport. This is the most reliable option:

```json
{
  "args": ["--stdio"]
}
```

### 3. Map All Related Extensions

Include all file extensions the language uses:

```json
{
  "extensionToLanguage": {
    ".ts": "typescript",
    ".tsx": "typescriptreact",
    ".mts": "typescript",
    ".cts": "typescript"
  }
}
```

### 4. Use Consistent Server Names

Use descriptive, consistent names for servers:

- ✅ `"pyright"`, `"typescript"`, `"gopls"`
- ❌ `"server1"`, `"lsp"`, `"python-server"`

## Validation

Before using your `.lsp.json`:

1. **Validate JSON syntax** - Use a JSON linter
2. **Verify server installation** - Run command manually to confirm it works
3. **Test file extension mapping** - Open files with each extension
4. **Check Claude Code logs** - Look for LSP initialization messages

---

## Project-Level Configuration Files

**CRITICAL DISTINCTION:** There are TWO levels of LSP configuration:

| Config Type | Purpose | Example |
| --- | --- | --- |
| `.lsp.json` | How to START the LSP server | `{ "pyright": { "command": "pyright-langserver" } }` |
| Project config | How LSP server ANALYZES code | `pyrightconfig.json`, `tsconfig.json` |

**Symptom:** If diagnostics work but hover/goToDefinition/documentSymbol don't → **Missing project config**

### Required Project Configs by Language

| Language | Project Config | Purpose |
| --- | --- | --- |
| Python | `pyrightconfig.json` or `[tool.pyright]` in `pyproject.toml` | Defines include/exclude paths, Python version, type checking mode |
| TypeScript | `tsconfig.json` | Defines compiler options, module resolution, target |
| C# | `*.sln` or `*.csproj` | Defines project root for csharp-ls |
| Go | `go.mod` | Defines module path and dependencies |
| Rust | `Cargo.toml` | Defines package and dependencies |

### Python: pyrightconfig.json

```json
{
  "include": ["src", "plugins"],
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    "**/.venv",
    "**/.mypy_cache",
    "**/dist"
  ],
  "venvPath": ".",
  "venv": ".venv",
  "typeCheckingMode": "standard",
  "pythonVersion": "3.13",
  "pythonPlatform": "All",
  "strictListInference": true,
  "strictSetInference": true,
  "reportMissingImports": "warning",
  "reportMissingTypeStubs": "warning",
  "reportUnusedImport": "warning",
  "reportUnusedVariable": "warning"
}
```

**Key Settings:**

| Setting | Values | Recommendation |
| --- | --- | --- |
| `typeCheckingMode` | `"off"`, `"basic"`, `"standard"`, `"strict"`, `"all"` | Use `"standard"` for balance |
| `pythonVersion` | `"3.11"`, `"3.12"`, `"3.13"`, `"3.14"` | Check current stable (3.13 as of Jan 2026) |
| `venvPath` + `venv` | Path to virtual environment | Required for import resolution |

### TypeScript: tsconfig.json

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2024"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src/**/*.ts", "plugins/**/*.ts"],
  "exclude": ["node_modules", "dist", "**/node_modules"]
}
```

**Key Settings:**

| Setting | Current Best Practice | Notes |
| --- | --- | --- |
| `module/moduleResolution` | `"NodeNext"` | Recommended for modern Node.js ESM |
| `target` | `"ES2022"` | Current baseline |
| `lib` | `["ES2024"]` | Latest runtime features |
| `strict` | `true` | Enable all strict checks |

### C#: Solution File for Root Detection

csharp-ls requires a `.sln` or `.csproj` for project root detection. Minimal placeholder:

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

**Requirements:**

| Component | Version (Jan 2026) |
| --- | --- |
| .NET SDK | 10.0 LTS |
| C# | 14 (default with .NET 10) |
| csharp-ls | Requires .NET 10 SDK |

### Version Reference (MCP-Validated Jan 2026)

Always verify current versions using MCP servers before generating configs:

| Technology | Current Stable | Query |
| --- | --- | --- |
| Python | 3.13 | `perplexity: "Python stable version January 2026"` |
| TypeScript | 5.9 | `perplexity: "TypeScript current version 2026"` |
| .NET SDK | 10.0 LTS | `perplexity: ".NET SDK latest LTS 2026"` |
| pyright | 1.1.407+ | `pyright-langserver --version` |

### Troubleshooting Semantic Features

| Symptom | Cause | Solution |
| --- | --- | --- |
| Diagnostics work, hover doesn't | Missing project config | Create pyrightconfig.json/tsconfig.json |
| No symbols in document | Server not indexed | Restart Claude Code, wait for indexing |
| goToDefinition fails | Include paths wrong | Check `include`/`exclude` in project config |
| Imports unresolved | venv not configured | Set `venvPath` + `venv` in pyrightconfig.json |

### Environment Requirements

```bash
# Required for Claude Code LSP tool access
export ENABLE_LSP_TOOL=1
```

---

**Last Updated:** 2026-01-11
