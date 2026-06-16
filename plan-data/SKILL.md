---
name: plan-data
description: Create a test data strategy covering synthetic data generation, anonymization, and environment-specific data management. Use for data privacy compliance and test environment setup.
allowed-tools: Read, Write, Glob, Grep, Skill
argument-hint: [project-context]
---

# Plan Test Data Command

Create a comprehensive test data strategy for managing data across test environments.

## Process

### Step 1: Gather Context

Identify project data needs:

- Data entities and relationships
- Sensitive data types (PII, PHI, financial)
- Environment requirements (dev, QA, staging)
- Compliance requirements (GDPR, HIPAA)
- Data volume requirements

### Step 2: Load Skills

Invoke the `test-strategy:test-data-strategy` skill for data management patterns.

### Step 3: Analyze Data Requirements

For each test level:

```markdown
| Level | Data Source | Volume | Refresh |
|-------|-------------|--------|---------|
| Unit | Synthetic | Minimal | Per test |
| Integration | Synthetic + fixtures | Moderate | Per suite |
| E2E | Masked production | Realistic | Weekly |
| Performance | Scaled synthetic | Production-like | Per release |
```

### Step 4: Identify Sensitive Data

Map PII and sensitive fields:

```markdown
| Entity | Field | Sensitivity | Treatment |
|--------|-------|-------------|-----------|
| User | Email | PII | Substitution |
| User | SSN | Highly sensitive | Tokenization |
| Order | CardNumber | Financial | Redaction |
| Log | IP Address | PII | Masking |
```

### Step 5: Design Generation Strategy

Recommend .NET data generation tools:

```csharp
// Bogus for realistic fake data
var customerFaker = new Faker<Customer>()
    .RuleFor(c => c.Name, f => f.Person.FullName)
    .RuleFor(c => c.Email, f => f.Internet.Email())
    .RuleFor(c => c.Phone, f => f.Phone.PhoneNumber());

// AutoFixture for anonymous test data
var fixture = new Fixture();
var order = fixture.Create<Order>();
```

### Step 6: Create Strategy Document

Generate comprehensive data strategy:

```markdown
# Test Data Strategy

## 1. Data Requirements by Level
[Matrix of requirements]

## 2. Data Sources
- Synthetic: Bogus, AutoFixture
- Fixtures: JSON/CSV seed files
- Masked: Anonymized production samples

## 3. Generation Patterns
[Code examples for each entity]

## 4. Anonymization Rules
[PII handling procedures]

## 5. Environment Configuration
- Dev: 100% synthetic
- QA: Masked production subset
- Staging: Full masked clone

## 6. Compliance Checklist
- [ ] GDPR: No real EU data in test
- [ ] HIPAA: PHI de-identified
- [ ] PCI: No real card numbers

## 7. Refresh Procedures
[When and how to refresh data]
```

### Step 7: Output

```markdown
## Test Data Strategy Created

**Entities Covered**: [count]
**Sensitive Fields Identified**: [count]
**Environments Configured**: [list]

**Files Created**:
- [path/to/data-strategy.md]
- [path/to/generators/CustomerFaker.cs]
- [path/to/seed/base-data.json]

**Compliance Status**:
- GDPR: [status]
- HIPAA: [status]
- PCI-DSS: [status]

**Next Steps**:
1. Review anonymization rules
2. Set up data refresh automation
3. Create seed scripts for each environment
```

## Examples

**General strategy:**

```bash
/test-strategy:plan-data
```

**With compliance context:**

```bash
/test-strategy:plan-data healthcare system with HIPAA requirements
```
