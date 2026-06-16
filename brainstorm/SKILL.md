---
name: brainstorm
description: "Facilitate AI-assisted brainstorming sessions for requirements discovery. Uses divergent-convergent thinking patterns to generate ideas, then filters and refines them. Supports multiple brainstorming techniques."
argument-hint: "[--domain <domain-name>] [--technique freeform|reverse|starbursting|scamper|sixhats] [--rounds <number>]"
allowed-tools: Task, Read, Write, Glob, Grep, Skill, AskUserQuestion
---

# Brainstorm Command

Facilitate AI-assisted brainstorming sessions for discovering new requirements and ideas.

## Interactive Session Setup

Use AskUserQuestion to configure the brainstorming session:

```yaml
# Question 1: Brainstorming Technique (MCP: divergent thinking methodologies)
question: "What brainstorming technique should we use?"
header: "Technique"
options:
  - label: "Freeform (Recommended)"
    description: "Classic brainstorm - quantity over quality, build on ideas"
  - label: "Reverse Brainstorming"
    description: "Think about how to CAUSE the problem, then flip"
  - label: "SCAMPER"
    description: "Substitute, Combine, Adapt, Modify, Eliminate, Reverse"
  - label: "Six Thinking Hats"
    description: "Parallel thinking from six perspectives"

# Question 2: Session Scope (MCP: CLI best practices - MVP vs Full)
question: "How comprehensive should the session be?"
header: "Scope"
options:
  - label: "Quick Ideation (Recommended)"
    description: "1 round, 20-30 ideas, top 5 candidates (~15 min)"
  - label: "Standard Session"
    description: "2 rounds, 40-50 ideas, grouped themes (~30 min)"
  - label: "Deep Exploration"
    description: "3+ rounds, all techniques, full refinement (~60 min)"
```

Use these responses to tailor technique selection and session depth.

## Usage

```bash
/requirements-elicitation:brainstorm
/requirements-elicitation:brainstorm --domain "mobile-app"
/requirements-elicitation:brainstorm --domain "checkout" --technique reverse
/requirements-elicitation:brainstorm --domain "onboarding" --technique sixhats --rounds 3
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| --domain | No | Domain to brainstorm for (default: current/most recent) |
| --technique | No | Brainstorming technique: `freeform`, `reverse`, `starbursting`, `scamper`, `sixhats` (default: `freeform`) |
| --rounds | No | Number of brainstorming rounds (default: 2) |

## Brainstorming Techniques

### Freeform (Default)

Classic brainstorming - generate as many ideas as possible without judgment.

```yaml
freeform:
  phase_1_diverge:
    goal: "Generate maximum ideas"
    rules:
      - "No criticism or evaluation"
      - "Quantity over quality"
      - "Build on others' ideas"
      - "Wild ideas welcome"
    prompts:
      - "What features could help users achieve [goal]?"
      - "What would make this 10x better?"
      - "What would competitors wish they had?"
      - "What would users love but not expect?"

  phase_2_converge:
    goal: "Filter and group ideas"
    actions:
      - "Remove duplicates"
      - "Group related ideas"
      - "Identify themes"
      - "Flag most promising"
```

### Reverse Brainstorming

Generate ideas by thinking about how to cause the problem.

```yaml
reverse:
  phase_1_reverse:
    question: "How could we make [problem] WORSE?"
    examples:
      - "How could we make checkout MORE confusing?"
      - "How could we make search MORE frustrating?"
      - "How could we make onboarding SLOWER?"

  phase_2_flip:
    action: "Reverse each idea to find solutions"
    example:
      problem: "Make checkout take longer"
      flipped: "Add one-click checkout option"

  phase_3_refine:
    action: "Evaluate flipped ideas as requirements"
