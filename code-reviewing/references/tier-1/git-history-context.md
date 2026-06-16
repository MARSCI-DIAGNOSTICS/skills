# Git History Context Analysis

**Tier**: 1 (Universal - Git History)
**Token Budget**: ~1,500 tokens
**Profiles**: thorough, strict (full); security, performance (partial)

## Purpose

Extract git history context to inform code review priorities and catch coupling issues. This analysis identifies:

- Files that typically change together but are missing from the review
- High-churn "hot spots" that warrant extra scrutiny
- Ownership patterns for context
- Recent commit patterns (bug fixes, security changes)

## Step 0e: Git History Analysis Workflow

**CRITICAL:** This step runs BEFORE file counting (Step 1) and AFTER repo config loading (Step 0b).

### Prerequisites

- Git repository with history (>10 commits for meaningful analysis)
- Files to review already identified (staged, PR, or specified paths)
- Profile allows history analysis (skip for `quick` profile)

### 1. Check Configuration

Read history analysis settings from `.claude/code-review.md` if present:

```yaml
## History Analysis
coupling_threshold: 60        # Percentage (40-90), default: 60
hotspot_window_months: 3      # Time window (1-12), default: 3
hotspot_threshold: 10         # Changes count, default: 10
skip_history: false           # Disable entirely, default: false
```

If `skip_history: true` or profile is `quick`, skip remaining steps.

### 2. Gather Files in Review Scope

```bash
# For staged changes
git diff --staged --name-only

# For PR changes
git diff --name-only main...HEAD

# Store as FILES_IN_REVIEW for subsequent analysis
```

### 3. Coupling Analysis (Check 1.33)

Identify files that frequently change together with files in the review scope.

**Command:**

```bash
# For each file in review, find files that commonly change with it
git log --name-only --pretty=format: -- <file> | sort | uniq -c | sort -rn | head -10
```

**Algorithm:**

1. For each file in review scope, get its change history (last 100 commits)
2. Count co-occurrence with other files
3. Calculate co-change percentage: `(times_changed_together / times_file_changed) * 100`
4. Flag if co-change rate > threshold (default 60%) AND the co-changed file is NOT in review

**Edge Cases:**

- New files (< 5 commits): Skip coupling analysis, note in output
- Renamed files: Use `git log --follow` for accurate history
- Generated files: Skip (already excluded from review)

### 4. Hot Spot Detection (Check 1.34)

Identify files in review that have high change frequency.

**Command:**

```bash
# Get change counts for files in review scope within time window
git log --since="3 months ago" --name-only --pretty=format: -- <files> | sort | uniq -c | sort -rn
```

**Algorithm:**

1. Count changes to each file in review scope within configured window
2. Flag files with changes >= threshold (default: 10)
3. Classify recent commits by message patterns:
   - Bug fixes: `fix`, `bug`, `issue`, `patch`, `hotfix`
   - Features: `feat`, `add`, `implement`, `new`
   - Refactoring: `refactor`, `cleanup`, `reorganize`

### 5. Author Context (Check 1.35 - strict only)

Identify ownership patterns for files under review.

**Command:**

```bash
# Get author statistics for files in review
git shortlog -sn -- <files>
```

**Algorithm:**

1. Calculate each author's contribution percentage
2. Identify primary owner (>50% of commits)
3. Flag single-owner files (bus factor = 1)
4. Note if a new author is modifying established files

### 6. Recent History Patterns (Check 1.36)

Analyze recent commits for patterns that inform review priority.

**Command:**

```bash
# Get recent commit messages for files in review
git log --oneline -10 -- <files>
```

**Pattern Detection:**

| Pattern | Keywords | Implication |
|---------|----------|-------------|
| Bug fix | fix, bug, issue, patch | Area may be fragile, extra scrutiny |
| Security | security, auth, vulnerability, CVE | Trigger Tier 3 security checks |
| Refactoring | refactor, cleanup | API may be unstable |
| Performance | perf, optimize, slow | Check for regressions |

---

## Check Definitions

### 1.33 Missing Co-Changed File

**Severity**: MAJOR
**Profiles**: thorough, strict

Files that frequently change together (>60% co-change rate) should typically be reviewed together. Missing co-changed files may indicate:

- Incomplete change (forgot related file)
- Potential inconsistency (API changed, caller not updated)
- Test file not updated with source

**Detection:**

```text
IF file A in review
AND file B has >60% co-change rate with A
AND file B NOT in review
AND file B exists (not deleted)
THEN flag "Missing Co-Changed File"
```

**Output Format:**

