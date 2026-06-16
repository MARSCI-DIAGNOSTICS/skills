---
name: survey
description: "Generate stakeholder surveys for requirements gathering and analyze responses. Creates questionnaires based on domain context, collects structured feedback, and produces statistical analysis with requirement candidates."
argument-hint: "[--domain <name>] [--mode generate|analyze|both] [--type <survey-type>]"
allowed-tools: Task, Read, Write, Glob, Grep, Skill
---

# Survey Command

Generate requirements surveys and analyze stakeholder responses for data-driven elicitation.

## Usage

```bash
/requirements-elicitation:survey
/requirements-elicitation:survey --domain "checkout"
/requirements-elicitation:survey --domain "auth" --mode generate --type kano
/requirements-elicitation:survey --domain "search" --mode analyze
/requirements-elicitation:survey --domain "onboarding" --mode both --respondents 50
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| --domain | No | Domain for the survey (default: current/most recent) |
| --mode | No | Mode: `generate`, `analyze`, `both` (default: `both`) |
| --type | No | Survey type: `kano`, `satisfaction`, `priority`, `discovery` (default: `discovery`) |
| --respondents | No | Expected number of respondents for analysis (default: 20) |

## Survey Types

### Discovery Survey

General-purpose requirements discovery questionnaire.

```yaml
discovery_survey:
  purpose: "Identify needs, pain points, and desired outcomes"

  sections:
    demographics:
      - "What is your role?"
      - "How often do you use [system]?"
      - "How long have you been a user?"

    current_experience:
      - "Rate your overall satisfaction (1-10)"
      - "What tasks do you perform most frequently?"
      - "What frustrates you most about the current process?"

    needs_and_goals:
      - "What are you trying to accomplish?"
      - "What prevents you from achieving your goals?"
      - "What would make your job easier?"

    feature_preferences:
      - "Which features do you use most?"
      - "Which features do you never use?"
      - "What features are missing?"

    open_ended:
      - "If you could change one thing, what would it be?"
      - "Describe your ideal experience"
      - "Any other feedback?"
```

### Kano Survey

Classify features using Kano methodology.

```yaml
kano_survey:
  purpose: "Classify features as Basic, Performance, or Excitement"

  question_pairs:
    functional:
      prompt: "If [feature] was present, how would you feel?"
      options:
        - "I would like it"
        - "I expect it"
        - "I'm neutral"
        - "I can tolerate it"
        - "I dislike it"

    dysfunctional:
      prompt: "If [feature] was absent, how would you feel?"
      options:
        - "I would like it"
        - "I expect it"
        - "I'm neutral"
        - "I can tolerate it"
        - "I dislike it"

  classification_matrix:
    "Like + Dislike": "Excitement (Delighter)"
    "Like + Neutral": "Excitement"
    "Expect + Dislike": "Basic (Must-Be)"
    "Expect + Neutral": "Performance"
    "Neutral + Neutral": "Indifferent"
    "Dislike + Like": "Reverse"
```

### Satisfaction Survey

Measure satisfaction with current/proposed features.

```yaml
satisfaction_survey:
  purpose: "Gauge satisfaction levels and identify improvement areas"

  scales:
    likert_5:
      - "Strongly Disagree"
      - "Disagree"
      - "Neutral"
      - "Agree"
      - "Strongly Agree"

    satisfaction_10:
      range: "1-10"
      anchors:
        1: "Extremely Dissatisfied"
        5: "Neutral"
        10: "Extremely Satisfied"

    nps:
      question: "How likely are you to recommend [product] to a colleague?"
      range: "0-10"
      categories:
        promoters: "9-10"
        passives: "7-8"
        detractors: "0-6"

  question_categories:
    - "Overall satisfaction"
    - "Feature-specific satisfaction"
    - "Ease of use"
    - "Performance"
    - "Reliability"
    - "Support quality"