```

### Starbursting

Generate questions rather than answers to explore the problem space.

```yaml
starbursting:
  question_categories:
    who:
      - "Who will use this?"
      - "Who is affected by this?"
      - "Who needs to approve this?"

    what:
      - "What problem does this solve?"
      - "What features are needed?"
      - "What could go wrong?"

    when:
      - "When will users need this?"
      - "When should this be available?"
      - "When would this fail?"

    where:
      - "Where will this be used?"
      - "Where does this fit in the journey?"
      - "Where are the integration points?"

    why:
      - "Why do users need this?"
      - "Why would they choose this?"
      - "Why might they resist this?"

    how:
      - "How will users interact with this?"
      - "How will we know it's working?"
      - "How will we support this?"
```

### SCAMPER

Systematic creativity technique using seven prompts.

```yaml
scamper:
  substitute:
    prompt: "What can be substituted?"
    examples:
      - "Replace password with biometrics"
      - "Substitute manual entry with auto-fill"

  combine:
    prompt: "What can be combined?"
    examples:
      - "Combine login and preferences setup"
      - "Merge checkout and account creation"

  adapt:
    prompt: "What can be adapted from elsewhere?"
    examples:
      - "Adapt Netflix's recommendation engine"
      - "Adapt Uber's real-time tracking"

  modify:
    prompt: "What can be modified/magnified/minimized?"
    examples:
      - "Magnify the confirmation feedback"
      - "Minimize the number of form fields"

  put_to_other_uses:
    prompt: "What else could this be used for?"
    examples:
      - "Use search for navigation"
      - "Use purchase history for recommendations"

  eliminate:
    prompt: "What can be eliminated?"
    examples:
      - "Eliminate mandatory registration"
      - "Remove unnecessary confirmation steps"

  reverse_rearrange:
    prompt: "What can be reversed or rearranged?"
    examples:
      - "Rearrange checkout to show total first"
      - "Reverse the sign-up flow"
```

### Six Thinking Hats

Parallel thinking from six perspectives.

```yaml
six_hats:
  white_hat:
    focus: "Facts and Information"
    questions:
      - "What data do we have?"
      - "What information is missing?"
      - "What do we know for certain?"

  red_hat:
    focus: "Emotions and Intuition"
    questions:
      - "How do users feel about this?"
      - "What's your gut reaction?"
      - "What frustrations exist?"

  black_hat:
    focus: "Critical Judgment"
    questions:
      - "What could go wrong?"
      - "What are the risks?"
      - "Why might this fail?"

  yellow_hat:
    focus: "Optimistic Value"
    questions:
      - "What are the benefits?"
      - "What's the best outcome?"
      - "Why will this succeed?"

  green_hat:
    focus: "Creative Ideas"
    questions:
      - "What new ideas emerge?"
      - "What alternatives exist?"
      - "What innovations are possible?"

  blue_hat:
    focus: "Process and Summary"
    questions:
      - "What's our conclusion?"
      - "What should we do next?"
      - "What have we learned?"
```

## Workflow

### Step 1: Setup

```yaml
setup:
  1. Load existing requirements from .requirements/{domain}/synthesis/
  2. Identify the domain focus area
  3. Select brainstorming technique
  4. Prepare technique-specific prompts
```

### Step 2: Divergent Phase

```yaml
divergent:
  goal: "Generate maximum ideas without judgment"
  approach:
    - Apply selected technique prompts
    - Generate ideas in rapid succession
    - Build on and combine ideas
    - Capture all ideas without filtering
  output: "Raw idea list (30-50+ ideas typical)"
```

### Step 3: Convergent Phase

```yaml
convergent:
  goal: "Filter, group, and prioritize ideas"
  steps:
    1. Remove duplicates and near-duplicates
    2. Group related ideas into themes
    3. Evaluate feasibility (quick assessment)
    4. Rate value/impact potential
    5. Select top ideas for refinement
```

### Step 4: Refinement Phase

```yaml
refinement:
  goal: "Transform top ideas into requirement candidates"
  for_each_selected_idea:
    - Expand into requirement statement
    - Identify stakeholders affected
    - Note dependencies and constraints
    - Flag for validation with stakeholders
