---
name: setup-aspire
description: Install the .NET Aspire CLI tool for MCP integration
allowed-tools: Bash, Read
---

# /dotnet:setup-aspire

Install the .NET Aspire CLI, required for the aspire MCP server.

## Workflow

### Step 1: Check current state

```bash
dotnet tool list -g | grep -i aspire || echo "Aspire CLI not installed"
```

### Step 2: Install

```bash
dotnet tool install --global aspire.cli
```

If already installed and needs updating:

```bash
dotnet tool update --global aspire.cli
```

### Step 3: Verify

```bash
aspire --version
```

### Step 4: Report

Tell the user to restart Claude Code so the aspire MCP server can reconnect with the now-available CLI tool.
