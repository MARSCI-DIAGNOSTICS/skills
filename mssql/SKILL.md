---
name: mssql
description: Manage MssqlMcp servers - status, rebuild, and upstream updates
argument-hint: "[status] [rebuild] [update] [--node] [--dotnet] [--check]"
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
---

# /microsoft:mssql

Manage the vendored MssqlMcp servers (Node.js and .NET). The plugin ships with pre-built servers - this skill is for diagnostics, rebuilding, and upstream updates.

## Subcommands

Parse the first positional argument from `$ARGUMENTS`:

| Subcommand | Description |
|------------|-------------|
| `status` | Check environment, verify artifacts, test connectivity (default if no args) |
| `rebuild` | Rebuild servers from existing source code |
| `update` | Pull latest from upstream GitHub and rebuild |

### Flags

| Flag | Applies to | Description |
|------|-----------|-------------|
| `--node` | `status`, `rebuild` | Only operate on Node.js server |
| `--dotnet` | `status`, `rebuild` | Only operate on .NET server |
| `--check` | `update` | Show what would change without applying |

## Subcommand: status (default)

Check environment configuration, verify build artifacts exist, and test database connectivity.

### Step 1: Check Environment Variables

```bash
echo "--- Node (Azure/cloud) ---"
echo "MSSQL_NODE_AUTH_TYPE: ${MSSQL_NODE_AUTH_TYPE:-azure-default (default)}"
echo "MSSQL_NODE_SERVER: ${MSSQL_NODE_SERVER:-localhost (default)}"
echo "MSSQL_NODE_DATABASE: ${MSSQL_NODE_DATABASE:-master (default)}"
echo "MSSQL_NODE_USER: ${MSSQL_NODE_USER:-(not set)}"
echo "MSSQL_NODE_PASSWORD: ${MSSQL_NODE_PASSWORD:+(set)}"
echo "MSSQL_NODE_ENCRYPT: ${MSSQL_NODE_ENCRYPT:-true (default)}"
echo "MSSQL_NODE_READONLY: ${MSSQL_NODE_READONLY:-true (default)}"
echo "MSSQL_NODE_TRUST_CERT: ${MSSQL_NODE_TRUST_CERT:-true (default)}"
echo ""
echo "--- .NET (local) ---"
echo "MSSQL_CONNECTION_STRING: ${MSSQL_CONNECTION_STRING:+(custom)}"
echo "MSSQL_DOTNET_SERVER: ${MSSQL_DOTNET_SERVER:-localhost (default)}"
echo "MSSQL_DOTNET_DATABASE: ${MSSQL_DOTNET_DATABASE:-master (default)}"
echo "MSSQL_DOTNET_AUTH_TYPE: ${MSSQL_DOTNET_AUTH_TYPE:-windows (default)}"
echo "MSSQL_DOTNET_READONLY: ${MSSQL_DOTNET_READONLY:-true (default)}"
```

### Step 2: Verify Build Artifacts

```bash
# Node.js - check bundle exists (single-file, no node_modules needed at runtime)
ls ${CLAUDE_PLUGIN_ROOT}/vendor/MssqlMcp/Node/bundle/index.cjs

# Node.js - check dist exists (used by bundle step)
ls ${CLAUDE_PLUGIN_ROOT}/vendor/MssqlMcp/Node/dist/index.js

# .NET - check published exe exists
ls ${CLAUDE_PLUGIN_ROOT}/vendor/MssqlMcp/dotnet-publish/MssqlMcp.exe
```

Report:

```text
Build Artifacts

  Node.js:
    bundle/index.cjs: Found (runtime entry point)
    dist/index.js: Found (used by bundle step)

  .NET:
    dotnet-publish/MssqlMcp.exe: Found (pre-built, ready to use)
```

### Step 3: Test Database Connectivity

```bash
# For LocalDB
sqlcmd -S "(localdb)\MSSQLLocalDB" -d master -Q "SELECT @@VERSION" -C

# For custom server
sqlcmd -S "${MSSQL_NODE_SERVER}" -d "${MSSQL_NODE_DATABASE}" -Q "SELECT @@VERSION" -C
```

### Step 4: Report

```text
SQL Server MCP Status

Environment:
  Server: (localdb)\MSSQLLocalDB
  Database: master
  Auth: azure-default
  Mode: Read-only

Build Status:
  mssql-node: Ready (bundle/index.cjs found)
  mssql-dotnet: Ready (dotnet-publish/MssqlMcp.exe found)

Connectivity:
  sqlcmd test: Success
  SQL Version: Microsoft SQL Server 2022 (RTM)

Status: READY
```

## Subcommand: rebuild

Rebuild servers from existing source code. Use after modifying source or fixing a corrupted build.

### Prerequisites

- **Node.js:** Node.js 18+ with npm
- **.NET:** .NET 8 SDK

### Step 1: Check Prerequisites

```bash
node --version
npm --version
dotnet --version
```

### Step 2: Build Node.js (unless --dotnet)

```bash
cd ${CLAUDE_PLUGIN_ROOT}/vendor/MssqlMcp/Node
npm install
npm run build
npm run bundle
```

Verify:

```bash
ls dist/index.js
ls bundle/index.cjs
```

### Step 3: Build .NET (unless --node)

```bash
cd ${CLAUDE_PLUGIN_ROOT}/vendor/MssqlMcp/dotnet
dotnet publish MssqlMcp/MssqlMcp.csproj -c Release -o ../dotnet-publish
```

Verify:

```bash
ls ${CLAUDE_PLUGIN_ROOT}/vendor/MssqlMcp/dotnet-publish/MssqlMcp.exe
```

### Step 4: Force-add rebuilt artifacts to git

