---
name: simulate
description: Run multi-stakeholder simulation to generate requirements from diverse perspectives. Simulates End User, Technical, Business, Compliance, and Operations stakeholders.
argument-hint: <topic> [--personas <persona-list>] [--domain <domain-name>] [--mode <simulation-mode>]
allowed-tools: Read, Glob, Grep, Write, Task, Skill
---

# Simulate Command

Run multi-stakeholder simulation to generate requirements from diverse perspectives when real stakeholders are unavailable.

## Usage

```bash
/requirements-elicitation:simulate "checkout redesign"
/requirements-elicitation:simulate "payment processing" --personas technical,compliance
/requirements-elicitation:simulate "user dashboard" --domain "analytics" --mode conflict
/requirements-elicitation:simulate "mobile app" --personas all --mode comprehensive
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| topic | Yes | The feature, system, or topic to simulate stakeholder perspectives for |
| --personas | No | Comma-separated list: `end-user`, `technical`, `business`, `compliance`, `operations`, or `all` (default: `all`) |
| --domain | No | Domain name for organizing output files |
| --mode | No | Simulation mode: `standard`, `conflict`, `comprehensive` (default: `standard`) |

## Simulation Modes

### Standard Mode

- Each persona generates requirements independently
- Basic conflict detection
- Good for initial discovery

### Conflict Mode

- Focuses on identifying conflicts between perspectives
- Personas "discuss" conflicting requirements
- Suggests resolutions

### Comprehensive Mode

- Multiple rounds of simulation
- Personas respond to each other's requirements
- Most thorough but takes longer

## Workflow

### Step 1: Initialize Simulation

Parse arguments and set up context:

```yaml
simulation_context:
  topic: "{from argument}"
  domain: "{from --domain or derive}"
  personas: ["{selected personas}"]
  mode: "{from --mode or default}"
  session_id: "SIM-{timestamp}"
```

### Step 2: Load Stakeholder Simulation Skill

Invoke the `requirements-elicitation:stakeholder-simulation` skill to load persona profiles.

### Step 3: Run Persona Simulations

For each selected persona, spawn the corresponding agent:

**Unified Agent with Persona Arguments:**

Use `stakeholder-persona` agent with persona type argument:

- `stakeholder-persona end-user` - Usability, UX, accessibility
- `stakeholder-persona technical` - Architecture, scalability, security
- `stakeholder-persona business` - ROI, market fit, value
- `stakeholder-persona compliance` - Regulatory, legal, audit
- `stakeholder-persona operations` - Deployment, monitoring, support

### Step 4: Collect and Analyze

Gather requirements from all personas:

- Categorize by type and priority
- Detect conflicts between perspectives
- Identify common themes

### Step 5: Consolidate

Merge and deduplicate requirements:

- Combine similar requirements
- Note which personas support each
- Flag conflicts for resolution

### Step 6: Save and Report

Save to `.requirements/{domain}/simulations/`
Display summary of findings.

## Examples

### Basic Simulation

```bash
/requirements-elicitation:simulate "e-commerce checkout"
```

Output:

```text
Stakeholder Simulation: e-commerce checkout
Session: SIM-20251225-150000
Mode: standard

Simulating 5 personas...

End User Persona:
- 8 requirements generated
- Focus: Simplicity, speed, error recovery

Technical Stakeholder:
- 6 requirements generated
- Focus: Security, scalability, integration

Business Stakeholder:
- 5 requirements generated
- Focus: Conversion, revenue, competitive features

Compliance Stakeholder:
- 7 requirements generated
- Focus: PCI-DSS, data protection, consent

Operations Stakeholder:
- 4 requirements generated
- Focus: Monitoring, deployment, recovery

Summary:
- Total requirements: 30
- Unique (after dedup): 26
- Conflicts detected: 3

Conflicts:
1. [end-user vs technical] Simplicity vs Security
   - EU wants: "One-click checkout"
   - Tech wants: "MFA for all transactions"
   - Suggested: "Risk-based authentication"

2. [business vs compliance] Data collection
   - Biz wants: "Collect browsing data for recommendations"
   - Comp wants: "Minimize data collection"
   - Suggested: "Opt-in with clear consent"

