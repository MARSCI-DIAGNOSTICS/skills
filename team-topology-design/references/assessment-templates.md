# Team Topology Assessment Templates

## Team Assessment Template

### Basic Team Information

```yaml
team_profile:
  name: "{Team Name}"
  type: "{StreamAligned | Platform | Enabling | ComplicatedSubsystem}"
  mission: "{Clear, concise team mission statement}"
  formed_date: "{YYYY-MM-DD}"

  composition:
    total_size: 0
    roles:
      - role: "Software Engineer"
        count: 0
      - role: "QA Engineer"
        count: 0
      - role: "Product Owner"
        count: 0
      - role: "Tech Lead"
        count: 0

  ownership:
    bounded_contexts: []
    services: []
    data_stores: []
    external_integrations: []
```

### Cognitive Load Assessment

```yaml
cognitive_load_assessment:
  team: "{Team Name}"
  assessment_date: "{YYYY-MM-DD}"
  assessor: "{Name}"

  intrinsic_load:
    description: "Complexity inherent to the domain"

    factors:
      domain_complexity:
        score: 0  # 1-5
        evidence: ""
        examples: []

      technical_complexity:
        score: 0  # 1-5
        evidence: ""
        examples: []

      regulatory_complexity:
        score: 0  # 1-5
        evidence: ""
        examples: []

    total_intrinsic: 0  # Sum of factors

  extraneous_load:
    description: "Complexity from poor tooling, processes, environment"

    factors:
      tooling_friction:
        score: 0  # 1-5
        evidence: ""
        pain_points: []

      process_overhead:
        score: 0  # 1-5
        evidence: ""
        pain_points: []

      environment_friction:
        score: 0  # 1-5
        evidence: ""
        pain_points: []

      cross_team_dependencies:
        score: 0  # 1-5
        evidence: ""
        pain_points: []

    total_extraneous: 0  # Sum of factors

  germane_load:
    description: "Cognitive effort for valuable learning"

    factors:
      learning_new_domain:
        score: 0  # 1-5
        evidence: ""

      skill_development:
        score: 0  # 1-5
        evidence: ""

      innovation_exploration:
        score: 0  # 1-5
        evidence: ""

    total_germane: 0  # Sum of factors

  totals:
    intrinsic: 0
    extraneous: 0
    germane: 0
    total: 0  # Should ideally be < 15 for sustainable load

  assessment:
    overall_level: "{Low | Medium | High | Critical}"
    sustainable: true  # false if total > 15
    primary_concern: ""

  recommendations:
    reduce_extraneous:
      - action: ""
        impact: "{High | Medium | Low}"
        effort: "{High | Medium | Low}"

    redistribute_intrinsic:
      - action: ""
        impact: "{High | Medium | Low}"
        effort: "{High | Medium | Low}"
```

### Cognitive Load Scoring Guide

```yaml
scoring_guide:
  domain_complexity:
    1: "Simple, well-understood domain with clear rules"
    2: "Moderately complex, some domain expertise needed"
    3: "Complex domain requiring significant expertise"
    4: "Highly complex with many edge cases and rules"
    5: "Extremely complex, requires deep specialization"

  technical_complexity:
    1: "Standard CRUD operations, simple architecture"
    2: "Some complexity, well-understood patterns"
    3: "Distributed systems, async processing"
    4: "High-performance, real-time, complex integrations"
    5: "Cutting-edge tech, novel solutions required"

  tooling_friction:
    1: "Modern, well-maintained, developer-friendly tools"
    2: "Minor friction, occasional workarounds"
    3: "Regular friction, multiple workarounds needed"
    4: "Significant friction, tools often block progress"
    5: "Major friction, tools actively impede work"

  cross_team_dependencies:
    1: "Fully autonomous, rarely need other teams"
    2: "Occasional dependencies, easily managed"
    3: "Regular dependencies, some coordination needed"
    4: "Frequent dependencies, significant coordination"
    5: "Constant dependencies, blocked without others"
```

## Interaction Assessment Template

### Team Interaction Map

```yaml
interaction_assessment:
  team: "{Team Name}"
  assessment_date: "{YYYY-MM-DD}"

  interactions:
    - with_team: "{Other Team Name}"
      mode: "{Collaboration | X-as-a-Service | Facilitating}"
      direction: "{Inbound | Outbound | Bidirectional}"
      frequency: "{Daily | Weekly | Monthly | Ad-hoc}"
      health: "{Healthy | Strained | Problematic}"

      details:
        purpose: ""
        api_definition: "{Well-defined | Emerging | Undefined}"
        communication_channels: []
        escalation_path: ""

      time_invested:
        hours_per_week: 0
        meetings_per_week: 0
        async_messages_per_week: 0

      issues:
        - description: ""
          impact: "{High | Medium | Low}"
          proposed_resolution: ""

    # Repeat for each team interaction

  summary:
    total_interactions: 0
    collaboration_count: 0
    x_as_a_service_count: 0
    facilitating_count: 0
    total_weekly_hours: 0

  assessment:
    interaction_complexity: "{Low | Medium | High}"
    collaboration_overload: false
    missing_interactions: []
    unnecessary_interactions: []

  recommendations:
    - interaction: "{Team A} <-> {Team B}"
      current_mode: ""
      recommended_mode: ""
      rationale: ""
```