```

### Priority Survey

Rank and prioritize features or requirements.

```yaml
priority_survey:
  purpose: "Gather stakeholder input on requirement priorities"

  methods:
    forced_ranking:
      instruction: "Rank these features from most to least important"
      output: "Ordered list by preference"

    pairwise_comparison:
      instruction: "For each pair, select the more important option"
      output: "Win/loss matrix and composite ranking"

    allocation:
      instruction: "You have 100 points. Allocate to features by importance"
      output: "Point distribution showing relative priority"

    moscow_voting:
      instruction: "Classify each feature as Must/Should/Could/Won't"
      options:
        - "Must Have"
        - "Should Have"
        - "Could Have"
        - "Won't Have (this time)"
```

## Workflow

### Generate Mode

```yaml
generate_workflow:
  1. Load domain context from .requirements/{domain}/
  2. Identify survey objectives based on elicitation stage
  3. Select appropriate survey type
  4. Generate questions tailored to domain
  5. Add demographic and contextual questions
  6. Output survey template in multiple formats
```

### Analyze Mode

```yaml
analyze_workflow:
  1. Load response data from .requirements/{domain}/surveys/
  2. Validate response completeness
  3. Perform statistical analysis
  4. Identify patterns and themes
  5. Generate requirement candidates from findings
  6. Output analysis report with visualizations
```

### Both Mode (Default)

```yaml
both_workflow:
  1. Generate survey (if not exists)
  2. Simulate/collect responses (interactive or file input)
  3. Analyze responses
  4. Generate comprehensive report
```

## Output Formats

### Survey Template

```yaml
survey_template:
  metadata:
    domain: "{domain}"
    type: "discovery"
    version: "1.0"
    created: "{ISO-8601}"

  introduction:
    title: "Requirements Survey: {domain}"
    description: "Help us understand your needs for {domain} improvements"
    estimated_time: "10-15 minutes"
    confidentiality: "Responses are anonymous and confidential"

  sections:
    - id: "S1"
      title: "About You"
      questions:
        - id: "Q1"
          type: "single_choice"
          text: "What is your primary role?"
          options:
            - "End User"
            - "Manager"
            - "Administrator"
            - "Developer"
            - "Other"
          required: true

        - id: "Q2"
          type: "scale"
          text: "How often do you use {system}?"
          scale:
            min: 1
            max: 5
            labels:
              1: "Rarely"
              3: "Weekly"
              5: "Daily"

    - id: "S2"
      title: "Current Experience"
      questions:
        - id: "Q3"
          type: "open_text"
          text: "What is your biggest challenge with the current process?"
          max_length: 500

        - id: "Q4"
          type: "multi_choice"
          text: "Which features do you use most? (Select up to 3)"
          options: [...features from domain context...]
          max_selections: 3

  closing:
    thank_you: "Thank you for your valuable feedback!"
    next_steps: "We will analyze responses and share findings within 2 weeks."