```

### Step 5: Output Generation

```yaml
output:
  brainstorm_session:
    domain: "{domain}"
    technique: "{technique}"
    date: "{ISO-8601}"
    rounds: 2

    raw_ideas:
      total: 47
      by_theme:
        - theme: "Speed/Performance"
          ideas: ["...", "..."]
        - theme: "Personalization"
          ideas: ["...", "..."]

    filtered_ideas:
      total: 18
      top_rated:
        - idea: "One-click reorder for previous purchases"
          theme: "Convenience"
          feasibility: "high"
          impact: "high"
          votes: 5

    requirement_candidates:
      - id: "IDEA-001"
        statement: "Users shall be able to reorder previous purchases with a single click"
        source_idea: "One-click reorder"
        stakeholders: ["returning-customers", "operations"]
        validation_needed: true
```

## Example Session

```text
/requirements-elicitation:brainstorm --domain "food-delivery" --technique reverse

═══════════════════════════════════════════════
BRAINSTORMING SESSION: food-delivery
Technique: Reverse Brainstorming
═══════════════════════════════════════════════

PHASE 1: REVERSE THINKING
"How could we make food delivery WORSE?"

Generating negative ideas...
✗ Make the menu hard to read
✗ Hide delivery fees until checkout
✗ Show inaccurate delivery times
✗ Make it impossible to customize orders
✗ Remove order tracking
✗ Make re-ordering difficult
✗ Ignore dietary preferences
✗ Make splitting bills complicated
... (32 more negative ideas)

PHASE 2: FLIPPING IDEAS

Negative → Positive Requirement:
✗ "Hide fees" → ✓ "Show all fees upfront before adding to cart"
✗ "Inaccurate times" → ✓ "Real-time GPS tracking with accurate ETAs"
✗ "No customization" → ✓ "Full customization with modifier options"
✗ "No tracking" → ✓ "Live order status with driver location"
... (32 more flips)

PHASE 3: GROUPING & FILTERING

Themes identified:
📊 Transparency (8 ideas)
🎯 Customization (6 ideas)
📍 Tracking (5 ideas)
♻️ Convenience (7 ideas)
💰 Pricing (6 ideas)

Top ideas by impact:
1. Show all fees upfront (Transparency, High Impact)
2. Real-time GPS tracking (Tracking, High Impact)
3. One-tap reorder (Convenience, High Impact)
4. Smart dietary filters (Customization, Medium Impact)
5. Easy bill splitting (Convenience, Medium Impact)

PHASE 4: REQUIREMENT CANDIDATES

Generated 12 requirement candidates:
REQ-CAND-001: "System shall display all fees before item is added to cart"
REQ-CAND-002: "System shall provide real-time GPS tracking of delivery driver"
REQ-CAND-003: "System shall enable one-tap reordering of previous orders"
...

═══════════════════════════════════════════════
SESSION COMPLETE
═══════════════════════════════════════════════

Results:
- Raw ideas generated: 40
- Ideas after filtering: 18
- Requirement candidates: 12
- Themes discovered: 5

Saved to: .requirements/food-delivery/brainstorm/BS-20251226-160000.yaml

Next steps:
1. Review candidates with stakeholders
2. Run /simulate to validate from user perspective
3. Add validated requirements to synthesis
```

## Output Locations

```yaml
output_locations:
  session: ".requirements/{domain}/brainstorm/BS-{timestamp}.yaml"
  candidates: ".requirements/{domain}/brainstorm/candidates-{timestamp}.yaml"
```

## Integration with Other Commands

### Before Brainstorming

```bash
# Review existing requirements for context
/requirements-elicitation:gaps --domain "delivery"

# Research domain for inspiration
/requirements-elicitation:research --domain "delivery"
```

### After Brainstorming

```bash
# Validate candidates with stakeholders
/requirements-elicitation:simulate --domain "delivery" --personas end-user

# Add validated candidates to requirements
/requirements-elicitation:discover --domain "delivery" --from-candidates
```

## Error Handling

```yaml
error_handling:
  no_context:
    message: "No domain context available"
    action: "Provide --domain or run /discover first"

  technique_mismatch:
    message: "Selected technique not suitable for domain"
    action: "Suggest alternative technique based on domain"
```