```bash
git add -f plugins/microsoft/vendor/MssqlMcp/dotnet-publish/
git add -f plugins/microsoft/vendor/MssqlMcp/Node/bundle/
git add -f plugins/microsoft/vendor/MssqlMcp/Node/dist/
```

### Step 5: Report

```text
MssqlMcp Rebuild Complete

Node.js Server:
  Output: bundle/index.cjs (single-file bundle with all deps)

.NET Server:
  Output: dotnet-publish/MssqlMcp.exe

Artifacts re-tracked in git. Commit when ready.
```

## Subcommand: update

Pull latest from upstream Azure-Samples/SQL-AI-samples and rebuild.

> **WARNING: Local Patches Will Be Overwritten**
>
> This plugin includes local patches (documented in `vendor/MssqlMcp/PATCHES.md`). After updating, you MUST re-apply these patches.

### Step 1: Clone Upstream to Temp

```bash
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/Azure-Samples/SQL-AI-samples.git
cd SQL-AI-samples
git sparse-checkout set MssqlMcp

LATEST_COMMIT=$(git rev-parse --short HEAD)
LATEST_MESSAGE=$(git log -1 --format=%s)
```

### Step 2: Compare Versions

```bash
cd "${CLAUDE_PLUGIN_ROOT}"
CURRENT_COMMIT=$(cat plugins/microsoft/vendor/MssqlMcp/VERSION 2>/dev/null || echo "unknown")
```

Report:

```text
MssqlMcp Update Check

  Current: ${CURRENT_COMMIT}
  Upstream: ${LATEST_COMMIT} - ${LATEST_MESSAGE}
```

If `--check`, stop here.

### Step 3: Copy Files

```bash
# Backup current
mv plugins/microsoft/vendor/MssqlMcp plugins/microsoft/vendor/MssqlMcp.bak

# Copy new files (preserving build artifacts and parent .gitignore from backup)
cp -r "$TEMP_DIR/SQL-AI-samples/MssqlMcp" plugins/microsoft/vendor/
cp -r plugins/microsoft/vendor/MssqlMcp.bak/Node/dist plugins/microsoft/vendor/MssqlMcp/Node/ 2>/dev/null || true
cp -r plugins/microsoft/vendor/MssqlMcp.bak/Node/bundle plugins/microsoft/vendor/MssqlMcp/Node/ 2>/dev/null || true
cp -r plugins/microsoft/vendor/MssqlMcp.bak/Node/node_modules plugins/microsoft/vendor/MssqlMcp/Node/ 2>/dev/null || true
cp -r plugins/microsoft/vendor/MssqlMcp.bak/dotnet-publish plugins/microsoft/vendor/MssqlMcp/ 2>/dev/null || true
cp plugins/microsoft/vendor/MssqlMcp.bak/.gitignore plugins/microsoft/vendor/MssqlMcp/ 2>/dev/null || true

# Write version file
echo "${LATEST_COMMIT}" > plugins/microsoft/vendor/MssqlMcp/VERSION

# Cleanup
rm -rf plugins/microsoft/vendor/MssqlMcp.bak
rm -rf "$TEMP_DIR"
```

### Step 4: Rebuild Node.js

```bash
cd plugins/microsoft/vendor/MssqlMcp/Node
npm install
npm run build
npm run bundle
```

### Step 5: Rebuild .NET

```bash
cd plugins/microsoft/vendor/MssqlMcp/dotnet
dotnet publish MssqlMcp/MssqlMcp.csproj -c Release -o ../dotnet-publish
```

### Step 6: Re-Apply Local Patches

**IMPORTANT:** Read and re-apply patches from `PATCHES.md`:

```bash
cat plugins/microsoft/vendor/MssqlMcp/PATCHES.md
```

Current patches to re-apply:

1. **Multi-auth support** in `Node/src/index.ts`:
   - Add `AuthType` type
   - Replace `createSqlConfig()` with multi-auth factory
   - Update `ensureSqlConnection()` for SQL auth

After re-applying, rebuild:

```bash
cd plugins/microsoft/vendor/MssqlMcp/Node
npm run build && npm run bundle
```

### Step 7: Force-add and Report

```bash
git add -f plugins/microsoft/vendor/MssqlMcp/dotnet-publish/
git add -f plugins/microsoft/vendor/MssqlMcp/Node/bundle/
git add -f plugins/microsoft/vendor/MssqlMcp/Node/dist/
git status --short plugins/microsoft/vendor/MssqlMcp/
```

## Examples

```bash
# Check status (default)
/microsoft:mssql

# Check status of Node.js server only
/microsoft:mssql status --node

# Rebuild both servers
/microsoft:mssql rebuild

# Rebuild only .NET server
/microsoft:mssql rebuild --dotnet

# Check for upstream updates (dry run)
/microsoft:mssql update --check

# Pull upstream and rebuild
/microsoft:mssql update
```

## Troubleshooting

**Node.js build fails:**

```text
Common issues:
  1. Old Node.js version - upgrade to 18+
  2. Corrupted node_modules - delete and retry
  3. npm cache issues - npm cache clean --force
  4. zod/TypeScript incompatibility - pin @modelcontextprotocol/sdk to 1.x
```

**.NET build fails:**

```text
Common issues:
  1. Wrong SDK version - install .NET 8
  2. Missing workloads - dotnet workload restore
  3. NuGet cache issues - dotnet nuget locals all --clear
```

## Upstream Source

- Repository: <https://github.com/Azure-Samples/SQL-AI-samples>
- Path: MssqlMcp/
- License: MIT

## Related Commands

- `/microsoft:setup-dab` - Install and configure Data API Builder
