---
name: runbook-creation
description: Operational runbook templates for incident response and procedures
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Runbook Creation Skill

## When to Use This Skill

Use this skill when:

- **Runbook Creation tasks** - Working on operational runbook templates for incident response and procedures
- **Planning or design** - Need guidance on Runbook Creation approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create operational runbooks for incident response, maintenance procedures, and operational tasks.

## MANDATORY: Documentation-First Approach

Before creating runbooks:

1. **Invoke `docs-management` skill** for runbook patterns
2. **Verify SRE best practices** via MCP servers (perplexity)
3. **Base guidance on Google SRE principles**

## Runbook Types

```text
Runbook Categories:

┌─────────────────────────────────────────────────────────────────────────────┐
│  Incident Response Runbooks                                                  │
│  • Alert-triggered procedures                                                │
│  • Escalation paths                                                          │
│  • Communication templates                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Operational Runbooks                                                        │
│  • Deployment procedures                                                     │
│  • Maintenance tasks                                                         │
│  • Backup/restore operations                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Troubleshooting Runbooks                                                    │
│  • Diagnostic procedures                                                     │
│  • Common issue resolution                                                   │
│  • Debug workflows                                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Emergency Runbooks                                                          │
│  • Disaster recovery                                                         │
│  • Security incident response                                                │
│  • Business continuity                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Standard Runbook Template

```markdown
# Runbook: [TITLE]

| Property | Value |
|----------|-------|
| **ID** | RB-[NUMBER] |
| **Category** | [Incident/Operational/Troubleshooting/Emergency] |
| **Service** | [Service Name] |
| **Owner** | [Team/Individual] |
| **Last Updated** | [YYYY-MM-DD] |
| **Last Tested** | [YYYY-MM-DD] |
| **Review Frequency** | [Quarterly/Monthly/Annually] |

---

## Overview

**Purpose:** [What this runbook helps you accomplish]

**When to Use:** [Conditions that trigger this runbook]

**Expected Outcome:** [What success looks like]

**Estimated Duration:** [Time to complete]

---

## Prerequisites

### Required Access

- [ ] [System/Tool 1] - [Role/Permission needed]
- [ ] [System/Tool 2] - [Role/Permission needed]

### Required Knowledge

- [Skill/Knowledge 1]
- [Skill/Knowledge 2]

### Tools Needed

| Tool | Purpose | Access URL |
|------|---------|------------|
| [Tool 1] | [Purpose] | [URL/Link] |
| [Tool 2] | [Purpose] | [URL/Link] |

---

## Quick Reference

```text
Quick Commands:
┌────────────────────────────────────────────────────────────────┐
│ Check service status: kubectl get pods -n [namespace]          │
│ View logs: kubectl logs -f [pod-name] -n [namespace]           │
│ Restart service: kubectl rollout restart deployment/[name]     │
│ Check metrics: [monitoring-url]                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Procedure

### Step 1: [Step Name]

**Objective:** [What this step accomplishes]

**Actions:**

1. [Action 1]

   ```bash
   # Command example
   kubectl get pods -n production
   ```

2. [Action 2]

**Expected Result:** [What you should see]

**If This Fails:** Go to [Troubleshooting Section](#troubleshooting)

---

### Step 2: [Step Name]

**Objective:** [What this step accomplishes]

**Actions:**

1. [Action 1]
2. [Action 2]

**Decision Point:**

```text
┌─────────────────────────────────────┐
│ Is the service responding?          │
│                                     │
│ YES → Continue to Step 3            │
│ NO  → Go to Step 4 (Escalation)     │
└─────────────────────────────────────┘
```

---

### Step 3: [Verification]

**Objective:** Verify the issue is resolved

**Verification Checklist:**

- [ ] Service is responding to health checks
- [ ] Metrics show normal values
- [ ] No new errors in logs
- [ ] Users can access the service

---

## Troubleshooting

### Issue: [Common Issue 1]

**Symptoms:** [What you observe]

**Cause:** [Root cause]

**Resolution:**

1. [Step 1]
2. [Step 2]

### Issue: [Common Issue 2]

**Symptoms:** [What you observe]

**Cause:** [Root cause]

**Resolution:**

1. [Step 1]
2. [Step 2]

---

## Escalation

### When to Escalate

- [ ] Issue not resolved after [X] minutes
- [ ] Impact affects [threshold]
- [ ] Required access not available
- [ ] Unsure of next steps

### Escalation Path

| Level | Contact | Method | Response Time |
|-------|---------|--------|---------------|
| L1 | On-call Engineer | PagerDuty | 15 min |
| L2 | Team Lead | Slack #incidents | 30 min |
| L3 | Engineering Manager | Phone | 1 hour |
| L4 | VP Engineering | Phone | As needed |

---

## Communication

### Status Updates

**Template:**

```text
[TIMESTAMP] - [SERVICE] - [STATUS]

