# TOGAF 10 ADM Phases Quick Reference

## ADM Cycle Overview

The Architecture Development Method (ADM) is the core of TOGAF, providing a tested and repeatable process for developing architectures.

## Phase Summary

| Phase | Name | Purpose | Duration |
| --- | --- | --- | --- |
| Preliminary | Architecture Capability | Establish EA practice | Once (setup) |
| A | Architecture Vision | Define scope and get buy-in | 2-4 weeks |
| B | Business Architecture | Document business needs | 4-8 weeks |
| C | Information Systems | Data + Application architecture | 6-12 weeks |
| D | Technology Architecture | Infrastructure design | 4-8 weeks |
| E | Opportunities & Solutions | Identify projects | 2-4 weeks |
| F | Migration Planning | Create roadmap | 2-4 weeks |
| G | Implementation Governance | Oversee execution | Ongoing |
| H | Architecture Change Mgmt | Evolve architecture | Ongoing |

## Minimal Viable Cycle

For smaller projects, use a lightweight ADM:

1. **Vision (A)** - What are we trying to achieve?
2. **Design (C/D)** - What's the technical approach?
3. **Plan (F)** - How do we get there?
4. **Execute (G)** - Build it right

## Key Artifacts Per Phase

### Phase A Artifacts

- Architecture Vision document
- Stakeholder map
- Statement of Architecture Work

### Phase B Artifacts

- Business process models
- Capability maps
- Organization structure

### Phase C Artifacts

- Data models
- Application portfolio
- Integration specifications

### Phase D Artifacts

- Technology standards
- Infrastructure diagrams
- Platform specifications

### Phase E Artifacts

- Work packages
- Transition architectures
- Build vs. buy decisions

### Phase F Artifacts

- Implementation roadmap
- Migration plan
- Resource estimates

## When to Skip Phases

- **Skip Preliminary**: Already have established EA practice
- **Skip B**: Pure technical modernization with stable business
- **Skip C**: Infrastructure-only changes
- **Lightweight E-F**: Obvious single project approach

## Integration with Agile

- Each phase can be treated as an agile "epic"
- Phase work can be decomposed into stories
- ADRs capture decisions incrementally
- Architecture evolves through sprints

## Reference

Based on TOGAF Standard, Version 10 by The Open Group.
