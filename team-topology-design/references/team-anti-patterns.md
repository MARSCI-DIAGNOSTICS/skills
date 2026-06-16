# Team Topology Anti-Patterns

## Structural Anti-Patterns

### 1. The Feature Factory

```yaml
anti_pattern:
  name: "Feature Factory"
  description: "Teams measured only by output velocity, not outcomes"

  symptoms:
    - "Story points per sprint as primary metric"
    - "No ownership of production systems"
    - "Handoffs between build and run teams"
    - "No time for technical excellence"
    - "Backlog grows faster than completion"

  root_causes:
    - "Project-based funding model"
    - "Separation of development and operations"
    - "Output-focused management metrics"
    - "No product ownership by teams"

  consequences:
    - technical_debt: "Accumulates rapidly, never addressed"
    - quality: "Degrades over time"
    - morale: "Teams feel like ticket machines"
    - business_value: "Features shipped but outcomes not measured"

  resolution:
    short_term:
      - "Add outcome metrics alongside output metrics"
      - "Allocate 20% time for technical health"
      - "Assign production support to building teams"

    long_term:
      - "Move to product-based funding"
      - "Create stream-aligned teams with full ownership"
      - "Implement SLOs and outcome tracking"

  warning_signs:
    - "We don't have time for refactoring"
    - "That's the ops team's problem"
    - "We just build what's in the backlog"
    - "Velocity is our main KPI"
```

### 2. The Ivory Tower Architecture Team

```yaml
anti_pattern:
  name: "Ivory Tower Architecture"
  description: "Central architecture team designs without building"

  symptoms:
    - "Architecture decisions made without implementation experience"
    - "Long approval cycles for any technical decision"
    - "Architects don't code or operate systems"
    - "Architecture documents rarely match reality"
    - "Teams feel constrained rather than supported"

  root_causes:
    - "Separation of thinking and doing"
    - "Career paths that promote away from coding"
    - "Desire for consistency over effectiveness"
    - "Command-and-control culture"

  consequences:
    - velocity: "Slow decision-making bottlenecks teams"
    - relevance: "Architecture drifts from implementation reality"
    - innovation: "Teams can't experiment or improve"
    - morale: "Developers feel untrusted and disempowered"

  resolution:
    short_term:
      - "Embed architects in stream-aligned teams"
      - "Require architects to code regularly"
      - "Create architecture guilds instead of teams"

    long_term:
      - "Distribute architecture responsibility to teams"
      - "Create enabling architecture practice, not team"
      - "Publish fitness functions, not approval gates"

  warning_signs:
    - "You need architecture approval for that"
    - "That's not how we do things here"
    - "The architecture team will design it, you implement"
    - "We haven't updated the architecture docs in months"
```

### 3. The Shared Services Swamp

```yaml
anti_pattern:
  name: "Shared Services Swamp"
  description: "Monolithic shared services that become bottlenecks"

  symptoms:
    - "One team owns all 'common' functionality"
    - "Queue of requests to shared services team"
    - "Any change requires coordination across many teams"
    - "Shared database accessed by multiple applications"
    - "Tightly coupled 'reusable' components"

  root_causes:
    - "Premature optimization for reuse"
    - "Cost-cutting by consolidation"
    - "Fear of duplication"
    - "Misunderstanding of DRY principle"

  consequences:
    - coupling: "Teams can't change without coordinating"
    - bottleneck: "Shared team can't keep up with demand"
    - fragility: "Changes break multiple consumers"
    - blame: "Issues always involve multiple teams"

  resolution:
    short_term:
      - "Identify highest-friction shared services"
      - "Allow teams to fork rather than wait"
      - "Create clear APIs with versioning"

    long_term:
      - "Move to platform team model with self-service"
      - "Apply DDD to identify true vs false sharing"
      - "Allow bounded duplication for team autonomy"

  warning_signs:
    - "We need to coordinate with the shared services team"
    - "Our change broke three other teams"
    - "We're waiting in the queue for that change"
    - "Everything goes through the common services"
```

### 4. The Component Team Maze

```yaml
anti_pattern:
  name: "Component Team Maze"
  description: "Teams organized by technical layer, not value stream"

  symptoms:
    - "Frontend team, backend team, database team"
    - "Multiple teams required for any feature"
    - "Handoffs and waiting between teams"
    - "Each team optimizes their layer locally"
    - "Integration problems discovered late"

  root_causes:
    - "Historical technical specialization"
    - "Belief that layers need dedicated expertise"
    - "Matrix organization with skill-based groups"
    - "Career paths tied to technical specialization"

  consequences:
    - lead_time: "Features take weeks due to handoffs"
    - ownership: "No team owns the full user experience"
    - quality: "Integration issues fall through cracks"
    - blame: "Finger-pointing between layer teams"

  resolution:
    short_term:
      - "Create cross-functional feature teams for key flows"
      - "Embed specialists in product teams temporarily"
      - "Measure end-to-end lead time, not layer throughput"

    long_term:
      - "Reorganize around value streams"
      - "Create stream-aligned teams with full-stack capability"
      - "Maintain communities of practice for skill sharing"

  warning_signs:
    - "The frontend team is waiting for the backend API"
    - "We need three teams to ship this feature"
    - "Each team did their part, but integration failed"
    - "Who owns this end-to-end? Nobody?"
```