Current Status: [Investigating/Identified/Monitoring/Resolved]
Impact: [Description of user impact]
Next Update: [Time of next update]

Actions Taken:
- [Action 1]
- [Action 2]

Next Steps:
- [Planned action]
```

### Stakeholder Notification

| Stakeholder | When to Notify | Method |
|-------------|----------------|--------|
| Engineering | Immediately | Slack |
| Product | If user-impacting | Slack |
| Support | If customer-facing | Email |
| Leadership | If SEV1/SEV2 | Phone |

---

## Post-Incident

### Cleanup Tasks

- [ ] Remove any temporary fixes
- [ ] Update monitoring/alerts if needed
- [ ] Document any new learnings

### Post-Incident Review

- [ ] Schedule post-mortem meeting
- [ ] Gather timeline and evidence
- [ ] Identify action items

---

## Appendix

### Related Runbooks

- [RB-XXX: Related Runbook 1]
- [RB-YYY: Related Runbook 2]

### Reference Documentation

- [Link to architecture docs]
- [Link to service docs]

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial version |
| 1.1 | [Date] | [Name] | [Changes] |

```text

```

## Incident Response Runbook Template

```markdown
# Incident Runbook: [Alert Name]

| Property | Value |
|----------|-------|
| **Alert** | [Alert Name/ID] |
| **Severity** | [SEV1/SEV2/SEV3/SEV4] |
| **Service** | [Service Name] |
| **SLO Impact** | [Which SLO is affected] |

---

## Alert Details

**Trigger Condition:**
```text

[Alert query/condition]
Example: error_rate > 1% for 5 minutes

```

**Alert Meaning:** [What this alert indicates]

**False Positive Indicators:** [Signs this might be a false alarm]

---

## Immediate Actions (First 5 Minutes)

### 1. Acknowledge Alert

```bash
# Acknowledge in PagerDuty
pd incident:acknowledge

# Or via Slack
/pd ack
```

### 2. Assess Impact

**Quick Health Checks:**

```bash
# Check service status
curl -s https://api.example.com/health | jq .

# Check error rate
kubectl logs -l app=service --tail=100 | grep -c ERROR

# Check pod status
kubectl get pods -n production -l app=service
```

**Impact Assessment:**

| Check | Command | Expected | Actual |
|-------|---------|----------|--------|
| Health endpoint | `curl /health` | 200 OK | [Result] |
| Error rate | `grep ERROR` | < 10 | [Result] |
| Pod status | `kubectl get pods` | Running | [Result] |

### 3. Initial Communication

Post in #incidents:

```text
🔴 INCIDENT: [Service] - [Brief Description]
Severity: [SEV level]
Impact: [User impact]
Status: Investigating
Lead: @[your-name]
```

---

## Diagnosis

### Common Causes and Checks

#### Cause 1: High Traffic

```bash
# Check request rate
kubectl top pods -n production -l app=service

# Check HPA status
kubectl get hpa -n production
```

**If traffic spike confirmed:**

- Scale replicas: `kubectl scale deployment/service --replicas=10`
- Enable rate limiting if available

#### Cause 2: Database Issues

```bash
# Check database connections
kubectl exec -it [pod] -- psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check slow queries
kubectl logs -l app=service | grep "slow query"
```

**If database issues:**

- Check connection pool exhaustion
- Look for long-running queries
- Consider read replica failover

#### Cause 3: Dependency Failure

```bash
# Check external dependencies
curl -s https://status.dependency.com/api/v2/status.json | jq .

# Check circuit breaker status
kubectl logs -l app=service | grep "circuit"
```

**If dependency failure:**

- Verify external service status
- Check for timeout configuration
- Consider enabling fallback behavior

---

## Resolution Steps

### Quick Fixes

| Issue | Quick Fix | Command |
|-------|-----------|---------|
| Pod crash loop | Restart deployment | `kubectl rollout restart deployment/service` |
| Memory pressure | Increase limits | `kubectl edit deployment/service` |
| Config error | Rollback config | `kubectl rollout undo deployment/service` |

### Rollback Procedure

```bash
# List recent deployments
kubectl rollout history deployment/service -n production

# Rollback to previous version
kubectl rollout undo deployment/service -n production

# Rollback to specific revision
kubectl rollout undo deployment/service -n production --to-revision=2
```

---

## Resolution Verification

**Verification Checklist:**

- [ ] Alert has cleared
- [ ] Health checks passing
- [ ] Error rate below threshold
- [ ] No user complaints in support channels
- [ ] Metrics returning to baseline

**Monitoring Period:** Monitor for 15 minutes after resolution

---

## Closure

### Update Status

