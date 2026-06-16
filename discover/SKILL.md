---
name: discover
description: Main orchestrator for full requirements elicitation workflow. Coordinates interviews, document extraction, simulation, research, and synthesis.
argument-hint: <domain> [--sources <source-types>] [--autonomy <level>] [--output <format>]
allowed-tools: Read, Glob, Grep, Write, Task, Skill, AskUserQuestion
---

# Discover Command

Main orchestrator for comprehensive requirements elicitation.

## Usage

```bash
/requirements-elicitation:discover "checkout"
/requirements-elicitation:discover "authentication" --sources interview,document
/requirements-elicitation:discover "reporting" --autonomy semi-auto
/requirements-elicitation:discover "inventory" --output canonical
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| domain | Yes | Domain/feature area to discover requirements for |
| --sources | No | Comma-separated source types: `interview`, `document`, `simulation`, `research`, `all` (default: `all`) |
| --autonomy | No | Autonomy level: `guided`, `semi-auto`, `full-auto` (default: `semi-auto`) |
| --output | No | Output format: `yaml`, `canonical`, `markdown` (default: `yaml`) |

## Workflow

### Phase 1: Initialization

```yaml
initialization:
  - Create domain folder: .requirements/{domain}/
  - Check for existing requirements
  - Load elicitation-methodology skill
  - Determine available sources
```

### Phase 2: Source-Specific Elicitation

Based on --sources argument, execute appropriate techniques:

#### If `interview` included

```yaml
interview_phase:
  - Identify stakeholders to interview
  - For each stakeholder:
    - Spawn requirements-interviewer agent
    - Conduct structured interview
    - Save transcript and requirements
```

#### If `document` included

```yaml
document_phase:
  - Scan for available documents
  - For each document:
    - Spawn document-miner agent
    - Extract requirements
    - Save extraction results
```

#### If `simulation` included

```yaml
simulation_phase:
  - Select appropriate personas
  - For each persona:
    - Spawn persona agent
    - Simulate stakeholder perspective
    - Capture simulated requirements
```

#### If `research` included

```yaml
research_phase:
  - Identify research topics
  - Query MCP servers:
    - perplexity for best practices
    - context7 for library docs
    - firecrawl for competitive analysis
  - Save research findings
```

### Phase 3: Gap Analysis

```yaml
gap_analysis:
  - Load gap-analysis skill
  - Spawn gap-detector agent
  - Identify missing requirement areas
  - Recommend additional elicitation
```

### Phase 4: Synthesis

```yaml
synthesis:
  - Spawn requirements-synthesizer agent
  - Consolidate all sources
  - Resolve conflicts
  - Produce unified requirement set
```

### Phase 5: Output Generation

```yaml
output:
  - Generate output in requested format
  - Save to .requirements/{domain}/
  - Display summary to user
```

## Autonomy Levels

### Guided Mode

At each phase:

- Present options to user
- Ask for approval before proceeding
- Allow user to modify approach
- Confirm before saving outputs

### Semi-Autonomous Mode

- Execute phases automatically
- Pause at key decision points
- Present summaries for review
- Allow user intervention

### Fully Autonomous Mode

- Execute entire workflow
- Make reasonable decisions automatically
- Present final results only
- Flag items needing human attention

## Examples

### Basic Discovery

```bash
/requirements-elicitation:discover "user-authentication"
```

Output:

```text
Requirements Discovery: user-authentication
Autonomy: semi-auto
Sources: all

Phase 1: Initialization
  Created: .requirements/user-authentication/
  No existing requirements found

Phase 2: Elicitation
  Ready to begin elicitation from all sources.

  Available sources:
  1. Interview - No stakeholders identified yet
  2. Document - No documents provided yet
  3. Simulation - 5 personas available
  4. Research - MCP servers available

  How would you like to proceed?
  [A] Start with stakeholder simulation (recommended for solo work)
  [B] Provide documents to analyze
  [C] Conduct stakeholder interview
  [D] Research domain best practices
  [E] Custom approach
```

### Document-Focused Discovery

```bash
/requirements-elicitation:discover "payment-processing" --sources document,research
```

Output:

```text
Requirements Discovery: payment-processing
Autonomy: semi-auto
Sources: document, research

Phase 1: Initialization
  Created: .requirements/payment-processing/

Phase 2a: Document Extraction
  No documents provided yet.

  Please provide documents by:
  - Pasting content directly
  - Providing file paths
  - Providing URLs

  Waiting for document input...
```

### Fully Autonomous Discovery

```bash
/requirements-elicitation:discover "inventory-management" --autonomy full-auto --sources simulation,research
```

Output:

```text
Requirements Discovery: inventory-management
Autonomy: full-auto
Sources: simulation, research

Executing full autonomous discovery...

Phase 1: Initialization ✓
  Created: .requirements/inventory-management/

Phase 2a: Stakeholder Simulation ✓
  stakeholder-persona end-user: 8 requirements
  stakeholder-persona technical: 12 requirements
  stakeholder-persona business: 10 requirements
  stakeholder-persona operations: 7 requirements
  stakeholder-persona compliance: 5 requirements

Phase 2b: Domain Research ✓
  Best practices: 6 requirements derived
  Technical constraints: 4 requirements derived

Phase 3: Gap Analysis ✓
  Coverage: 75%
  Gaps identified: 3 (security, accessibility, disaster-recovery)

Phase 4: Synthesis ✓
  Total unique requirements: 38
  Conflicts resolved: 2
  Conflicts flagged: 1

Phase 5: Output ✓
  Saved to: .requirements/inventory-management/synthesis/SYN-20251225-160000.yaml

Summary:
  Functional requirements: 24
  Non-functional requirements: 10
  Constraints: 3
  Assumptions: 1

  Ready for specification: YES (1 minor conflict pending)

  Next steps:
  - Review synthesis output
  - Resolve flagged conflict (competing performance targets)
  - Export to canonical format when ready
```

## Output Structure

After discovery, the domain folder contains:

```text
.requirements/{domain}/
├── interviews/
│   └── INT-{timestamp}.yaml
├── documents/
│   └── DOC-{timestamp}.yaml
├── simulations/
│   └── SIM-{timestamp}.yaml
├── research/
│   └── RES-{timestamp}.yaml
├── analysis/
│   └── GAP-{timestamp}.yaml
└── synthesis/
    └── SYN-{timestamp}.yaml
```

## Integration

### Follow-Up Commands

```bash
# Check for gaps
/requirements-elicitation:gaps --domain "{domain}"

# Additional research
/requirements-elicitation:research "{topic}" --domain "{domain}"

# Additional interview
/requirements-elicitation:interview "{stakeholder}" --domain "{domain}"

# Export to specification format
/requirements-elicitation:export --domain "{domain}" --to canonical
```

## Best Practices

1. **Start with simulation for solo work** - Persona agents provide diverse perspectives
2. **Add documents when available** - Existing docs are rich requirement sources
3. **Use research for unfamiliar domains** - MCP servers provide industry knowledge
4. **Run gap analysis before synthesis** - Identify missing areas early
5. **Review synthesis carefully** - Conflicts and gaps need human judgment

## Error Handling

```yaml
error_handling:
  no_sources_available:
    message: "No elicitation sources available"
    action: "Guide user to provide at least one source"

  synthesis_failed:
    message: "Unable to synthesize requirements"
    action: "Show partial results, suggest manual review"

  mcp_unavailable:
    message: "MCP servers not responding"
    action: "Skip research phase, continue with other sources"
```