### Interaction Mode Criteria

```yaml
mode_selection_criteria:
  collaboration:
    when_appropriate:
      - "Discovery phase of new capability"
      - "High uncertainty requiring joint exploration"
      - "Undefined interfaces between teams"
      - "Building new shared understanding"

    duration_expectation: "4-12 weeks typical"

    warning_signs:
      - "Collaboration lasting > 6 months"
      - "No clear deliverable or end state"
      - "Same teams always collaborating"

  x_as_a_service:
    when_appropriate:
      - "Well-defined, stable interface"
      - "Consuming team needs capability, not joint discovery"
      - "Provider team can offer standardized service"
      - "Minimal customization required"

    expectations:
      - "Clear API/interface definition"
      - "SLAs and support model"
      - "Self-service where possible"
      - "Versioning strategy"

    warning_signs:
      - "Constant customization requests"
      - "Provider team becoming bottleneck"
      - "Undocumented tribal knowledge"

  facilitating:
    when_appropriate:
      - "Enabling team helping stream-aligned team"
      - "Specific capability or skill gap"
      - "Time-limited engagement"
      - "Goal is capability transfer"

    expectations:
      - "Clear learning objectives"
      - "Graduation criteria defined"
      - "Documentation as deliverable"
      - "Time-boxed engagement"

    warning_signs:
      - "No graduation criteria"
      - "Engagement extending indefinitely"
      - "No knowledge transfer happening"
```

## Team API Template

```yaml
team_api:
  team: "{Team Name}"
  version: "1.0"
  last_updated: "{YYYY-MM-DD}"

  overview:
    mission: "{Team mission statement}"
    value_proposition: "{What we provide to consumers}"
    team_type: "{StreamAligned | Platform | Enabling | ComplicatedSubsystem}"

  services_provided:
    - name: "{Service Name}"
      description: ""
      interface_type: "{REST API | gRPC | Event | UI | Library}"
      documentation_url: ""
      status: "{GA | Beta | Alpha | Deprecated}"

      capabilities:
        - capability: ""
          sla: ""

      getting_started:
        prerequisites: []
        quick_start_guide: ""
        example_usage: ""

  support_model:
    contact_channels:
      - channel: "Slack"
        address: "#team-name-support"
        response_time: "< 4 hours during business hours"
      - channel: "Email"
        address: "team@company.com"
        response_time: "< 1 business day"
      - channel: "JIRA"
        project: "TEAM"
        response_time: "Per SLA tier"

    support_tiers:
      - tier: "P1 - Critical"
        description: "Service down, no workaround"
        response_time: "15 minutes"
        resolution_time: "4 hours"
      - tier: "P2 - High"
        description: "Major feature broken, workaround exists"
        response_time: "1 hour"
        resolution_time: "1 business day"
      - tier: "P3 - Medium"
        description: "Minor issue, not blocking"
        response_time: "4 hours"
        resolution_time: "1 week"
      - tier: "P4 - Low"
        description: "Enhancement, question"
        response_time: "1 business day"
        resolution_time: "Best effort"

    on_call:
      schedule_url: ""
      escalation_path: ""

  preferred_interactions:
    collaboration:
      appetite: "{High | Medium | Low}"
      availability: ""
      engagement_process: ""

    x_as_a_service:
      appetite: "{High | Medium | Low}"
      self_service_url: ""
      onboarding_process: ""

    receiving_facilitation:
      current_needs: []
      preferred_format: ""

  roadmap:
    published_roadmap_url: ""
    feedback_mechanism: ""
    feature_request_process: ""

  team_practices:
    working_hours: ""
    sprint_cadence: ""
    demo_schedule: ""
    office_hours: ""

  dependencies:
    consumes_from:
      - team: "{Other Team}"
        service: ""
        criticality: "{Critical | Important | Nice-to-have}"

    provides_to:
      - team: "{Other Team}"
        service: ""
        usage_level: "{Heavy | Moderate | Light}"
```

## Inverse Conway Assessment Template

