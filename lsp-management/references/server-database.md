# LSP Server Database

Curated recommendations for Language Server Protocol servers, organized by language/technology.

## Selection Criteria

Servers are recommended based on:

1. **Stability** - Production-ready, actively maintained
2. **Performance** - Fast startup, responsive diagnostics
3. **Feature coverage** - Hover, go-to-definition, find-references, diagnostics
4. **Cross-platform** - Works on Windows, macOS, Linux
5. **Ease of installation** - Available via standard package managers

## Python

### Recommended: Pyright

| Attribute | Value |
| --- | --- |
| **Package** | `pyright` (npm) |
| **Command** | `pyright-langserver --stdio` |
| **Website** | <https://github.com/microsoft/pyright> |
| **Strengths** | Fast, accurate type checking, Microsoft-backed |
| **Best for** | Type-annotated Python, large codebases |

### Alternative: Pylsp

| Attribute | Value |
| --- | --- |
| **Package** | `python-lsp-server` (pip) |
| **Command** | `pylsp` |
| **Website** | <https://github.com/python-lsp/python-lsp-server> |
| **Strengths** | Plugin ecosystem, configurable |
| **Best for** | Dynamic Python, custom linting integration |

### Alternative: Ruff

| Attribute | Value |
| --- | --- |
| **Package** | `ruff` (pip/cargo) |
| **Command** | `ruff server --preview` |
| **Website** | <https://github.com/astral-sh/ruff> |
| **Strengths** | Extremely fast linting, Rust-based |
| **Best for** | Linting-focused workflows, CI integration |

## TypeScript / JavaScript

### Recommended: typescript-language-server

| Attribute | Value |
| --- | --- |
| **Package** | `typescript-language-server` (npm) |
| **Command** | `typescript-language-server --stdio` |
| **Website** | <https://github.com/typescript-language-server/typescript-language-server> |
| **Strengths** | Official TypeScript support, widely adopted |
| **Best for** | Most TypeScript/JavaScript projects |

### Alternative: vtsls

| Attribute | Value |
| --- | --- |
| **Package** | `@vtsls/language-server` (npm) |
| **Command** | `vtsls --stdio` |
| **Website** | <https://github.com/yioneko/vtsls> |
| **Strengths** | Faster startup, VS Code parity |
| **Best for** | Large monorepos, performance-critical |

## Go

### Recommended: gopls

| Attribute | Value |
| --- | --- |
| **Package** | `golang.org/x/tools/gopls` (go install) |
| **Command** | `gopls` |
| **Website** | <https://pkg.go.dev/golang.org/x/tools/gopls> |
| **Strengths** | Official Go team, comprehensive features |
| **Best for** | All Go projects |

## Rust

### Recommended: rust-analyzer

| Attribute | Value |
| --- | --- |
| **Package** | `rust-analyzer` (rustup component) |
| **Command** | `rust-analyzer` |
| **Website** | <https://rust-analyzer.github.io/> |
| **Strengths** | De facto standard, excellent performance |
| **Best for** | All Rust projects |

## C\#

### Recommended: csharp-ls

| Attribute | Value |
| --- | --- |
| **Package** | `csharp-ls` (dotnet tool) |
| **Command** | `csharp-ls` |
| **Website** | <https://github.com/razzmatazz/csharp-language-server> |
| **Strengths** | Lightweight, cross-platform, dotnet tool |
| **Best for** | Most C# projects, especially cross-platform |

### Alternative: OmniSharp

| Attribute | Value |
| --- | --- |
| **Package** | OmniSharp release binaries |
| **Command** | `OmniSharp -lsp` |
| **Website** | <https://github.com/OmniSharp/omnisharp-roslyn> |
| **Strengths** | Full Roslyn integration, mature |
| **Best for** | Complex solutions, Unity projects |

## C / C++

### Recommended: clangd

| Attribute | Value |
| --- | --- |
| **Package** | LLVM/Clang distribution |
| **Command** | `clangd` |
| **Website** | <https://clangd.llvm.org/> |
| **Strengths** | LLVM-backed, fast, accurate |
| **Best for** | Most C/C++ projects |

### Alternative: ccls

