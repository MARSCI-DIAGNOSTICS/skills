---
name: check-api-status
description: Check Anthropic API status and recent incidents from status.anthropic.com
allowed-tools: WebFetch, mcp__perplexity__search
---

# Check API Status

Check the current status of Anthropic's API and Claude services. Useful when experiencing slowdowns to determine if the issue is on Anthropic's end.

## Usage

```text
/check-api-status
```

## What Gets Checked

1. **Anthropic Status Page** - status.anthropic.com
2. **Claude Status Page** - status.claude.ai (if available)
3. **Recent Incidents** - Last 7 days of reported issues
4. **Community Reports** - Recent social media/forum reports

## Workflow

### Step 1: Fetch Status Page

Use WebFetch to retrieve status.anthropic.com:

```text
Fetch https://status.anthropic.com and extract:
- Current overall status
- Individual service statuses (API, Console, Claude.ai)
- Active incidents
- Recent resolved incidents
```

### Step 2: Search for Recent Issues

Use perplexity to search for recent reports:

```text
Search: "Anthropic Claude API slow outage December 2025"
```

### Step 3: Present Findings

```text
Anthropic API Status
====================
Checked: {timestamp}

Overall Status: {OPERATIONAL | DEGRADED | OUTAGE}

Services:
  API:          {status}
  Console:      {status}
  Claude.ai:    {status}
  Claude Code:  {status}

Active Incidents:
  {if any - title, start time, current status}

Recent Incidents (last 7 days):
  {date}: {incident title} - {RESOLVED | MONITORING}

Community Reports:
  {if found - recent reports of issues}

Interpretation:
  {guidance based on findings}
```

## Example Output

### All Clear

```text
Anthropic API Status
====================
Checked: 2025-12-26 15:45:00 EST

Overall Status: OPERATIONAL

Services:
  API:          Operational
  Console:      Operational
  Claude.ai:    Operational
  Claude Code:  Operational

Active Incidents: None

Recent Incidents (last 7 days):
  Dec 21: API Performance Degradation - RESOLVED
          Duration: 2 hours
          Impact: Increased latency for some requests

Community Reports: No widespread issues reported

Interpretation:
  All systems operational. If you're experiencing slowdowns,
  the issue is likely local. Try:
  - /check-claude-storage for storage bloat
  - /cleanup-sessions 7 to free space
  - Restart Claude Code
```

### During Incident

```text
Anthropic API Status
====================
Checked: 2025-12-26 15:45:00 EST

Overall Status: DEGRADED PERFORMANCE

Services:
  API:          Degraded
  Console:      Operational
  Claude.ai:    Degraded
  Claude Code:  Degraded

Active Incidents:
  Title: Increased API Latency
  Started: 2025-12-26 14:00 UTC
  Status: Investigating
  Description: Some users experiencing slower response times

Recent Incidents (last 7 days):
  Dec 21: API Performance Degradation - RESOLVED

Community Reports:
  Multiple reports on social media of slow responses

Interpretation:
  There is a known issue affecting Claude services.
  Anthropic is investigating. Consider:
  - Waiting for resolution
  - Reducing request frequency
  - Using simpler prompts
```

## Notes

- This command requires internet access
- Status page may not reflect all issues immediately
- Community reports can indicate issues before official acknowledgment
- For local issues, use `/diagnose-performance` instead