## Interaction Anti-Patterns

### 5. The Collaboration Overload

```yaml
anti_pattern:
  name: "Collaboration Overload"
  description: "Too many teams in permanent collaboration mode"

  symptoms:
    - "Every change requires multiple team meetings"
    - "Shared Slack channels with 50+ people"
    - "Stand-ups that take an hour"
    - "Calendar filled with cross-team syncs"
    - "Can't remember which team owns what"

  root_causes:
    - "Unclear boundaries between teams"
    - "Lack of well-defined team APIs"
    - "Fear of making decisions alone"
    - "Consensus culture taken to extreme"

  consequences:
    - throughput: "Decisions take forever"
    - context_switching: "Constant interruptions"
    - accountability: "Diffused responsibility"
    - burnout: "Meeting fatigue across teams"

  resolution:
    short_term:
      - "Reduce meeting frequency and size"
      - "Define clear team boundaries and APIs"
      - "Establish decision rights per team"

    long_term:
      - "Move appropriate interactions to X-as-a-Service"
      - "Use async communication for non-urgent matters"
      - "Define explicit collaboration periods (time-boxed)"

  expected_collaboration_duration: "Typically 6-12 weeks maximum"

  warning_signs:
    - "Let's get everyone in a room to discuss"
    - "We need to check with five other teams"
    - "Our whole day is meetings"
    - "Which Slack channel should I ask in?"
```

### 6. The Platform That Isn't

```yaml
anti_pattern:
  name: "Platform That Isn't"
  description: "Platform team that requires tickets rather than self-service"

  symptoms:
    - "Request a database via Jira ticket"
    - "Wait 2 weeks for environment provisioning"
    - "Platform team manually provisions resources"
    - "Documentation is outdated or missing"
    - "Every request needs platform team intervention"

  root_causes:
    - "Platform team understaffed"
    - "No investment in self-service tooling"
    - "Control mindset rather than enablement"
    - "Platform built without customer feedback"

  consequences:
    - velocity: "Stream-aligned teams blocked on platform"
    - frustration: "Shadow IT and workarounds emerge"
    - toil: "Platform team drowns in manual work"
    - value: "Platform doesn't actually accelerate teams"

  resolution:
    short_term:
      - "Document common requests and create runbooks"
      - "Automate top 3 most frequent requests"
      - "Create feedback channel from stream teams"

    long_term:
      - "Build true self-service with golden paths"
      - "Treat platform as internal product with roadmap"
      - "Measure success by consumer team velocity"

  platform_thinnest_viable_test:
    question: "Can a team provision everything they need without talking to platform team?"
    good_answer: "Yes, via self-service portal and APIs"
    bad_answer: "No, they need to submit requests"

  warning_signs:
    - "Submit a ticket and we'll get to it"
    - "We need to manually configure that"
    - "The platform team is the bottleneck"
    - "We built our own solution because platform was too slow"
```

### 7. The Enabling Team That Doesn't Enable

```yaml
anti_pattern:
  name: "Enabling Team That Doesn't Enable"
  description: "Enabling team becomes permanent dependency"

  symptoms:
    - "Stream teams always need enabling team help"
    - "Knowledge stays with enabling team"
    - "No skills transfer to stream teams"
    - "Enabling team owns production issues"
    - "Same problems repeat across teams"

  root_causes:
    - "Enabling team measured on tasks completed, not capability built"
    - "Stream teams happy to offload work"
    - "No explicit enablement duration limits"
    - "Insufficient documentation and training"

  consequences:
    - scalability: "Enabling team becomes bottleneck"
    - autonomy: "Stream teams remain dependent"
    - cost: "Duplicate expertise required permanently"
    - growth: "Teams don't develop new capabilities"

  resolution:
    short_term:
      - "Set explicit time limits on engagements"
      - "Measure capability transfer, not tasks done"
      - "Require documentation as deliverable"

    long_term:
      - "Define graduation criteria for each engagement"
      - "Sunset enabling team when capability spread"
      - "Move to community of practice model"

  healthy_enabling_pattern:
    phases:
      - "Assess: 1-2 weeks identifying gaps"
      - "Enable: 4-8 weeks intensive coaching"
      - "Support: 2-4 weeks answering questions"
      - "Graduate: Team is self-sufficient"
    duration: "3-6 months maximum per engagement"

  warning_signs:
    - "We always need the SRE team to help"
    - "Only the enabling team knows how to do that"
    - "We've been 'enabling' this team for 2 years"
    - "Can you just do it for us?"
```

