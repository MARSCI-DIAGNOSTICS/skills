# Zachman Framework 3.0 Quick Reference

## The Matrix Concept

Zachman is a 6x6 classification schema that organizes architecture artifacts by:

- **Rows**: Stakeholder perspectives (from executive to operator)
- **Columns**: Fundamental questions (what, how, where, who, when, why)

## Column Quick Reference (Interrogatives)

| Column | Question | Focus Area | Example Artifacts |
| --- | --- | --- | --- |
| 1 | What? | Data/Inventory | Entity models, data dictionaries |
| 2 | How? | Process/Function | Process flows, algorithms |
| 3 | Where? | Network/Location | Network diagrams, deployment |
| 4 | Who? | People/Organization | Org charts, RACI matrices |
| 5 | When? | Time/Schedule | Event models, timelines |
| 6 | Why? | Motivation/Rules | Goals, business rules |

## Row Quick Reference (Perspectives)

| Row | Perspective | Audience | Detail Level |
| --- | --- | --- | --- |
| 1 | Planner | Executives | Scope/Context |
| 2 | Owner | Business managers | Business model |
| 3 | Designer | Architects | Logical design |
| 4 | Builder | Developers | Physical design |
| 5 | Subcontractor | Implementers | Detailed specs |
| 6 | User | Operators | Running system |

## Practical Usage

### As a Checklist

Use the matrix to check documentation completeness:

```text
         What  How   Where  Who   When  Why
Planner   [ ]   [ ]   [ ]   [ ]   [ ]   [ ]
Owner     [ ]   [ ]   [ ]   [ ]   [ ]   [ ]
Designer  [x]   [x]   [x]   [ ]   [ ]   [x]
Builder   [x]   [x]   [x]   [x]   [ ]   [x]
```

### Minimum Viable Coverage

At minimum, document:

- Row 3-4, Column 1-2: System design (What & How)
- Row 4, Column 6: Technical decisions (Why - via ADRs)

### For Specific Analysis

1. Identify the audience (row)
2. Identify the question (column)
3. Locate or create the appropriate artifact

## Key Insight

- **TOGAF** tells you HOW to create architecture
- **Zachman** tells you HOW TO ORGANIZE what you create

They are complementary, not competing frameworks.

## Common Mistakes

1. Trying to fill every cell (36 artifacts is excessive for most projects)
2. Confusing it with a methodology (it's a taxonomy)
3. Ignoring row 4-5 (the most code-extractable rows)
4. Over-investing in row 1-2 without business stakeholder involvement

## Reference

Based on Zachman Framework Standard, Version 3.0 by ZIFA.
