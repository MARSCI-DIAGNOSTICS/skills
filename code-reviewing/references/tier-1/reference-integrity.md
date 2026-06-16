# Reference Integrity Checks

**Tier**: 1 (Always Applied when renames/deletions detected)
**Token Budget**: ~1,500 tokens
**Profile**: `thorough`, `strict` (always-on for CRITICAL checks)

## Purpose

Verify all references are updated when files, functions, classes, or variables are renamed or deleted. Catches broken imports, stale documentation links, and orphaned configuration references.

## Detection Workflow (Step 1d)

### 1. Detect Renames and Deletions from Git

```bash
# Detect renamed files (R = rename)
git diff --name-status HEAD~1 | grep ^R
# Output: R100    old/path/file.ts    new/path/file.ts

# Detect deleted files (D = delete)
git diff --name-status HEAD~1 | grep ^D
# Output: D    deleted/file.ts

# For staged changes
git diff --staged --name-status | grep -E '^[RD]'

# For PR changes
git diff --name-status main...HEAD | grep -E '^[RD]'
```

### 2. Detect Symbol Renames (Functions, Classes, Variables)

Symbol renames are harder to detect. Use these heuristics:

```text
1. Parse git diff for removed + added patterns:
   - Removed: `export function oldName(`
   - Added: `export function newName(`
   → Likely rename if in same file/similar context

2. Look for semantic patterns:
   - Class rename: `class OldName` → `class NewName`
   - Interface rename: `interface IOldName` → `interface INewName`
   - Constant rename: `const OLD_NAME` → `const NEW_NAME`
   - Type alias rename: `type OldType` → `type NewType`

3. Language-specific detection:
   - C#: Check for renamed public members in same file
   - TypeScript: Check for renamed exports
   - Python: Check for renamed functions/classes at module level
```

### 3. Search for Stale References

For each detected rename/deletion, search for remaining references:

```bash
# Search for old file path in imports
grep -r "from ['\"].*old/path/file" --include="*.ts" --include="*.tsx"
grep -r "import.*old/path/file" --include="*.ts" --include="*.tsx"

# Search for old symbol name
grep -r "\bOldClassName\b" --include="*.ts" --include="*.tsx"
grep -r "\boldFunctionName\b" --include="*.ts" --include="*.tsx"

# Search in documentation (markdown links)
grep -r "\[.*\](.*old/path/file" --include="*.md"
grep -r "](old/path/file" --include="*.md"

# Search in configuration files
grep -r "old/path/file\|OldClassName" --include="*.json" --include="*.yaml" --include="*.toml"
```

## Checks

### 1.30.1 Broken Imports After Rename (CRITICAL)

**Detection**: Parse import statements, verify referenced file/module exists.

**Languages**:

| Language | Import Pattern | Verification |
|----------|----------------|--------------|
| TypeScript/JavaScript | `import { X } from './path'` | Check if path resolves |
| Python | `from module import X` | Check if module exists |
| C# | `using Namespace.Class` | Check if namespace/class exists |
| Go | `import "package/path"` | Check if package exists |
| Rust | `use crate::module::Item` | Check if module/item exists |

**Severity**: CRITICAL (code won't compile/run)

**Finding Format**:

```markdown
### Broken Import After Rename

**File**: `src/services/user.ts:5`
**Severity**: CRITICAL
**Confidence**: HIGH

**Problem**: Import references deleted/renamed file.

**Details**:
- Import: `import { UserService } from './old-user-service'`
- Target: `./old-user-service.ts` was renamed to `./user-service.ts`
- Status: Import path not updated

**Fix**: Update import path to new location.

**Suggested Fix**:
```typescript
// Before
import { UserService } from './old-user-service';

// After
import { UserService } from './user-service';
```

### 1.30.2 Stale Documentation Links (MAJOR)

**Detection**: Parse markdown links, verify target files exist.

**Link Patterns**:

```markdown
# Relative links
[Link Text](./path/to/file.md)
[Link Text](../other/file.md#section)

# Reference-style links
[Link Text][ref]
[ref]: ./path/to/file.md

# Image references
![Alt Text](./images/diagram.png)
```

**Verification**:

1. Extract link target from markdown
2. Resolve relative to current file's directory
3. Check if target file exists
4. For anchors (#section), optionally verify heading exists

**Severity**: MAJOR (documentation integrity)

**Finding Format**:

```markdown
### Stale Documentation Link

**File**: `docs/architecture.md:42`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Markdown link references deleted/renamed file.

**Details**:
- Link: `[API Design](./api/old-design.md)`
- Target: `./api/old-design.md` was renamed to `./api/design.md`
- Status: Link not updated

**Fix**: Update link to new file path.
```

### 1.30.3 Orphaned Config References (MAJOR)

**Detection**: Search configuration files for references to renamed/deleted paths or symbols.

**Configuration Files to Check**:

| File Type | Reference Patterns |
|-----------|-------------------|
| `package.json` | `main`, `exports`, `bin`, `files` |
| `tsconfig.json` | `paths`, `include`, `exclude`, `references` |
| `*.csproj` | `<Compile Include>`, `<ProjectReference>` |
| `docker-compose.yml` | `build.context`, `volumes` |
| `webpack.config.js` | `entry`, `alias` |
| `.env*` | Path references |
| `jest.config.js` | `moduleNameMapper`, `testMatch` |

**Severity**: MAJOR (build/runtime failures)

**Finding Format**:

```markdown
### Orphaned Configuration Reference

**File**: `tsconfig.json:15`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Configuration references deleted/renamed path.

**Details**:
- Config: `"paths": { "@utils/*": ["./src/old-utils/*"] }`
- Target: `./src/old-utils/` was renamed to `./src/utils/`
- Status: Path alias not updated

**Fix**: Update path alias to new directory.
```

### 1.30.4 Hardcoded String References (MINOR)

**Detection**: Grep for old names in string literals (low confidence).

**String Patterns**:

```typescript
// Template literals
`Loading ${oldClassName}...`

// Error messages
throw new Error('OldClassName not found');

// Logging
console.log('Processing oldFunctionName');

// Configuration strings
const endpoint = '/api/old-endpoint';
```

**Confidence**: LOW (may be intentional, false positives common)

**Severity**: MINOR (profile-gated)

**Finding Format**:

```markdown
### Possible Stale String Reference

**File**: `src/logger.ts:23`
**Severity**: MINOR
**Confidence**: LOW

**Problem**: String literal may reference renamed symbol.

**Details**:
- String: `"Processing OldServiceName request"`
- Symbol `OldServiceName` was renamed to `ServiceName`
- Status: String may need update (verify manually)

**Fix**: Review and update string if it refers to the renamed symbol.
```

## Cross-Reference Validation

When renames/deletions are detected, perform comprehensive search:

```text
1. Build list of old names (files and symbols)

2. For each old name, search across codebase:
   a. Source files (imports, references)
   b. Test files (imports, mocks, assertions)
   c. Documentation (links, examples)
   d. Configuration (paths, aliases)
   e. Build scripts (references)

3. For each reference found:
   a. Check if corresponding update exists in diff
   b. If no update → flag as stale reference
   c. Assign severity based on reference type
```

## Edge Cases

| Scenario | Handling |
|----------|----------|
| File moved (not just renamed) | Treat as rename, check old import paths |
| Symbol renamed across files | Search all files for old symbol |
| Partial rename (typo fix) | Apply fuzzy matching |
| Re-export through barrel | Check barrel file AND consumers |
| Dynamic imports | Lower confidence, flag for manual review |
| Generated code references | Check if generator updated, not generated files |

## Language-Specific Patterns

### TypeScript/JavaScript

```typescript
// Named imports
import { OldName } from './module';

// Default imports
import OldName from './module';

// Re-exports
export { OldName } from './module';
export * from './old-module';

// Dynamic imports
const module = await import('./old-module');

// Type imports
import type { OldType } from './types';
```

### Python

```python
# Standard imports
from old_module import OldClass
import old_module

# Relative imports
from .old_module import function
from ..old_package import module

# __init__.py re-exports
from .old_module import *
```

### C\#

```csharp
// Using statements
using OldNamespace.OldClass;
using static OldNamespace.Utilities;

// Project references (in .csproj)
<ProjectReference Include="..\OldProject\OldProject.csproj" />

// Assembly references
[assembly: InternalsVisibleTo("OldProject.Tests")]
```

## Integration with Baseline Mode

When `--baseline` is specified, reference integrity issues are attributed:

- **NEW**: Reference was broken by changes in this changeset
- **PRE-EXISTING**: Reference was already broken before this changeset

Only NEW issues block merges in quality gates.

## Quick Reference

```text
REFERENCE INTEGRITY CHECKS:
[CRITICAL] Broken imports after rename → Always check
[MAJOR] Stale documentation links → Always check
[MAJOR] Orphaned config references → Always check
[MINOR] Hardcoded string references → Profile-gated (thorough/strict)

DETECTION STEPS:
1. Parse git diff for renames (R) and deletions (D)
2. Extract old file paths and symbol names
3. Search codebase for remaining references
4. Cross-reference with changes in diff
5. Flag unupdated references by severity
```

---

**Last Updated:** 2025-12-31
