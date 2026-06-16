# LSP Server Installation Guide

Per-server installation commands for all recommended LSP servers.

## Prerequisites

Ensure you have the appropriate package managers installed:

| Package Manager | For Languages | Installation |
| --- | --- | --- |
| npm | Node.js-based servers | Comes with Node.js |
| pip | Python servers | Comes with Python |
| go | Go tools | <https://go.dev/dl/> |
| cargo | Rust tools | <https://rustup.rs/> |
| gem | Ruby tools | Comes with Ruby |
| dotnet | .NET tools | <https://dot.net/download> |

## Python

### Pyright (Recommended)

```bash
# npm (recommended)
npm install -g pyright

# Verify installation
pyright-langserver --version
```

**Configuration:**

```json
{
  "pyright": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    }
  }
}
```

#### Optional: pyrightconfig.json

Create `pyrightconfig.json` in project root for better analysis:

```json
{
  "venvPath": ".",
  "venv": ".venv",
  "pythonVersion": "3.13"
}
```

### Pylsp (Alternative)

```bash
# pip
pip install python-lsp-server

# Verify installation
pylsp --version
```

### Ruff (Linting)

```bash
# pip
pip install ruff

# Verify installation
ruff --version
```

## TypeScript / JavaScript

### typescript-language-server (Recommended)

```bash
# npm
npm install -g typescript typescript-language-server

# Verify installation
typescript-language-server --version
```

**Configuration:**

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
  }
}
```

### vtsls (Alternative)

```bash
# npm
npm install -g @vtsls/language-server

# Verify installation
vtsls --version
```

## Go

### gopls (Recommended)

```bash
# go install
go install golang.org/x/tools/gopls@latest

# Verify installation
gopls version
```

**Configuration:**

```json
{
  "gopls": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Note:** Ensure `$GOPATH/bin` is in your PATH.

## Rust

### rust-analyzer (Recommended)

```bash
# rustup (recommended)
rustup component add rust-analyzer

# Verify installation
rust-analyzer --version
```

**Configuration:**

```json
{
  "rust-analyzer": {
    "command": "rust-analyzer",
    "args": [],
    "extensionToLanguage": {
      ".rs": "rust"
    }
  }
}
```

**Alternative installation (standalone):**

```bash
# macOS
brew install rust-analyzer

# Windows
scoop install rust-analyzer

# Linux
# Download from https://github.com/rust-lang/rust-analyzer/releases
```

## C\#

### csharp-ls (Recommended)

```bash
# dotnet tool
dotnet tool install -g csharp-ls

# Verify installation
csharp-ls --version
```

**Configuration:**

```json
{
  "csharp": {
    "command": "csharp-ls",
    "args": [],
    "extensionToLanguage": {
      ".cs": "csharp",
      ".csx": "csharp"
    }
  }
}
```

**Note:** Ensure `~/.dotnet/tools` is in your PATH.

### OmniSharp (Alternative)

Download from <https://github.com/OmniSharp/omnisharp-roslyn/releases>

```bash
# Verify installation
OmniSharp --version
```

## C / C++

### clangd (Recommended)

```bash
# macOS
brew install llvm

# Windows
scoop install llvm

# Ubuntu/Debian
sudo apt install clangd

# Verify installation
clangd --version
```

**Configuration:**

```json
{
  "clangd": {
    "command": "clangd",
    "args": ["--background-index"],
    "extensionToLanguage": {
      ".c": "c",
      ".h": "c",
      ".cpp": "cpp",
      ".hpp": "cpp"
    }
  }
}
```

**Tip:** Create `compile_commands.json` for accurate analysis:

```bash
# CMake projects
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .

# Meson projects
meson setup builddir

# Bear (for make projects)
bear -- make
```

### ccls (Alternative)

```bash
# macOS
brew install ccls

# Ubuntu
sudo apt install ccls
```

## Java

### Eclipse JDTLS

Download from <https://download.eclipse.org/jdtls/snapshots/>

**Setup:**

1. Extract to a permanent location (e.g., `~/.local/share/jdtls`)
2. Create a wrapper script

```bash
#!/bin/bash
java \
  -Declipse.application=org.eclipse.jdt.ls.core.id1 \
  -Dosgi.bundles.defaultStartLevel=4 \
  -Declipse.product=org.eclipse.jdt.ls.core.product \
  -jar ~/.local/share/jdtls/plugins/org.eclipse.equinox.launcher_*.jar \
  -configuration ~/.local/share/jdtls/config_linux \
  -data ~/.cache/jdtls-workspace \
  --add-modules=ALL-SYSTEM \
  --add-opens java.base/java.util=ALL-UNNAMED \
  --add-opens java.base/java.lang=ALL-UNNAMED
```

## Ruby

### Solargraph (Recommended)

```bash
# gem
gem install solargraph

# Verify installation
solargraph --version
```

**Configuration:**

```json
{
  "solargraph": {
    "command": "solargraph",
    "args": ["stdio"],
    "extensionToLanguage": {
      ".rb": "ruby"
    }
  }
}
```

## PHP

### Intelephense (Recommended)

```bash
# npm
npm install -g intelephense

# Verify installation
intelephense --version
```

**Configuration:**

```json
{
  "intelephense": {
    "command": "intelephense",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".php": "php"
    }
  }
}
```

### phpactor (Alternative)

```bash
# composer
composer global require phpactor/phpactor
```

## Lua

### lua-language-server

```bash
# macOS
brew install lua-language-server

# Windows
scoop install lua-language-server

# Linux - download from releases
# https://github.com/LuaLS/lua-language-server/releases
```

**Configuration:**

```json
{
  "lua": {
    "command": "lua-language-server",
    "args": [],
    "extensionToLanguage": {
      ".lua": "lua"
    }
  }
}
```

## YAML

### yaml-language-server

```bash
# npm
npm install -g yaml-language-server

# Verify installation
yaml-language-server --version
```

**Configuration:**

```json
{
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

## JSON

### vscode-json-languageserver

```bash
# npm
npm install -g vscode-langservers-extracted

# Verify installation
vscode-json-language-server --version
```

**Configuration:**

```json
{
  "json": {
    "command": "vscode-json-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".json": "json",
      ".jsonc": "jsonc"
    }
  }
}
```

## Bash / Shell

### bash-language-server

```bash
# npm
npm install -g bash-language-server

# Verify installation
bash-language-server --version
```

**Configuration:**

```json
{
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

## Verification Checklist

After installing an LSP server:

1. **Command runs** - Execute the command manually
2. **PATH is correct** - Server is accessible from terminal
3. **Dependencies met** - Runtime/compiler available
4. **Claude Code restart** - Restart to pick up new configuration

---

**Last Updated:** 2026-01-11