| Attribute | Value |
| --- | --- |
| **Package** | `ccls` (package manager) |
| **Command** | `ccls` |
| **Website** | <https://github.com/MaskRay/ccls> |
| **Strengths** | Fast indexing, cross-references |
| **Best for** | Large C++ codebases |

## Java

### Recommended: Eclipse JDTLS

| Attribute | Value |
| --- | --- |
| **Package** | Eclipse JDT Language Server (download) |
| **Command** | `jdtls` (wrapper script) |
| **Website** | <https://github.com/eclipse-jdtls/eclipse.jdt.ls> |
| **Strengths** | Full-featured, widely supported |
| **Best for** | All Java projects |

## Ruby

### Recommended: Solargraph

| Attribute | Value |
| --- | --- |
| **Package** | `solargraph` (gem) |
| **Command** | `solargraph stdio` |
| **Website** | <https://solargraph.org/> |
| **Strengths** | Type inference, documentation |
| **Best for** | Most Ruby projects |

## PHP

### Recommended: Intelephense

| Attribute | Value |
| --- | --- |
| **Package** | `intelephense` (npm) |
| **Command** | `intelephense --stdio` |
| **Website** | <https://intelephense.com/> |
| **Strengths** | Fast, premium features available |
| **Best for** | Most PHP projects |

### Alternative: phpactor

| Attribute | Value |
| --- | --- |
| **Package** | `phpactor` (composer) |
| **Command** | `phpactor language-server` |
| **Website** | <https://phpactor.readthedocs.io/> |
| **Strengths** | Open source, refactoring focus |
| **Best for** | Refactoring-heavy workflows |

## Lua

### Recommended: lua-language-server

| Attribute | Value |
| --- | --- |
| **Package** | Binary download or package manager |
| **Command** | `lua-language-server` |
| **Website** | <https://github.com/LuaLS/lua-language-server> |
| **Strengths** | Official, well-maintained |
| **Best for** | All Lua projects |

## YAML

### Recommended: yaml-language-server

| Attribute | Value |
| --- | --- |
| **Package** | `yaml-language-server` (npm) |
| **Command** | `yaml-language-server --stdio` |
| **Website** | <https://github.com/redhat-developer/yaml-language-server> |
| **Strengths** | Schema validation, completion |
| **Best for** | YAML configuration files |

## JSON

### Recommended: vscode-json-languageserver

| Attribute | Value |
| --- | --- |
| **Package** | `vscode-langservers-extracted` (npm) |
| **Command** | `vscode-json-language-server --stdio` |
| **Website** | <https://github.com/microsoft/vscode> |
| **Strengths** | Schema validation, formatting |
| **Best for** | JSON configuration files |

## Markdown

### Recommended: marksman

| Attribute | Value |
| --- | --- |
| **Package** | Binary download |
| **Command** | `marksman server` |
| **Website** | <https://github.com/artempyanykh/marksman> |
| **Strengths** | Wiki-links, references, TOC |
| **Best for** | Documentation projects |

## Bash / Shell

### Recommended: bash-language-server

| Attribute | Value |
| --- | --- |
| **Package** | `bash-language-server` (npm) |
| **Command** | `bash-language-server start` |
| **Website** | <https://github.com/bash-lsp/bash-language-server> |
| **Strengths** | ShellCheck integration |
| **Best for** | Shell script projects |

## Quick Comparison Table

| Language | Primary | Alternative | Notes |
| --- | --- | --- | --- |
| Python | Pyright | Pylsp, Ruff | Pyright for types, Ruff for linting |
| TypeScript/JS | typescript-language-server | vtsls | vtsls for large projects |
| Go | gopls | - | No real alternative needed |
| Rust | rust-analyzer | - | De facto standard |
| C# | csharp-ls | OmniSharp | csharp-ls simpler to install |
| C/C++ | clangd | ccls | clangd preferred |
| Java | jdtls | - | Complex setup |
| Ruby | solargraph | - | Standard choice |
| PHP | intelephense | phpactor | intelephense more features |
| Lua | lua-language-server | - | Standard choice |
| YAML | yaml-language-server | - | Standard choice |
| JSON | vscode-json-languageserver | - | Standard choice |

---

**Last Updated:** 2026-01-11
