---
name: setup-dab
description: Install and configure Data API Builder (DAB) for production SQL Server MCP access with RBAC
argument-hint: "[--init] [--add <entity>] [--verify]"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# /microsoft:setup-dab

Install and configure Microsoft Data API Builder (DAB) for production-ready SQL Server MCP integration.

## Overview

Data API Builder (DAB) provides a production-grade MCP server for SQL Server with:

- **RBAC**: Role-based access control for entities
- **Caching**: Automatic result caching
- **Telemetry**: Built-in observability
- **Deterministic queries**: NL2DAB instead of fragile NL2SQL

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--init` | Initialize new DAB configuration | false |
| `--add <entity>` | Add entity to configuration | (none) |
| `--verify` | Verify existing setup | false |

## Prerequisites

- .NET 8 SDK or later
- SQL Server database with accessible connection string
- Tables/views to expose as entities

## Workflow

### Step 1: Check DAB Installation

```bash
# Check if DAB is installed globally
dotnet tool list -g | grep -i dataapibuilder

# Check version
dab --version
```

If not installed:

```text
Data API Builder not found.

Installing DAB globally...
  dotnet tool install -g microsoft.dataapibuilder --prerelease

Note: Using --prerelease for latest MCP features.
```

Install command:

```bash
dotnet tool install -g microsoft.dataapibuilder --prerelease
```

### Step 2: Initialize Configuration (--init)

If `--init` specified or no dab-config.json exists:

```text
DAB Configuration Wizard

Data API Builder requires entity configuration for security.
Unlike raw SQL access, DAB only exposes pre-approved entities.

Connection String Setup
-----------------------
Enter your SQL Server connection string (will be stored as env var reference):
```

Use AskUserQuestion to get connection string approach:

```text
How do you want to configure the connection string?

Options:
1. Environment variable (Recommended) - Reference $DAB_CONNECTION_STRING
2. Direct entry - Store in dab-config.json (less secure)
```

Initialize with environment variable:

```bash
dab init --database-type mssql --connection-string "@env('DAB_CONNECTION_STRING')" --config dab-config.json
```

### Step 3: Add Entities

Prompt user to add entities:

```text
Entity Configuration
--------------------
DAB requires explicit entity definitions for each table/view you want to expose.

Would you like to:
1. Add an entity now
2. Skip (configure later)
```

If adding entity:

```text
Entity Details

  Table/View name (e.g., dbo.Products):
  Entity name (e.g., Products):
  Permissions:
    - anonymous:read (read-only, no auth)
    - anonymous:* (full access, no auth)
    - authenticated:read (read-only, requires auth)
    - authenticated:* (full access, requires auth)
```

Add entity command:

```bash
# Read-only access
dab add Products --source dbo.Products --permissions "anonymous:read"

# Full CRUD access
dab add Products --source dbo.Products --permissions "anonymous:*"

# With specific operations
dab add Products --source dbo.Products --permissions "anonymous:read,create"
```

### Step 4: Verify Configuration (--verify)

If `--verify` specified:

```bash
# Check config file
cat dab-config.json

# Validate configuration
dab validate --config dab-config.json

# Check environment variable
echo $DAB_CONNECTION_STRING
```

Report status:

```text
DAB Configuration Verification

  Config File: dab-config.json
  Validation: Passed
  Database Type: mssql
  Connection: @env('DAB_CONNECTION_STRING')

  Entities:
    - Products (dbo.Products) - anonymous:read
    - Orders (dbo.Orders) - anonymous:read
    - Customers (dbo.Customers) - authenticated:*

  Environment:
    DAB_CONNECTION_STRING: Set

  Status: Ready to start
```

### Step 5: Configure Claude Code

DAB is **not enabled by default** in the plugin. Add mssql-dab to your project's `.claude/settings.json`:

```json
{
  "mcpServers": {
    "mssql-dab": {
      "type": "http",
      "url": "http://localhost:5000/mcp"
    }
  }
}
```

Or to enable globally, add to `~/.claude.json` under `mcpServers`.

### Step 6: Start Instructions

```text
Setup Complete - Starting DAB

IMPORTANT: DAB uses HTTP transport. You must start DAB separately.

To start the DAB server (run in a separate terminal):

  # Set connection string (if not in profile)
  export DAB_CONNECTION_STRING="Server=localhost;Database=test;..."

  # Start DAB - this runs a web server that exposes MCP at /mcp
  dab start --config dab-config.json

  # DAB will listen on http://localhost:5000 by default
  # MCP endpoint: http://localhost:5000/mcp

Available MCP Tools (once DAB is running):
  - describe_entities - List available entities and properties
  - create_record - Insert new data
  - read_records - Query data (auto-cached)
  - update_record - Modify data
  - delete_record - Remove data
  - execute_entity - Execute stored procedures
```

## Output Format

**Installation Success:**

```text
Data API Builder Setup

Phase 1: Installation
  Checking global tools...
  DAB not found, installing...
  dotnet tool install -g microsoft.dataapibuilder --prerelease
  Installed: microsoft.dataapibuilder 2.0.0-preview

Phase 2: Configuration
  Database type: mssql
  Connection: @env('DAB_CONNECTION_STRING')
  Config file: dab-config.json

