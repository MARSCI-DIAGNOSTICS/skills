# Kiro Hooks Integration

Automation hooks for Kiro specification workflows.

## Overview

Hooks enable automation of Kiro specification workflows, including validation, synchronization, and enforcement of specification-driven development practices.

## Hook Events

### Specification Events

| Event | Trigger | Use Case |
| --- | --- | --- |
| `SpecCreated` | New spec file created | Initialize structure, validate format |
| `SpecUpdated` | Spec file modified | Re-validate, sync related files |
| `SpecCompleted` | All tasks marked done | Archive, generate summary |

### Task Events

| Event | Trigger | Use Case |
| --- | --- | --- |
| `TaskStarted` | Task marked in-progress | Log start time, check dependencies |
| `TaskCompleted` | Task marked complete | Update progress, trigger next |
| `TaskBlocked` | Task marked blocked | Alert, suggest resolution |

### Sync Events

| Event | Trigger | Use Case |
| --- | --- | --- |
| `SyncRequested` | Manual sync triggered | Bidirectional sync |
| `DriftDetected` | Specs out of sync | Alert, suggest reconciliation |

## Hook Implementations

### PreToolUse: Spec Validation

Validate specification files before allowing edits:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "tool": "Write",
          "path": ".kiro/specs/**/*.md"
        },
        "command": "validate-kiro-spec"
      }
    ]
  }
}
```

**Validation Script:**

```bash
#!/bin/bash
# validate-kiro-spec.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path')

# Check file type
case "$FILE_PATH" in
  *requirements.md)
    validate_requirements "$FILE_PATH"
    ;;
  *design.md)
    validate_design "$FILE_PATH"
    ;;
  *tasks.md)
    validate_tasks "$FILE_PATH"
    ;;
esac
```

### PostToolUse: Auto-Sync

Automatically sync related files after changes:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": {
          "tool": "Write",
          "path": ".kiro/specs/**/requirements.md"
        },
        "command": "sync-requirements-to-tasks"
      }
    ]
  }
}
```

**Sync Script:**

```python
#!/usr/bin/env python3
"""Sync requirements to tasks."""

import json
import sys
import re

def sync_requirements_to_tasks(req_path: str, tasks_path: str):
    """Ensure all requirements have corresponding tasks."""

    with open(req_path) as f:
        requirements = extract_requirement_ids(f.read())

    with open(tasks_path) as f:
        tasks_content = f.read()

    for req_id in requirements:
        if req_id not in tasks_content:
            print(f"Warning: {req_id} has no corresponding task")
            return {"decision": "warn", "reason": f"Missing task for {req_id}"}

    return {"decision": "allow"}

if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    # Process and output result
```

### SessionStart: Load Context

Load steering context at session start:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "load-kiro-context"
      }
    ]
  }
}
```

**Context Loading Script:**

```python
#!/usr/bin/env python3
"""Load Kiro steering context."""

import os
from pathlib import Path

def load_steering_files():
    """Load all steering files into context."""

    steering_dir = Path(".kiro/steering")

    if not steering_dir.exists():
        return None

    context_parts = []

    for md_file in steering_dir.glob("*.md"):
        with open(md_file) as f:
            content = f.read()
            context_parts.append(f"# {md_file.stem}\n\n{content}")

    return "\n\n---\n\n".join(context_parts)
```

## Enforcement Hooks

### Require EARS Format

Block requirements that don't use EARS patterns:

```python
#!/usr/bin/env python3
"""Enforce EARS patterns in requirements."""

import json
import sys
import re

EARS_PATTERNS = [
    r"The system SHALL",
    r"WHILE .+, the system SHALL",
    r"WHEN .+, the system SHALL",
    r"IF .+, THEN the system SHALL",
    r"WHERE .+, the system SHALL",
]

def check_ears_compliance(content: str) -> bool:
    """Check if all requirements use EARS patterns."""

    # Find all requirement sections
    requirements = re.findall(r"### FR-\d+:.*?\n\n(.*?)(?=\n### |\Z)",
                              content, re.DOTALL)

    for req in requirements:
        if not any(re.search(pattern, req) for pattern in EARS_PATTERNS):
            return False

    return True

if __name__ == "__main__":
    input_data = json.load(sys.stdin)

    # Get the content being written
    content = input_data.get("content", "")

    if not check_ears_compliance(content):
        result = {
            "decision": "block",
            "reason": "Requirements must use EARS patterns (SHALL, WHEN, WHILE, IF, WHERE)"
        }
    else:
        result = {"decision": "allow"}

    print(json.dumps(result))
