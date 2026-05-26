# SaaS Revenue & Growth Metrics Calculator

Use this template to calculate your revenue and retention metrics. Fill in your numbers and calculate each metric.

---

## Revenue Metrics

### Revenue
```
Period: [Month/Quarter/Year]
Total Customer Payments: $_
Revenue = $_
```

### ARPU (Average Revenue Per User)
```
Total Revenue: $_
Total Users: _
ARPU = Total Revenue / Total Users = $_
```

### ARPA (Average Revenue Per Account)
```
MRR: $_
Active Accounts: _
ARPA = MRR / Active Accounts = $_
```

### ARPA/ARPU Analysis
```
ARPA: $_
ARPU: $_
Average Seats per Account = ARPA / ARPU = _
```

### ACV (Annual Contract Value)
```
Annual Recurring Revenue per Contract: $_
(Exclude one-time fees like setup, professional services)
ACV = $_
```

### MRR/ARR
```
Starting MRR: $_

MRR Components:
+ New MRR (new customers): $_
+ Expansion MRR (upsells/cross-sells): $_
- Churned MRR (lost customers): $_
- Contraction MRR (downgrades): $_

Ending MRR: $_
ARR = MRR × 12 = $_
```

### Gross vs. Net Revenue
```
Gross Revenue: $_
- Discounts: $_
- Refunds: $_
- Credits: $_
Net Revenue = $_

Discount Rate = Discounts / Gross Revenue = _%
Refund Rate = Refunds / Gross Revenue = _%
```

---

## Retention & Expansion Metrics

### Churn Rate (Monthly)
```
Logo Churn:
Starting Customers: _
Customers Lost: _
Logo Churn Rate = Customers Lost / Starting Customers = _%

Revenue Churn:
Starting MRR: $_
MRR Lost: $_
Revenue Churn Rate = MRR Lost / Starting MRR = _%
```

**Convert to Annual Churn:**
```
Monthly Churn Rate: _%
Annual Churn Rate = 1 - (1 - Monthly Churn)^12 = _%
```

### NRR (Net Revenue Retention)
```
Starting ARR: $_
+ Expansion Revenue: $_
- Churned Revenue: $_
- Contraction Revenue: $_
Ending ARR (from cohort): $_

NRR = Ending ARR / Starting ARR × 100 = _%
```

### Expansion Revenue
```
Upsells (tier upgrades): $_
Cross-sells (add-ons): $_
Usage growth: $_
Total Expansion Revenue: $_

Expansion as % of MRR = Expansion / Total MRR = _%
```

### Quick Ratio
```
New MRR: $_
Expansion MRR: $_
Churned MRR: $_
Contraction MRR: $_

Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
Quick Ratio = _
```

---

## Analysis Frameworks

### Revenue Mix Analysis
```
Product/Segment A Revenue: $_
Product/Segment B Revenue: $_
Product/Segment C Revenue: $_
Total Revenue: $_

Product A % = _
Product B % = _
Product C % = _
```

### Cohort Retention Analysis
```
Cohort: [Month/Quarter]
Starting Customers: _

Month 0: 100%
Month 1: _%
Month 2: _%
Month 3: _%
Month 6: _%
Month 12: _%
```

---

## Benchmarks & Quality Checks

### Revenue Metrics
- [ ] Gross vs. net revenue clearly labeled
- [ ] Revenue growth rate > cost growth rate
- [ ] ARPU/ARPA tracked by cohort (not just blended)
- [ ] Revenue concentration: Top customer <10%, Top 10 <40%

### Retention Metrics
- [ ] Monthly churn <5% (ideally <2%)
- [ ] Revenue churn vs. logo churn compared
- [ ] NRR >100% (ideally >120%)
- [ ] Quick Ratio >2 (ideally >4)

### Cohort Analysis
- [ ] Recent cohorts perform same or better than older cohorts
- [ ] Revenue retention tracked, not just logo retention
- [ ] Expansion analyzed by cohort

---

## Red Flags

Check if any of these apply:

- [ ] Revenue churn > logo churn (losing big customers)
- [ ] ARPU growing but customer count shrinking (mix shift, not improvement)
- [ ] Newer cohorts churn faster than older cohorts (PMF degradation)
- [ ] NRR <100% (contracting, not expanding)
- [ ] Quick Ratio <2 (leaky bucket)
- [ ] Discounts >20% or refunds >10% (pricing/product problems)
- [ ] Revenue concentration >50% in top 10 customers (risk)
- [ ] Expansion revenue <10% of total MRR (monetization problem)

---

**If you checked any red flags, see SKILL.md Common Pitfalls section for fixes.**