```yaml
inverse_conway_assessment:
  assessment_date: "{YYYY-MM-DD}"
  target_architecture: "{Link to architecture documentation}"

  current_state:
    team_count: 0
    team_structure: "{Description of current org structure}"

    teams:
      - name: ""
        type: ""
        bounded_contexts: []
        services_owned: []

  desired_architecture:
    description: ""

    bounded_contexts:
      - name: ""
        description: ""
        key_capabilities: []
        expected_change_frequency: "{High | Medium | Low}"

    communication_patterns:
      - between: ["{Context A}", "{Context B}"]
        pattern: "{Sync | Async | None}"
        coupling: "{Tight | Loose | None}"

  gap_analysis:
    structural_gaps:
      - gap: ""
        current: ""
        desired: ""
        impact: "{High | Medium | Low}"
        resolution: ""

    interaction_gaps:
      - gap: ""
        current: ""
        desired: ""
        impact: "{High | Medium | Low}"
        resolution: ""

    capability_gaps:
      - gap: ""
        missing_skills: []
        resolution: ""

  transformation_plan:
    phases:
      - phase: 1
        name: ""
        duration: ""
        changes:
          team_changes: []
          interaction_changes: []
          service_migrations: []
        success_criteria: []

    risks:
      - risk: ""
        likelihood: "{High | Medium | Low}"
        impact: "{High | Medium | Low}"
        mitigation: ""

    timeline:
      start_date: ""
      phase_1_complete: ""
      phase_2_complete: ""
      target_state: ""
```

## Platform Team Maturity Assessment

```yaml
platform_maturity_assessment:
  platform_team: "{Team Name}"
  assessment_date: "{YYYY-MM-DD}"

  maturity_dimensions:
    self_service:
      level: 0  # 1-5
      evidence: ""

      capabilities:
        - capability: "Provision compute"
          self_service: false
          time_to_provision: ""
        - capability: "Provision database"
          self_service: false
          time_to_provision: ""
        - capability: "Create CI/CD pipeline"
          self_service: false
          time_to_provision: ""
        - capability: "Configure networking"
          self_service: false
          time_to_provision: ""
        - capability: "Access secrets"
          self_service: false
          time_to_provision: ""

    documentation:
      level: 0  # 1-5
      evidence: ""

      assessment:
        getting_started_guide: "{Missing | Outdated | Current}"
        api_reference: "{Missing | Outdated | Current}"
        tutorials: "{Missing | Outdated | Current}"
        troubleshooting_guide: "{Missing | Outdated | Current}"
        architecture_docs: "{Missing | Outdated | Current}"

    developer_experience:
      level: 0  # 1-5
      evidence: ""

      metrics:
        time_to_first_deployment: ""
        developer_satisfaction_score: 0  # 1-10
        support_ticket_volume_trend: "{Increasing | Stable | Decreasing}"

    golden_paths:
      level: 0  # 1-5
      evidence: ""

      paths_available:
        - name: "New Service"
          documentation: ""
          automation_level: "{Full | Partial | Manual}"
          adoption_rate: 0  # percentage

    product_thinking:
      level: 0  # 1-5
      evidence: ""

      practices:
        roadmap_published: false
        user_research_conducted: false
        feedback_mechanisms: []
        metrics_tracked: []

  overall_maturity:
    level: 0  # 1-5, average of dimensions
    assessment: "{Novice | Intermediate | Advanced | Expert}"

  maturity_levels:
    1:
      name: "Novice"
      description: "Ticket-based, manual provisioning, limited docs"
    2:
      name: "Developing"
      description: "Some automation, basic docs, reactive support"
    3:
      name: "Intermediate"
      description: "Partial self-service, good docs, proactive improvements"
    4:
      name: "Advanced"
      description: "Mostly self-service, excellent DX, product roadmap"
    5:
      name: "Expert"
      description: "Full self-service, golden paths, platform-as-product"

  improvement_plan:
    priority_areas:
      - area: ""
        current_level: 0
        target_level: 0
        actions: []
        timeline: ""
```

## Quarterly Review Template

```yaml
quarterly_team_topology_review:
  quarter: "{Q1/Q2/Q3/Q4 YYYY}"
  review_date: "{YYYY-MM-DD}"
  facilitator: "{Name}"
  attendees: []

  team_health_summary:
    teams_assessed: 0

    by_type:
      stream_aligned: 0
      platform: 0
      enabling: 0
      complicated_subsystem: 0

    cognitive_load:
      healthy: 0
      warning: 0
      critical: 0

    key_concerns: []

  interaction_health_summary:
    total_interactions: 0

    by_mode:
      collaboration: 0
      x_as_a_service: 0
      facilitating: 0

    problematic_interactions: []
    interaction_changes_needed: []

  topology_changes:
    last_quarter:
      teams_created: []
      teams_dissolved: []
      teams_reorganized: []
      interaction_mode_changes: []

    planned_next_quarter:
      teams_to_create: []
      teams_to_dissolve: []
      teams_to_reorganize: []
      interaction_changes: []

  platform_health:
    maturity_score: 0
    maturity_trend: "{Improving | Stable | Declining}"
    key_initiatives: []

  action_items:
    - action: ""
      owner: ""
      due_date: ""
      priority: "{High | Medium | Low}"

  next_review_date: "{YYYY-MM-DD}"
```

---

**Last Updated:** 2025-12-26