```

### Analysis Report

```yaml
analysis_report:
  metadata:
    domain: "{domain}"
    survey_type: "discovery"
    analysis_date: "{ISO-8601}"
    responses_analyzed: 47
    response_rate: "78%"

  demographics:
    role_distribution:
      end_user: 60%
      manager: 25%
      administrator: 10%
      other: 5%
    usage_frequency:
      daily: 45%
      weekly: 35%
      monthly: 15%
      rarely: 5%

  quantitative_results:
    satisfaction_scores:
      overall: 6.2
      ease_of_use: 5.8
      performance: 7.1
      reliability: 6.5

    nps_score: 32
    nps_breakdown:
      promoters: 45%
      passives: 30%
      detractors: 25%

    feature_priorities:
      - feature: "Real-time tracking"
        priority_score: 8.7
        mentions: 38
      - feature: "Mobile access"
        priority_score: 8.2
        mentions: 34

  qualitative_analysis:
    themes:
      - theme: "Speed and Performance"
        frequency: 28
        sentiment: "negative"
        sample_quotes:
          - "The system is too slow during peak hours"
          - "Loading times are frustrating"

      - theme: "Mobile Experience"
        frequency: 22
        sentiment: "mixed"
        sample_quotes:
          - "Would love to use on my phone"
          - "Mobile version is limited"

    pain_points:
      - description: "Slow performance during peak usage"
        severity: "high"
        frequency: 28
        requirement_candidate: "REQ-SURV-001"

      - description: "Lack of mobile functionality"
        severity: "medium"
        frequency: 22
        requirement_candidate: "REQ-SURV-002"

  requirement_candidates:
    - id: "REQ-SURV-001"
      statement: "System shall maintain response times under 2 seconds during peak load"
      source: "Survey analysis - performance theme"
      confidence: "high"
      supporting_data:
        mentions: 28
        avg_severity: 8.2/10

    - id: "REQ-SURV-002"
      statement: "System shall provide mobile-optimized interface for core functions"
      source: "Survey analysis - mobile theme"
      confidence: "high"
      supporting_data:
        mentions: 22
        avg_priority: 8.2/10

  visualizations:
    satisfaction_radar: |
      [Mermaid radar chart of satisfaction dimensions]

    priority_bar: |
      [Mermaid bar chart of feature priorities]

    theme_wordcloud: |
      [Description of common themes]

  recommendations:
    immediate:
      - "Address performance issues (highest severity)"
      - "Conduct follow-up interviews on mobile requirements"

    short_term:
      - "Validate requirement candidates with stakeholders"
      - "Prioritize REQ-SURV-001 and REQ-SURV-002"

    process:
      - "Consider follow-up survey post-implementation"
      - "Establish satisfaction baseline for tracking"
```

## Statistical Analysis Features

### Quantitative Analysis

```yaml
quantitative_analysis:
  descriptive:
    - "Mean, median, mode for scale questions"
    - "Standard deviation for variance"
    - "Frequency distribution for choice questions"

  comparative:
    - "Cross-tabulation by demographics"
    - "Segment comparison (power users vs casual)"
    - "Before/after comparison (if applicable)"

  scoring:
    - "NPS calculation and breakdown"
    - "Kano classification matrix"
    - "Priority ranking aggregation"
    - "Satisfaction index computation"
```

### Qualitative Analysis

```yaml
qualitative_analysis:
  theme_extraction:
    - "Identify recurring topics in open responses"
    - "Categorize by sentiment (positive/negative/neutral)"
    - "Extract representative quotes"

  pattern_detection:
    - "Correlate themes with demographics"
    - "Identify user segments with distinct needs"
    - "Detect contradictions and outliers"

  requirement_generation:
    - "Transform pain points into requirement statements"
    - "Aggregate feature requests into candidates"
    - "Assign confidence levels based on frequency"
```

## Example Session

```text
/requirements-elicitation:survey --domain "helpdesk" --mode both --type discovery

═══════════════════════════════════════════════
REQUIREMENTS SURVEY: helpdesk
Mode: Generate + Analyze
Type: Discovery Survey
═══════════════════════════════════════════════

PHASE 1: SURVEY GENERATION
─────────────────────────────────────────────

Analyzing domain context...
Found: 15 existing requirements, 3 stakeholder personas

Generating survey questions...
✓ Demographics section (4 questions)
✓ Current experience section (6 questions)
✓ Needs and goals section (5 questions)
✓ Feature preferences section (4 questions)
✓ Open-ended section (3 questions)

Survey generated: 22 questions
Estimated completion time: 12 minutes

Saved to: .requirements/helpdesk/surveys/SURV-20251226-180000.yaml

─────────────────────────────────────────────
PHASE 2: RESPONSE COLLECTION
─────────────────────────────────────────────

[Simulating stakeholder responses based on personas...]
- End Users (15 responses)
- Support Agents (8 responses)
- Managers (5 responses)
- Administrators (2 responses)

Total responses collected: 30

─────────────────────────────────────────────
PHASE 3: ANALYSIS
─────────────────────────────────────────────

Quantitative Results:
┌─────────────────────────────────────────┐
│ SATISFACTION SCORES                     │
├─────────────────────────────────────────┤
│ Overall Satisfaction:     6.4/10        │
│ Ease of Use:              5.2/10        │
│ Response Time:            7.1/10        │
│ Self-Service Options:     4.8/10        │
└─────────────────────────────────────────┘