```markdown
**1.33 Missing Co-Changed File** [MAJOR]
- File in Review: `src/auth/login.ts`
- Usually Changes With: `src/auth/logout.ts` (68% co-change rate over 45 commits)
- Recommendation: Consider including `logout.ts` in this review or verify it doesn't need updates
```

### 1.34 Hot Spot Under Review

**Severity**: WARNING
**Profiles**: thorough, strict

High-churn files (changed frequently) may indicate:

- Unstable design needing refactoring
- Central component needing extra care
- Area prone to bugs (based on fix frequency)

**Detection:**

```text
IF file in review
AND file changed >= 10 times in last 3 months
THEN flag "Hot Spot Under Review"
```

**Output Format:**

```markdown
**1.34 Hot Spot Under Review** [WARNING]
- File: `src/api/users.ts`
- Change Frequency: 15 changes in last 3 months
- Commit Patterns: bug fixes (8), features (5), refactoring (2)
- Recommendation: This high-churn file warrants careful review. Consider if frequent changes indicate design issues.
```

### 1.35 Single-Owner File

**Severity**: INFO
**Profiles**: strict only

Files with a single primary author may have:

- Bus factor risk (knowledge silos)
- Opportunity for knowledge transfer via review

**Detection:**

```text
IF file in review
AND one author has >90% of commits
AND file has >20 commits total
THEN flag "Single-Owner File"
```

**Output Format:**

```markdown
**1.35 Single-Owner File** [INFO]
- File: `src/core/engine.ts`
- Primary Owner: Alice (45 of 48 commits, 94%)
- Recommendation: This file has a single primary contributor. Consider this review as a knowledge-sharing opportunity.
```

### 1.36 Recent Bug Fix Area

**Severity**: WARNING
**Profiles**: thorough, strict

Areas with recent bug fixes may be fragile and need extra scrutiny.

**Detection:**

```text
IF file in review
AND file has >= 3 bug fix commits in last 3 months
THEN flag "Recent Bug Fix Area"
```

**Output Format:**

```markdown
**1.36 Recent Bug Fix Area** [WARNING]
- File: `src/payment/processor.ts`
- Recent Bug Fixes: 4 in last 3 months
- Recent Commits:
  - `fix: handle null card number` (2 weeks ago)
  - `fix: prevent double charge` (1 month ago)
  - `fix: validate expiry date` (2 months ago)
- Recommendation: This area has been bug-prone recently. Review carefully for edge cases and regression potential.
```

---

## Output Format

Add this section to the code review output when history analysis runs:

```markdown
## History Context Summary

### Coupling Issues
| File in Review | Usually Changes With | Co-Change Rate | Status |
|----------------|---------------------|----------------|--------|
| src/auth/login.ts | src/auth/logout.ts | 68% | MISSING |
| src/api/users.ts | tests/api/users.test.ts | 85% | MISSING |

### Hot Spots (High Churn)
| File | Changes (3mo) | Pattern Breakdown |
|------|---------------|-------------------|
| src/api/users.ts | 15 | bug fixes (8), features (5), refactoring (2) |

### Ownership Context
| File | Primary Owner | Coverage |
|------|---------------|----------|
| src/core/engine.ts | Alice | 94% (45/48 commits) |

### Recent Bug Fix Areas
| File | Bug Fixes (3mo) | Latest Fix |
|------|-----------------|------------|
| src/payment/processor.ts | 4 | "fix: handle null card number" (2 weeks ago) |
```

---

## Profile-Specific Behavior

| Profile | Coupling | Hot Spots | Author | Recent | Notes |
|---------|----------|-----------|--------|--------|-------|
| quick | Skip | Skip | Skip | Skip | Speed priority |
| security | Skip | Skip | Skip | Security keywords only | Focus on security history |
| thorough | Yes | Yes | Skip | Yes | Balanced analysis |
| strict | Yes (enforce) | Yes | Yes | Yes | Full analysis |
| performance | Skip | Perf-related | Skip | Perf keywords | Performance focus |

---

## Edge Cases

1. **New Repository** (< 50 commits total)
   - Skip coupling analysis entirely
   - Note in output: "Limited git history - coupling analysis skipped"

2. **Renamed Files**
   - Use `git log --follow -- <file>` to track across renames
   - Map old paths to new paths for coupling analysis

3. **Large Monorepo** (1000+ files)
   - Limit coupling analysis to files in same directory tree
   - Use `-- <path>` filter to scope git commands

4. **Baseline Mode Integration**
   - History findings are NEW if the coupling issue was introduced in this PR
   - Pre-existing coupling issues are tagged PRE-EXISTING

5. **Binary Files**
   - Skip history analysis for binary files
   - They're already excluded from code review