Phase 3: Entities
  No entities configured yet.

  To add entities:
    dab add <EntityName> --source <schema.table> --permissions "anonymous:read"

  Examples:
    dab add Products --source dbo.Products --permissions "anonymous:read"
    dab add Orders --source dbo.Orders --permissions "authenticated:*"

Setup Complete

Environment variable required:
  DAB_CONNECTION_STRING="Server=...;Database=...;..."

Test with:
  dab start --config dab-config.json
  /microsoft:mssql status --dab
```

**Verification Output:**

```text
DAB Configuration Verification

Config: dab-config.json

  Database: mssql
  Connection: @env('DAB_CONNECTION_STRING')
  Host Mode: Development

Entities (3):
  Entity       Source          Permissions
  -----------  --------------  ---------------
  Products     dbo.Products    anonymous:read
  Orders       dbo.Orders      anonymous:read
  Customers    dbo.Customers   authenticated:*

Environment:
  DAB_CONNECTION_STRING: Configured

Validation: Passed

Ready to start: dab start --config dab-config.json
```

## DAB Configuration File

Example `dab-config.json`:

```json
{
  "$schema": "https://github.com/Azure/data-api-builder/releases/latest/download/dab.draft.schema.json",
  "data-source": {
    "database-type": "mssql",
    "connection-string": "@env('DAB_CONNECTION_STRING')"
  },
  "runtime": {
    "rest": { "enabled": true },
    "graphql": { "enabled": true }
  },
  "entities": {
    "Products": {
      "source": "dbo.Products",
      "permissions": [{
        "role": "anonymous",
        "actions": ["read"]
      }]
    }
  }
}
```

## Examples

```bash
# Install DAB and create initial config
/microsoft:setup-dab --init

# Add an entity with read-only access
/microsoft:setup-dab --add Products

# Verify existing configuration
/microsoft:setup-dab --verify
```

## Manual Commands

If you prefer manual setup:

```bash
# Install DAB
dotnet tool install -g microsoft.dataapibuilder --prerelease

# Initialize config
dab init --database-type mssql --connection-string "@env('DAB_CONNECTION_STRING')"

# Add entities
dab add Products --source dbo.Products --permissions "anonymous:read"
dab add Orders --source dbo.Orders --permissions "authenticated:read,create"

# Validate
dab validate

# Start
dab start
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DAB_CONNECTION_STRING` | Yes | SQL Server connection string (used by `dab start`) |
| `DAB_CONFIG_PATH` | No | Path to dab-config.json (default: ./dab-config.json) |
| `DAB_MCP_URL` | No | MCP endpoint URL (default: <http://localhost:5000/mcp>) |

## Connection String Examples

```bash
# Local SQL Server with Windows Auth
DAB_CONNECTION_STRING="Server=localhost;Database=MyDb;Trusted_Connection=True;TrustServerCertificate=True"

# Azure SQL with AD Interactive
DAB_CONNECTION_STRING="Server=tcp:myserver.database.windows.net,1433;Database=MyDb;Authentication=Active Directory Interactive"

# SQL Server with username/password
DAB_CONNECTION_STRING="Server=localhost;Database=MyDb;User Id=sa;Password=YourPassword;TrustServerCertificate=True"
```

## Security Best Practices

1. **Use environment variables** for connection strings
2. **Principle of least privilege** - only expose needed entities
3. **Use read-only permissions** where possible
4. **Enable authentication** for sensitive data
5. **Review permissions** before production deployment

```bash
# Good: Read-only, specific entities
dab add Products --source dbo.Products --permissions "anonymous:read"

# Risky: Full access to all operations
dab add AllData --source dbo.SensitiveTable --permissions "anonymous:*"
```

## Troubleshooting

**DAB install fails:**

```text
If dotnet tool install fails:
  1. Check .NET 8+ is installed: dotnet --version
  2. Clear NuGet cache: dotnet nuget locals all --clear
  3. Check network/proxy settings
  4. Try without --prerelease for stable version
```

**Connection fails:**

```text
If DAB can't connect:
  1. Verify connection string format
  2. Check SQL Server is running
  3. Verify firewall allows connections
  4. Test with: sqlcmd -S <server> -d <database>
```

**Entity add fails:**

```text
If dab add fails:
  1. Verify table/view exists in database
  2. Check schema name (dbo.TableName not just TableName)
  3. Ensure user has SELECT permission on table
```

## DAB vs MssqlMcp

| Feature | DAB | MssqlMcp |
|---------|-----|----------|
| Access Control | RBAC, entity-level | Connection-level only |
| Query Type | NL2DAB (deterministic) | NL2SQL (fragile) |
| Production Ready | Yes | Experimental |
| Setup Complexity | Higher (entity config) | Lower (connection only) |
| Caching | Built-in | No |
| Best For | Production apps | Quick exploration |

## Related Commands

- `/microsoft:mssql` - Manage MssqlMcp servers (status, rebuild, update)

## Documentation

- [DAB MCP Overview](https://learn.microsoft.com/azure/data-api-builder/mcp/overview)
- [DAB CLI Reference](https://learn.microsoft.com/azure/data-api-builder/cli-reference)
- [DAB Configuration](https://learn.microsoft.com/azure/data-api-builder/configuration-file)