NPS Score: 28 (Passive range)
- Promoters: 40%
- Passives: 33%
- Detractors: 27%

Top Feature Priorities:
1. Knowledge base search (8.9/10)
2. Ticket status tracking (8.5/10)
3. Mobile app access (8.1/10)
4. Chat support (7.8/10)
5. Email integration (7.2/10)

Qualitative Themes:
📊 Self-Service (23 mentions) - "Want to solve issues myself"
📊 Response Time (18 mentions) - "Faster resolution needed"
📊 Mobile Access (15 mentions) - "Need to check tickets on phone"
📊 Knowledge Base (12 mentions) - "Hard to find answers"

Pain Points Identified:
❌ Poor self-service options (high severity)
❌ Knowledge base hard to search (high severity)
❌ No mobile access (medium severity)
❌ Email notifications unreliable (medium severity)

─────────────────────────────────────────────
REQUIREMENT CANDIDATES
─────────────────────────────────────────────

Generated 8 requirement candidates:

REQ-SURV-001: "Users shall be able to search knowledge base
              with natural language queries"
              [Confidence: HIGH | Mentions: 35]

REQ-SURV-002: "System shall provide mobile app for ticket
              management and status tracking"
              [Confidence: HIGH | Mentions: 23]

REQ-SURV-003: "System shall send reliable email notifications
              for ticket status changes"
              [Confidence: MEDIUM | Mentions: 15]

... (5 more candidates)

═══════════════════════════════════════════════
SURVEY ANALYSIS COMPLETE
═══════════════════════════════════════════════

Summary:
- Response rate: 75% (30/40 invited)
- NPS Score: 28
- Top priority: Self-service improvements
- Requirement candidates: 8

Saved to: .requirements/helpdesk/surveys/ANALYSIS-20251226-180000.yaml

Next steps:
1. Review requirement candidates with stakeholders
2. Run /prioritize to rank candidates
3. Run /simulate to validate from user perspective
```

## Output Locations

```yaml
output_locations:
  survey_template: ".requirements/{domain}/surveys/SURV-{timestamp}.yaml"
  analysis_report: ".requirements/{domain}/surveys/ANALYSIS-{timestamp}.yaml"
  raw_responses: ".requirements/{domain}/surveys/responses-{timestamp}.yaml"
  requirement_candidates: ".requirements/{domain}/surveys/candidates-{timestamp}.yaml"
```

## Integration with Other Commands

### Before Survey

```bash
# Gather context for better questions
/requirements-elicitation:research --domain "helpdesk"

# Review existing requirements
/requirements-elicitation:gaps --domain "helpdesk"
```

### After Survey

```bash
# Validate candidates with stakeholder simulation
/requirements-elicitation:simulate --domain "helpdesk" --from-survey

# Prioritize survey-generated candidates
/requirements-elicitation:prioritize --domain "helpdesk" --method wsjf

# Add validated candidates to requirements
/requirements-elicitation:discover --domain "helpdesk" --from-candidates
```

## Response Data Format

For analyzing external survey responses:

```yaml
response_format:
  responses:
    - respondent_id: "R001"
      timestamp: "2025-12-26T10:30:00Z"
      demographics:
        role: "end_user"
        usage_frequency: 4
      answers:
        Q1: "End User"
        Q2: 4
        Q3: "The search function never finds what I need"
        Q4: ["Ticket creation", "Status check", "Knowledge base"]
        Q5: 6
```

## Error Handling

```yaml
error_handling:
  insufficient_responses:
    message: "Not enough responses for reliable analysis (minimum: 10)"
    action: "Collect more responses or use simulation"

  no_domain_context:
    message: "No domain context available"
    action: "Run /discover or provide --domain"

  invalid_response_format:
    message: "Response file format not recognized"
    action: "Check response file matches expected schema"

  low_response_rate:
    message: "Response rate below 20%"
    action: "Consider follow-up or incentives"
```