```

### Require Acceptance Criteria

Block requirements without acceptance criteria:

```python
#!/usr/bin/env python3
"""Enforce acceptance criteria on requirements."""

import json
import sys
import re

def check_acceptance_criteria(content: str) -> list:
    """Find requirements missing acceptance criteria."""

    missing = []

    # Find all FR-x sections
    sections = re.findall(r"### (FR-\d+):.*?(?=\n### |\Z)", content, re.DOTALL)

    for section in sections:
        req_id = re.match(r"FR-\d+", section).group()

        if "#### Acceptance Criteria" not in section:
            missing.append(req_id)
        elif "- [ ] AC-" not in section:
            missing.append(req_id)

    return missing

if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    content = input_data.get("content", "")

    missing = check_acceptance_criteria(content)

    if missing:
        result = {
            "decision": "block",
            "reason": f"Requirements missing acceptance criteria: {', '.join(missing)}"
        }
    else:
        result = {"decision": "allow"}

    print(json.dumps(result))
```

## Automation Workflows

### Auto-Generate Tasks from Requirements

When requirements are finalized, auto-generate task stubs:

```python
#!/usr/bin/env python3
"""Generate task stubs from requirements."""

import re
from pathlib import Path

def generate_tasks(requirements_path: str, tasks_path: str):
    """Generate task stubs for each requirement."""

    with open(requirements_path) as f:
        content = f.read()

    # Extract requirement IDs and titles
    requirements = re.findall(r"### (FR-\d+): (.+)", content)

    tasks = ["# Tasks\n\n## Task List\n"]

    for idx, (req_id, title) in enumerate(requirements, 1):
        task = f"""
- [ ] **TSK-{idx:03d}**: Implement {title}
  - Requirement: {req_id}
  - Effort: M
  - Deliverables: TBD
  - Acceptance: TBD
"""
        tasks.append(task)

    tasks.append("""
## Progress

| Status | Count |
| --- | --- |
| Pending | {} |
| Complete | 0 |
""".format(len(requirements)))

    with open(tasks_path, 'w') as f:
        f.write("\n".join(tasks))
```

### Progress Tracking

Track task completion progress:

```python
#!/usr/bin/env python3
"""Track task progress after updates."""

import json
import sys
import re

def count_task_states(content: str) -> dict:
    """Count tasks by state."""

    return {
        "pending": len(re.findall(r"- \[ \]", content)),
        "in_progress": len(re.findall(r"- \[~\]", content)),
        "complete": len(re.findall(r"- \[x\]", content)),
        "blocked": len(re.findall(r"- \[-\]", content)),
    }

def update_progress_section(content: str, counts: dict) -> str:
    """Update the progress section with current counts."""

    new_progress = f"""## Progress

| Status | Count |
| --- | --- |
| Pending | {counts['pending']} |
| In Progress | {counts['in_progress']} |
| Complete | {counts['complete']} |
| Blocked | {counts['blocked']} |
"""

    # Replace existing progress section
    return re.sub(r"## Progress\n.*?(?=\n## |\Z)",
                  new_progress, content, flags=re.DOTALL)
```

## Configuration

### hooks.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "tool": "Write",
          "path": ".kiro/specs/**/requirements.md"
        },
        "command": ".kiro/hooks/validate-requirements.py",
        "environment": {
          "KIRO_STRICT_MODE": "true"
        }
      }
    ],
    "PostToolUse": [
      {
        "matcher": {
          "tool": "Write",
          "path": ".kiro/specs/**/*.md"
        },
        "command": ".kiro/hooks/sync-specs.py"
      }
    ]
  }
}
```

### Environment Variables

| Variable | Purpose |
| --- | --- |
| `KIRO_STRICT_MODE` | Enable strict validation |
| `KIRO_AUTO_SYNC` | Enable automatic sync |
| `KIRO_SPECS_PATH` | Custom specs location |

## Best Practices

### Hook Design

1. **Fast Execution:** Hooks should complete quickly
2. **Clear Messages:** Provide actionable feedback
3. **Idempotent:** Safe to run multiple times
4. **Focused:** One hook, one responsibility

### Error Handling

1. **Graceful Degradation:** Don't block on non-critical errors
2. **Helpful Messages:** Explain what's wrong and how to fix
3. **Logging:** Log for debugging but don't spam

### Testing

1. **Unit Test:** Test validation logic in isolation
2. **Integration Test:** Test hooks with real spec files
3. **Edge Cases:** Handle empty files, malformed content