```text
✅ RESOLVED: [Service] - [Brief Description]
Duration: [X] minutes
Root Cause: [Brief cause]
Resolution: [What fixed it]
Follow-up: [Any action items]
```

### Post-Incident Tasks

- [ ] Update incident timeline
- [ ] Create post-mortem doc if SEV1/SEV2
- [ ] File tickets for follow-up work
- [ ] Update runbook if needed

```text

```

## Database Failover Runbook

```markdown
# Runbook: Database Failover

| Property | Value |
|----------|-------|
| **ID** | RB-DB-001 |
| **Category** | Emergency |
| **Service** | PostgreSQL Primary |
| **Owner** | Platform Team |
| **Last Tested** | 2025-01-15 |

---

## Overview

**Purpose:** Failover from primary database to replica when primary is unavailable.

**When to Use:**
- Primary database unresponsive for > 5 minutes
- Primary database corruption detected
- Planned maintenance requiring failover

**Expected Outcome:** Application traffic routed to new primary

**Estimated Duration:** 15-30 minutes

---

## Prerequisites

### Required Access

- [ ] Azure Portal - Contributor on resource group
- [ ] kubectl - cluster-admin
- [ ] Database credentials - postgres superuser

### Pre-Failover Checks

```bash
# Verify replica is healthy and caught up
az postgres flexible-server replica list --resource-group rg-prod --name pg-primary

# Check replication lag
psql -h pg-replica.postgres.database.azure.com -U postgres -c \
  "SELECT pg_last_wal_receive_lsn() - pg_last_wal_replay_lsn() AS lag_bytes;"
```

**Acceptable lag:** < 1MB

---

## Failover Procedure

### Step 1: Confirm Primary is Unavailable

```bash
# Test primary connectivity
psql -h pg-primary.postgres.database.azure.com -U postgres -c "SELECT 1;"

# Check Azure status
az postgres flexible-server show --resource-group rg-prod --name pg-primary --query "state"
```

**Expected:** Connection timeout or error state

### Step 2: Notify Stakeholders

```text
🔴 DATABASE FAILOVER INITIATED
Target: pg-primary → pg-replica
Reason: [Primary unavailable/Maintenance/etc.]
Expected Downtime: 5-10 minutes
```

### Step 3: Promote Replica

```bash
# Promote replica to primary (Azure Flexible Server)
az postgres flexible-server replica stop-replication \
  --resource-group rg-prod \
  --name pg-replica

# Verify promotion
az postgres flexible-server show \
  --resource-group rg-prod \
  --name pg-replica \
  --query "replicationRole"
```

**Expected:** `replicationRole: None` (standalone)

### Step 4: Update Connection Strings

```bash
# Update Kubernetes secret
kubectl create secret generic db-connection \
  --from-literal=host=pg-replica.postgres.database.azure.com \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart applications to pick up new connection
kubectl rollout restart deployment -l uses-database=true -n production
```

### Step 5: Verify Application Connectivity

```bash
# Check application logs
kubectl logs -l app=api-service --tail=50 | grep -i database

# Test application health
curl -s https://api.example.com/health | jq .database
```

---

## Post-Failover

### Immediate Tasks

- [ ] Verify all applications connected to new primary
- [ ] Check for data consistency
- [ ] Monitor error rates

### Recovery Tasks (Next 24 Hours)

- [ ] Investigate original primary failure
- [ ] Create new replica from new primary
- [ ] Update DNS/connection strings permanently
- [ ] Document incident and learnings

---

## Rollback

If failover causes issues:

```bash
# If original primary is recoverable
# Stop writes to new primary
kubectl scale deployment --replicas=0 -l uses-database=true -n production

# Restore original primary
az postgres flexible-server update --resource-group rg-prod --name pg-primary --state Enabled

# Revert connection strings
kubectl create secret generic db-connection \
  --from-literal=host=pg-primary.postgres.database.azure.com \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart applications
kubectl rollout restart deployment -l uses-database=true -n production
```

```text

```

## Runbook Quality Checklist

| Criterion | Description | Check |
|-----------|-------------|-------|
| **Actionable** | Every step has a specific action | [ ] |
| **Testable** | Can be practiced in non-prod | [ ] |
| **Current** | Reflects current system state | [ ] |
| **Complete** | Covers happy and error paths | [ ] |
| **Accessible** | Available during incidents | [ ] |
| **Versioned** | Changes tracked with dates | [ ] |

## Workflow

When creating runbooks:

1. **Identify Need**: What operation/incident needs documentation?
2. **Gather Information**: Interview operators, review past incidents
3. **Draft Runbook**: Use appropriate template
4. **Validate Steps**: Walk through with subject matter expert
5. **Test in Non-Prod**: Execute runbook in staging
6. **Publish**: Add to runbook collection
7. **Train Team**: Ensure operators know where to find it
8. **Maintain**: Review and update regularly

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