## Cognitive Load Anti-Patterns

### 8. The Everything Team

```yaml
anti_pattern:
  name: "Everything Team"
  description: "Team responsible for too many domains/services"

  symptoms:
    - "Team owns 15+ microservices"
    - "Context switching between unrelated domains"
    - "Shallow knowledge across many areas"
    - "Constant firefighting across services"
    - "Can't go deep on any one thing"

  cognitive_load_indicators:
    services_per_developer: "> 3 is warning sign"
    domain_count: "> 2 bounded contexts is concerning"
    oncall_variety: "Pages for unrelated systems"
    meeting_context_switches: "Multiple domains per day"

  root_causes:
    - "Team grew by absorbing orphaned services"
    - "Cost-cutting reduced team count"
    - "No clear service ownership model"
    - "Technical rather than domain boundaries"

  consequences:
    - quality: "Shallow understanding leads to bugs"
    - morale: "Team feels overwhelmed"
    - velocity: "Constant context switching"
    - expertise: "Jack of all trades, master of none"

  resolution:
    short_term:
      - "Inventory all team responsibilities"
      - "Identify top 3 domains by business value"
      - "Freeze expansion, focus on core"

    long_term:
      - "Split team along domain boundaries"
      - "Transfer services to appropriate teams"
      - "Retire or consolidate low-value services"

  warning_signs:
    - "I don't remember how that service works"
    - "We own too much to do any of it well"
    - "Another service got dumped on us"
    - "We're spread too thin"
```

### 9. The Fracture Plane Failure

```yaml
anti_pattern:
  name: "Fracture Plane Failure"
  description: "Team boundaries don't align with natural system boundaries"

  symptoms:
    - "One service split across multiple teams"
    - "Tightly coupled services owned by different teams"
    - "Database shared by multiple team services"
    - "Every change requires multi-team coordination"

  root_causes:
    - "Teams formed before architecture understood"
    - "Org changes without service realignment"
    - "Technical debt in coupling ignored"
    - "Cost of splitting deemed too high"

  fracture_plane_types:
    business_domain: "Bounded contexts from DDD"
    regulatory: "Compliance boundaries (PCI, HIPAA)"
    change_cadence: "Parts that change together"
    team_location: "Geography and timezone"
    risk: "Failure isolation requirements"
    performance: "Scalability requirements"
    technology: "Different tech stacks"
    user_persona: "Different user types"

  consequences:
    - coordination: "Constant cross-team dependency"
    - velocity: "Can't change without alignment"
    - ownership: "Unclear accountability"
    - architecture: "Natural boundaries remain ignored"

  resolution:
    short_term:
      - "Map current boundaries vs natural fracture planes"
      - "Identify highest-friction misalignments"
      - "Create facade APIs to reduce coupling"

    long_term:
      - "Refactor services along fracture planes"
      - "Realign team boundaries to match"
      - "Use Inverse Conway to guide architecture"

  warning_signs:
    - "This service is partly ours, partly theirs"
    - "We share a database with two other teams"
    - "We can't deploy without the other team"
    - "Our boundaries make no business sense"
```

## Recovery Strategies

### Assessment Questions

```yaml
assessment:
  structural_health:
    - "How many teams are required to deliver a typical feature?"
    - "What's the average lead time from idea to production?"
    - "How much time is spent in cross-team coordination?"
    - "Can teams deploy independently?"

  interaction_health:
    - "What percentage of time is spent in meetings?"
    - "How long do teams stay in collaboration mode?"
    - "Is the platform truly self-service?"
    - "Do enabling teams have graduation criteria?"

  cognitive_load_health:
    - "How many services does each developer own?"
    - "How many domains does each team span?"
    - "Can team members explain their domain deeply?"
    - "How often do teams context switch?"
```

### Anti-Pattern Detection Checklist

```yaml
detection_checklist:
  weekly_team_health:
    - "Did we ship without coordinating with other teams?"
    - "Did we avoid multi-team meetings for routine work?"
    - "Did our platform requests get self-served?"
    - "Did we stay focused on our core domain?"

  monthly_review:
    - "Are our team boundaries still sensible?"
    - "Is our cognitive load sustainable?"
    - "Are collaboration relationships evolving?"
    - "Is the platform getting more self-service?"

  quarterly_assessment:
    - "Run full Team Topologies assessment"
    - "Review fracture planes vs team boundaries"
    - "Assess platform maturity"
    - "Plan any team restructuring needed"
```

---

**Last Updated:** 2025-12-26
