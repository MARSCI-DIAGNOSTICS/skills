# Action: prompt-extract

Extract prompts from session transcripts to build a personal prompt library and learn from successful patterns.

## Arguments

| Argument | Description |
|----------|-------------|
| `--successful-only` | Only extract prompts that led to successful outcomes |
| `--category CATEGORY` | Filter by task category (code-review, refactor, feature, bug, etc.) |
| `--days N` | Extract from sessions in last N days (default: 30) |
| `--export FILE` | Export extracted prompts to markdown file |
| `--min-length N` | Minimum prompt length in characters (default: 20) |
| (no args) | Extract all prompts from recent sessions |

## What Defines "Successful"

A prompt is considered successful when the resulting session shows:

| Indicator | Weight |
|-----------|--------|
| Task completed without errors | High |
| No user corrections required | High |
| No "let me try again" from assistant | Medium |
| No follow-up "that's wrong" from user | Medium |
| Minimal retries/iterations | Medium |
| Explicit user approval ("thanks", "perfect") | Low |

## Workflow

### Step 1: Find Sessions

```python
from pathlib import Path
from datetime import datetime, timezone, timedelta

claude_dir = Path.home() / ".claude"
projects_dir = claude_dir / "projects"

cutoff = datetime.now(timezone.utc) - timedelta(days=30)

sessions = []
for project_dir in projects_dir.iterdir():
    if project_dir.is_dir():
        for session_file in project_dir.glob("*.jsonl"):
            if not session_file.name.startswith("agent-"):
                mtime = datetime.fromtimestamp(session_file.stat().st_mtime, tz=timezone.utc)
                if mtime > cutoff:
                    sessions.append({
                        "path": session_file,
                        "project": project_dir.name,
                        "modified": mtime
                    })
```

### Step 2: Extract Prompts

Parse session JSONL for user messages, pair with assistant responses, and analyze success.

### Step 3: Analyze Success

```python
def analyze_success(prompt, response, subsequent_messages):
    """Determine if a prompt led to successful outcome."""
    score = 100

    failure_phrases = ["error", "failed", "let me try again", "sorry",
                       "that didn't work", "I apologize", "mistake"]
    for phrase in failure_phrases:
        if phrase in response.lower():
            score -= 20

    for msg in subsequent_messages:
        if msg.get("role") == "user":
            content = msg.get("content", "").lower()
            correction_phrases = ["no", "wrong", "that's not", "actually",
                                  "I meant", "try again", "fix"]
            for phrase in correction_phrases:
                if phrase in content:
                    score -= 15

    positive_phrases = ["thanks", "perfect", "great", "works", "done"]
    for msg in subsequent_messages:
        if msg.get("role") == "user":
            for phrase in positive_phrases:
                if phrase in msg.get("content", "").lower():
                    score += 10

    return score >= 70
```

### Step 4: Categorize Prompts

```python
def categorize_prompt(prompt_text):
    categories = {
        "code-review": ["review", "check", "audit", "look at"],
        "refactor": ["refactor", "clean up", "improve", "optimize"],
        "feature": ["add", "implement", "create", "build", "new"],
        "bug": ["fix", "bug", "error", "issue", "broken"],
        "documentation": ["document", "readme", "docs", "explain"],
        "test": ["test", "spec", "coverage", "unit test"],
        "configuration": ["config", "setup", "install", "configure"]
    }
    prompt_lower = prompt_text.lower()
    for category, keywords in categories.items():
        if any(kw in prompt_lower for kw in keywords):
            return category
    return "general"
```

## Output Format

Shows extracted prompts grouped by category with success scores, what worked, and what didn't. Export format creates a reusable prompt library in markdown.

## Use Cases

1. **Build prompt library** - Collect prompts that work well
2. **Learn from failures** - Understand why some prompts need iteration
3. **Improve prompting skills** - Identify patterns that succeed
4. **Share with team** - Export prompts for team reference
5. **Train new users** - Show examples of effective prompts
