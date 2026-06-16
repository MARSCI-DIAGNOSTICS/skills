# LSP Troubleshooting Guide

Common LSP issues and their solutions.

## ⚠️ CRITICAL: Claude Code LSP Status (January 2026)

**LSP support in Claude Code is experimental and has known issues.** Before troubleshooting, be aware of the current state.

### Environment Variable Required

To expose the LSP tool to Claude, you **MUST** set:

```bash
# Enable LSP tool visibility (singular, not plural)
ENABLE_LSP_TOOL=1 claude
```

**Note:** The variable is `ENABLE_LSP_TOOL` (singular), NOT `ENABLE_LSP_TOOLS`.

### Known Issues by Version

> **Issue Status Verification:** GitHub issue status may change. Verify current status via the `claude-code-issue-researcher` agent or directly at [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues).

| Version | Status | Notes |
|---------|--------|-------|
| v2.0.67 | ✅ Working | Last known stable LSP version |
| v2.0.69-2.0.76 | ❌ Broken | Race condition: LSP Manager init before plugins (#13952) |
| v2.1.0+ | ⚠️ Partial | Race condition fixed, but new regression (#17468) |

### Current Regressions (v2.1.0+)

**GitHub Issue #17468 (OPEN):** Starting Claude Code with `ENABLE_LSP_TOOL=1` no longer exposes the LSP tool in v2.1.0+. This worked in v2.0.76.

**Workaround:** If you need working LSP, consider downgrading:

```bash
npx @anthropic-ai/claude-code@2.0.67
```

### Platform-Specific Issues

| Platform | Issue # | Status | Summary |
|----------|---------|--------|---------|
| Windows | #15914, #16084, #17312 | OPEN | LSP plugins not loading |
| macOS | #16291, #17468 | OPEN | TypeScript LSP, tool visibility |
| Linux/NixOS | #16080 | OPEN | LSP discovery (FHS path assumptions) |

**Windows-specific workaround:** Use `cclsp` MCP server with `cmd /c` wrapper to resolve `.cmd` extension issues.

### Checking Debug Logs

```bash
# Check LSP Manager timing
cat ~/.claude/debug/latest | grep -i lsp

# Look for race condition symptoms:
# - "LSP notification handlers registered for all 0 server(s)"
# - Plugin loading AFTER LSP Manager init
```

## Quick Diagnosis

### 1. Check Server Is Running

```bash
# List running language server processes
# Windows PowerShell
Get-Process | Where-Object { $_.ProcessName -match "langserver|lsp|pyright|gopls|rust-analyzer" }

# macOS/Linux
ps aux | grep -E "langserver|lsp|pyright|gopls|rust-analyzer"
```

### 2. Check Server Installation

```bash
# Test command directly
pyright-langserver --version
typescript-language-server --version
gopls version
rust-analyzer --version
csharp-ls --version
```

### 3. Validate .lsp.json

```bash
# Check JSON syntax
cat .lsp.json | python -m json.tool
```

## Common Issues

### Server Not Starting

**Symptoms:**

- No hover information
- No go-to-definition
- No diagnostics

**Solutions:**

1. **Check command path**

   ```bash
   # Find where the command is
   which pyright-langserver  # macOS/Linux
   where pyright-langserver  # Windows
   ```

2. **Verify installation**

   ```bash
   npm list -g pyright
   ```

3. **Check .lsp.json syntax**

   - Ensure valid JSON
   - Check for typos in command name
   - Verify args array is correct

4. **Restart Claude Code**

   - Exit and restart Claude Code session
   - LSP servers start on session init

### Hover Not Working

**Symptoms:**

- Server starts but hover shows no information
- Other features work (diagnostics, go-to-definition)

**Solutions:**

1. **Python/Pyright specific:**

   Create `pyrightconfig.json`:

   ```json
   {
     "venvPath": ".",
     "venv": ".venv",
     "pythonVersion": "3.13"
   }
   ```

2. **TypeScript specific:**

   Ensure `tsconfig.json` exists and includes the file.

3. **Check file is in project scope:**

   - File must be within project directory
   - Check for exclude patterns in config

### Diagnostics Missing

**Symptoms:**

- No squiggly underlines for errors
- Build fails but LSP doesn't show issues

**Solutions:**

1. **Check language ID mapping:**

   ```json
   "extensionToLanguage": {
     ".py": "python"  // Must match language ID exactly
   }
   ```

2. **Verify file type detection:**

   - Check file extension is mapped
   - Try renaming file to standard extension

3. **Project configuration:**

   - Python: Check `pyrightconfig.json`
   - TypeScript: Check `tsconfig.json`
   - C/C++: Check `compile_commands.json`

### Server Crashes Repeatedly

**Symptoms:**

- LSP works briefly then stops
- Features intermittently available

**Solutions:**

1. **Increase maxRestarts:**

   ```json
   {
     "pyright": {
       "restartOnCrash": true,
       "maxRestarts": 5
     }
   }
   ```

2. **Check server logs:**

   - Look for error messages in console
   - Check server-specific log files

3. **Update server:**

   ```bash
   npm update -g pyright
   npm update -g typescript-language-server
   ```

4. **Check memory usage:**

   - Large projects may exhaust memory
   - Consider increasing Node.js memory limit

### Go-to-Definition Not Working

**Symptoms:**

- Can't navigate to definitions
- Works for some files but not others

**Solutions:**

1. **Check project structure:**

   - Ensure proper package.json/go.mod/Cargo.toml exists
   - Verify file is part of the project

2. **Indexing may be in progress:**

   - Wait for initial indexing to complete
   - Large projects take longer

3. **External dependencies:**

   - Install dependencies first (`npm install`, `pip install -r requirements.txt`)
   - LSP needs type information from dependencies

### Wrong Language Server Used

**Symptoms:**

- Getting TypeScript errors in JavaScript files
- Wrong language features

**Solutions:**

1. **Check extensionToLanguage mapping:**

   ```json
   {
     "extensionToLanguage": {
       ".js": "javascript",   // Not "typescript"
       ".ts": "typescript"
     }
   }
   ```

2. **Multiple servers configured:**

   - Only one server per language ID
   - Remove conflicting configurations

### PATH Issues

**Symptoms:**

- Server works in terminal but not in Claude Code
- "Command not found" type errors

**Solutions:**

1. **Check PATH inheritance:**

   ```bash
   # Print current PATH
   echo $PATH
   ```

2. **Use absolute paths (temporary fix):**

   ```json
   {
     "pyright": {
       "command": "/usr/local/bin/pyright-langserver"
     }
   }
   ```

3. **Restart shell/terminal:**

   - New PATH entries may not be picked up
   - Start new terminal session

### Windows-Specific Issues

**Symptoms:**

- Server works on macOS/Linux but not Windows
- Path-related errors

**Solutions:**

1. **Check executable extension:**

   ```json
   {
     "pyright": {
       "command": "pyright-langserver.cmd"  // May need .cmd on Windows
     }
   }
   ```

2. **Use forward slashes in paths:**

   ```json
   {
     "command": "C:/Users/name/.npm/pyright-langserver"
   }
   ```

3. **Check npm global path:**

   ```bash
   npm config get prefix
   # Add to PATH: %prefix%\node_modules\.bin
   ```

## Language-Specific Troubleshooting

### Python (Pyright)

**Virtual Environment Issues:**

```json
// pyrightconfig.json
{
  "venvPath": ".",
  "venv": ".venv"
}
```

**Type Checking Too Strict:**

```json
// pyrightconfig.json
{
  "typeCheckingMode": "basic"  // or "off"
}
```

### TypeScript

**Project Not Recognized:**

Ensure `tsconfig.json` exists with proper includes:

```json
{
  "include": ["src/**/*"],
  "compilerOptions": {
    "strict": true
  }
}
```

### Go (gopls)

**Module Issues:**

```bash
# Initialize module
go mod init myproject

# Download dependencies
go mod tidy
```

### Rust (rust-analyzer)

**Cargo.toml Issues:**

- Ensure valid Cargo.toml exists
- Run `cargo check` to verify project builds

### C# (csharp-ls)

**Solution Issues:**

- Ensure .sln or .csproj file exists
- Run `dotnet restore` first

### C/C++ (clangd)

**compile_commands.json Missing:**

```bash
# CMake
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON build/

# Bear (for Make)
bear -- make
```

## Performance Issues

### Slow Initial Load

**Causes:**

- Large codebase indexing
- Many dependencies

**Solutions:**

1. **Add ignore patterns** to language-specific config
2. **Increase server memory** where possible
3. **Wait for initial indexing** to complete

### High CPU Usage

**Causes:**

- Continuous re-indexing
- File watcher issues

**Solutions:**

1. **Check for file change loops** (build artifacts)
2. **Add ignore patterns** for generated files
3. **Update to latest server version**

## Debugging Steps

### 1. Minimal Configuration

Start with single server:

```json
{
  "pyright": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python"
    }
  }
}
```

### 2. Test Server Manually

```bash
# Run server directly
pyright-langserver --stdio

# Should wait for input (JSON-RPC messages)
```

### 3. Verify File Type Detection

Create simple test file and check if features work.

### 4. Check Claude Code Logs

Look for LSP-related error messages in console output.

## When to Report Issues

Report to Claude Code GitHub if:

- Server works in other editors but not Claude Code
- Consistent crashes with specific file patterns
- Features work initially then stop

Include:

- `.lsp.json` configuration
- Server version
- OS and Claude Code version
- Minimal reproduction steps

---

**Last Updated:** 2026-01-11