Saved to: .requirements/e-commerce/simulations/SIM-20251225-150000.yaml
```

### Focused Simulation

```bash
/requirements-elicitation:simulate "API security" --personas technical,compliance,operations
```

Output:

```text
Stakeholder Simulation: API security
Session: SIM-20251225-151500
Mode: standard
Personas: technical, compliance, operations

Technical Stakeholder:
- OAuth 2.0 + JWT requirements
- Rate limiting requirements
- Input validation requirements

Compliance Stakeholder:
- Audit logging requirements
- Data encryption requirements
- Access control requirements

Operations Stakeholder:
- API monitoring requirements
- Incident response requirements
- Key rotation requirements

Summary:
- Total requirements: 18
- Strong consensus on security fundamentals
- Minor conflict on logging granularity

Saved to: .requirements/api/simulations/SIM-20251225-151500.yaml
```

### Conflict-Focused Simulation

```bash
/requirements-elicitation:simulate "feature prioritization" --mode conflict --domain "product-roadmap"
```

Output:

```text
Stakeholder Simulation: feature prioritization
Session: SIM-20251225-153000
Mode: conflict (focus on disagreements)

Conflict Analysis:

CONFLICT 1: Release Timeline
- Business: "Ship MVP in 2 months"
- Technical: "Need 4 months for proper architecture"
- Operations: "Need 3 months for proper monitoring"
→ Resolution: Phased release with feature flags

CONFLICT 2: Feature Scope
- End User: "Keep it simple, fewer features"
- Business: "More features for competitive parity"
→ Resolution: Core MVP + optional advanced features

CONFLICT 3: Data Retention
- Business: "Keep all data for analytics"
- Compliance: "Delete after 90 days per GDPR"
- Operations: "Archival storage costs are high"
→ Resolution: Tiered retention with anonymization

CONFLICT 4: Authentication
- End User: "Social login only"
- Technical: "Enterprise SSO required"
- Compliance: "MFA for sensitive operations"
→ Resolution: Multiple auth methods with risk-based MFA

Saved to: .requirements/product-roadmap/simulations/SIM-20251225-153000.yaml
```

## Output Format

### Saved YAML Structure

```yaml
simulation_session:
  id: "SIM-{timestamp}"
  topic: "{topic}"
  domain: "{domain}"
  mode: standard|conflict|comprehensive
  timestamp: "{ISO-8601}"

personas_simulated:
  - name: end-user
    agent: stakeholder-persona
    agent_arg: end-user
    requirements_count: 8
  - name: technical
    agent: stakeholder-persona
    agent_arg: technical
    requirements_count: 6
  # ... more personas

requirements:
  - id: REQ-SIM-001
    text: "{requirement}"
    perspectives: [end-user, business]
    priority: must
    confidence: medium
    needs_validation: true

  - id: REQ-SIM-002
    text: "{requirement}"
    perspectives: [technical, operations]
    priority: should
    confidence: medium
    needs_validation: true

conflicts:
  - id: CONFLICT-001
    topic: "Authentication complexity"
    positions:
      end-user: "Simple login"
      technical: "MFA required"
    suggested_resolution: "Risk-based authentication"
    requires_decision: true

themes:
  - name: "Security"
    requirements: [REQ-SIM-003, REQ-SIM-007, REQ-SIM-012]
  - name: "Performance"
    requirements: [REQ-SIM-004, REQ-SIM-009]

validation_notes:
  - "All simulated requirements need stakeholder validation"
  - "Conflict resolutions are suggestions only"
  - "Priority assignments based on persona consensus"
```

## Integration

### Follow-Up Commands

```bash
# Validate with real stakeholders
/requirements-elicitation:interview "Product Manager" --context "validate simulation"

# Check for gaps
/requirements-elicitation:gaps

# Research specific topics that came up
/requirements-elicitation:research "risk-based authentication best practices"

# Consolidate with other sources
/requirements-elicitation:discover "{domain}" --sources simulations,interviews
```

## Important Notes

**Confidence Level**: All simulated requirements have `confidence: medium` and `needs_validation: true`. Simulation cannot replace real stakeholder input.

**Best Use**: Simulation is best for:

- Initial discovery when stakeholders unavailable
- Validating completeness of existing requirements
- Identifying potential conflicts before stakeholder meetings
- Solo developers who need diverse perspectives
