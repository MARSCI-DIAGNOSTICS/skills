# Multi-Language Support Strategy

**Last Updated:** 2026-01-18

## Overview

This document describes the multi-language support architecture for hooks. While the architecture supports multiple language implementations, **the current production implementation uses .NET exclusively**.

## Current Implementation

All hooks currently use **.NET 10** as the standard implementation:

- Cross-platform compatibility (Windows, macOS, Linux)
- Strong JSON handling with source-generated serialization
- Type safety and AOT compilation support
- Consistent behavior across all platforms
- Executed via `dotnet-run.sh` wrapper script

**Note:** Previous bash implementations have been removed. The multi-language directory structure remains available for future language additions if needed.

## Directory Structure

Current hook directory structure uses .NET implementation:

```text
plugins/<plugin-name>/hooks/<hook-name>/
├── dotnet/                         # .NET implementation (current)
│   └── <hook-name>.cs
├── README.md                       # Hook documentation
```

**Future multi-language support** (not currently implemented):

```text
plugins/<plugin-name>/hooks/<hook-name>/
├── dotnet/                         # .NET implementation (current)
│   └── <hook-name>.cs
├── python/                         # Python implementation (future)
│   ├── <hook_name>.py
│   └── requirements.txt
├── typescript/                     # TypeScript implementation (future)
│   ├── src/
│   │   └── index.ts
│   └── package.json
├── README.md
```

## Future: Configuration-Based Selection (hook.yaml)

When multi-language support is implemented, hooks could use a `hook.yaml` file declaring available implementations:

```yaml
name: prevent-backup-files
version: 1.0.0

# Implementation Management
implementations:
  bash:
    entry_point: bash/prevent-backup-files.sh
    handler: main
    minimum_version: "4.0"
    available: true
  python:
    entry_point: python/prevent_backup_files.py
    handler: validate
    minimum_version: "3.8"
    dependencies: python/requirements.txt
    available: false  # Not yet implemented
  typescript:
    entry_point: typescript/dist/index.js
    handler: validate
    build_command: npm run build
    available: false

# Selection Strategy
selection:
  strategy: preference_order
  preference_order:
    - typescript  # Try TypeScript first (fastest when available)
    - python      # Fallback to Python
    - bash        # Final fallback (always available)
  active: bash    # Currently active implementation
```

## Future: Adding Python Implementation

**Example of how multi-language support would work:**

### 1. Create python/ directory

```bash
mkdir .claude/hooks/prevent-backup-files/python
```

### 2. Create Python implementation

```python
# python/prevent_backup_files.py
import json
import sys

def validate(payload):
    # Your logic here
    pass

if __name__ == "__main__":
    payload = json.load(sys.stdin)
    validate(payload)
```

### 3. Update hook.yaml

```yaml
implementations:
  python:
    available: true  # Mark as available
selection:
  active: python     # Switch to Python
```

### 4. Update .claude/settings.json

```json
{
  "command": "python .claude/hooks/prevent-backup-files/python/prevent_backup_files.py"
}
```

### 5. Test both implementations

```bash
# Test Python
bash .claude/hooks/prevent-backup-files/tests/integration.test.sh

# Compare with bash (temporarily switch back)
```

## Future: Best Tool for the Job

**When choosing implementations (future capability):**

- **.NET (current standard):** Type safety, JSON handling, cross-platform, AOT support
- **Python:** Complex parsing, regex, data processing, external libraries (PyYAML, etc.)
- **TypeScript/Node:** JSON processing, async operations, npm ecosystem

## Future: Multi-Language Support Benefits

When implemented, multi-language support would provide:

- **Language isolation:** dotnet/, python/, typescript/ subdirectories
- **Native conventions:** Each language follows its own project structure
- **Independent tooling:** Language-specific dependencies and build processes
- **Configuration-based selection:** Switch implementations without code changes
- **Migration support:** Run multiple implementations concurrently during transition
- **Fallback strategy:** Preference-order selection (try dotnet → python → typescript)

## Implementation Examples

### .NET Implementation (Current Standard)

```csharp
// dotnet/<hook-name>.cs
using System;
using System.Text.Json;
using System.Text.Json.Serialization;

// Use source-generated JSON for AOT compatibility
[JsonSourceGenerationOptions(PropertyNamingPolicy = JsonKnownNamingPolicy.SnakeCaseLower)]
[JsonSerializable(typeof(HookInput))]
[JsonSerializable(typeof(HookOutput))]
internal partial class HookJsonContext : JsonSerializerContext { }

var input = Console.In.ReadToEnd();
var payload = JsonSerializer.Deserialize(input, HookJsonContext.Default.HookInput);

// Check if enabled
var enabled = Environment.GetEnvironmentVariable("CLAUDE_HOOK_MY_HOOK_ENABLED");
if (enabled == "0")
{
    Console.WriteLine("{}");
    return;
}

// Your logic here

var output = new HookOutput { SystemMessage = "my-hook: completed" };
Console.WriteLine(JsonSerializer.Serialize(output, HookJsonContext.Default.HookOutput));
```

### Future: Python Implementation

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def load_config(hook_dir):
    """Load hook.yaml configuration"""
    # Implementation here
    pass

def is_hook_enabled(config):
    """Check if hook is enabled"""
    return config.get('enabled', True)

def validate(payload):
    """Main validation logic"""
    # Your logic here
    pass

if __name__ == "__main__":
    # Load configuration
    script_dir = Path(__file__).parent
    hook_dir = script_dir.parent
    config = load_config(hook_dir)

    if not is_hook_enabled(config):
        sys.exit(0)

    # Read JSON payload
    payload = json.load(sys.stdin)

    # Validate
    validate(payload)

    sys.exit(0)
```

### Future: TypeScript Implementation

```typescript
// typescript/src/index.ts
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

interface HookPayload {
  tool: string;
  file_path?: string;
  // ... other fields
}

interface HookConfig {
  enabled: boolean;
  enforcement: string;
  // ... other fields
}

function loadConfig(hookDir: string): HookConfig {
  const configPath = path.join(hookDir, 'hook.yaml');
  const configContent = fs.readFileSync(configPath, 'utf8');
  return yaml.load(configContent) as HookConfig;
}

function validate(payload: HookPayload, config: HookConfig): void {
  // Your logic here
}

async function main() {
  const hookDir = path.join(__dirname, '../..');
  const config = loadConfig(hookDir);

  if (!config.enabled) {
    process.exit(0);
  }

  const input = fs.readFileSync(0, 'utf8');
  const payload: HookPayload = JSON.parse(input);

  validate(payload, config);

  process.exit(0);
}

main().catch((error) => {
  console.error(error);
  process.exit(3);
});
```

## Testing Hooks

### Current Testing Approach

Hooks are tested by invoking the .NET implementation through the `dotnet-run.sh` wrapper:

```bash
# Test a hook by piping JSON input
echo '{"tool_name":"Write","tool_input":{"file_path":"test.md"}}' | \
  bash plugins/<plugin>/scripts/dotnet-run.sh plugins/<plugin>/hooks/<hook>/dotnet/<hook>.cs
```

### Future: Multi-Language Testing

When multi-language support is implemented, each language could have its own test file:

```text
tests/
├── dotnet.test.sh              # .NET-specific tests
├── python.test.sh              # Python-specific tests (future)
├── typescript.test.sh          # TypeScript-specific tests (future)
└── fixtures/
    └── payloads.json           # Shared test data
```
