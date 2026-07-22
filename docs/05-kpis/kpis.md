# KPIs & Metrics

## Overview

Key Performance Indicators (KPIs) are measurable values that track progress toward strategic objectives. This document defines the core KPIs for the Kidney Care Analytics Platform organized by business domain and stakeholder perspective.

---

## Clinical Quality KPIs

### 1. Treatment Adequacy

**Definition:** Measure of whether prescribed treatment is actually delivered.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Treatment Delivered %** | (Actual Treatment Time / Intended Treatment Time) × 100 | % | ≥95% | Per session |
| **KT/V** | (Dialyzer clearance × Time) / Patient's Volume of Distribution | Units | ≥1.2 (HD), ≥1.7 (weekly PD) | Monthly |
| **URR (Urea Reduction Ratio)** | ((Predialysis BUN - Postdialysis BUN) / Predialysis BUN) × 100 | % | ≥65% | Monthly |
| **Session Completion Rate** | (Completed Sessions / Scheduled Sessions) × 100 | % | ≥98% | Daily/Weekly |

**Use Case:** Nephrologists monitor treatment adequacy to ensure prescribed therapy is delivered; affects patient outcomes.

---

### 2. Patient Safety & Complications

**Definition:** Frequency and severity of adverse events and complications.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Peritonitis Rate (PD)** | (Number of peritonitis episodes / Number of patient-months) × 1000 | Episodes/1000 patient-months | <0.5 | Monthly |
| **Exit Site Infection Rate (PD)** | (Number of ESI episodes / Number of patient-months) × 1000 | Episodes/1000 patient-months | <0.5 | Monthly |
| **Hypotensive Incident Rate** | (Number of intradialytic hypotension events / Number of sessions) × 100 | % | <5% | Weekly |
| **Hospitalization Rate** | (Number of hospitalizations / Total patient-months) × 12 | Hospitalizations/patient-year | <2 | Monthly |
| **30-Day Readmission Rate** | (Readmitted within 30 days / Total discharges) × 100 | % | <10% | Monthly |

**Use Case:** Quality directors and CMO track safety metrics for accreditation, compliance, and quality improvement.

---

### 3. Clinical Outcomes

**Definition:** Long-term patient health outcomes.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Survival Rate (1-year)** | (Living patients at 1 year / Cohort start size) × 100 | % | ≥95% | Annually |
| **Survival Rate (2-year)** | (Living patients at 2 years / Cohort start size) × 100 | % | ≥85% | Annually |
| **Transplant Rate** | (Patients receiving transplants / Total candidates) × 100 | % | >15% annually | Quarterly |
| **Infection-Related Mortality Rate** | (Infection-related deaths / Total patient-months) × 100 | Deaths/100 patient-months | <0.1 | Quarterly |
| **Cardiovascular Hospitalization Rate** | (CV hospitalizations / Total patient-months) × 12 | CV Hosp/patient-year | <1 | Quarterly |

**Use Case:** CMO, Quality leadership track patient outcomes; comparative analytics for market positioning.

---

### 4. Comorbidity Management

**Definition:** Control of comorbid conditions affecting dialysis outcomes.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Blood Pressure Control %** | (Sessions with BP <140/90 / Total sessions) × 100 | % | ≥70% | Weekly |
| **Anemia Control %** | (Patients with Hgb 10-12 g/dL / Total on ESA) × 100 | % | ≥80% | Monthly |
| **Bone Health: PTH Control %** | (Patients with PTH 150-600 pg/mL / Total patients) × 100 | % | ≥60% | Monthly |
| **Phosphorus Control %** | (Sessions with P 3.5-5.5 mg/dL / Total sessions) × 100 | % | ≥75% | Monthly |
| **Calcium Control %** | (Sessions with Ca 8.4-10.2 mg/dL / Total sessions) × 100 | % | ≥75% | Monthly |

**Use Case:** Nephrologists and nurses manage comorbidities; critical for preventing complications.

---

## Operational Excellence KPIs

### 5. Utilization & Capacity

**Definition:** Optimal use of clinical resources.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Bed Utilization %** | (Total sessions scheduled / (Available beds × Operating hours)) × 100 | % | 85-95% | Daily |
| **Provider Utilization %** | (Sessions delivered / Scheduled sessions for provider) × 100 | % | 90%+ | Weekly |
| **Machine Availability %** | (Operating machines / Total licensed machines) × 100 | % | ≥95% | Daily |
| **Treatment Room Utilization %** | (Occupied treatment-hours / Available treatment-hours) × 100 | % | 80-90% | Weekly |

**Use Case:** Operations managers optimize scheduling and resource allocation.

---

### 6. Operational Efficiency

**Definition:** Cost-effective delivery of services.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Cost Per Session** | (Total facility costs) / (Number of sessions) | $/session | <$300 (varies by modality) | Monthly |
| **Supply Cost Per Session** | (Total supplies cost) / (Number of sessions) | $/session | <$150 | Monthly |
| **Labor Cost Per Session** | (Total labor cost) / (Number of sessions) | $/session | <$100 | Monthly |
| **Cost Per Patient Per Month** | (Total patient-related costs) / (Total patient-months) | $/patient-month | Target varies | Monthly |
| **Session Duration Variance** | |% of intended | ±10% | Weekly |

**Use Case:** Finance and operations track cost efficiency; identify cost reduction opportunities.

---

### 7. Schedule Adherence

**Definition:** Reliability of treatment scheduling.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **On-Time Arrival %** | (Sessions starting within 15 min of schedule / Total sessions) × 100 | % | ≥95% | Daily |
| **No-Show Rate** | (Patients not arriving / Scheduled sessions) × 100 | % | <2% | Weekly |
| **Cancellation Rate** | (Cancelled sessions / Scheduled sessions) × 100 | % | <1% | Weekly |
| **Schedule Cancellation Reason Distribution** | Breakdown by reason (medical, personal, facility) | % | Monitor all reasons | Weekly |
| **Session Rescheduling Success Rate** | (Successfully rescheduled / Total cancellations) × 100 | % | ≥95% | Weekly |

**Use Case:** Scheduling coordinators and managers optimize appointment adherence; minimize revenue loss.

---

### 8. Staff Productivity

**Definition:** Efficient use of clinical personnel.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Sessions Per FTE** | (Total sessions) / (Total FTE) | Sessions/FTE/year | 1200-1500 | Monthly |
| **Patient-to-Staff Ratio** | (Total patients) / (Total clinical staff FTE) | Patients per FTE | 8-10 | Monthly |
| **Overtime Hours % of Total** | (Overtime hours / Total hours worked) × 100 | % | <10% | Monthly |
| **Staff Utilization %** | (Productive hours / Total available hours) × 100 | % | ≥80% | Weekly |
| **Cross-Training %** | (Staff trained in multiple functions / Total staff) × 100 | % | ≥60% | Quarterly |

**Use Case:** Managers track labor productivity and plan staffing; HR monitors workforce efficiency.

---

## Financial KPIs

### 9. Revenue & Reimbursement

**Definition:** Revenue generation and collection.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Revenue Per Session** | (Total revenue) / (Number of sessions) | $/session | Target varies | Monthly |
| **Reimbursement Rate by Payer** | (Actual payment / Billed amount) × 100 | % | 75-90% | Monthly |
| **Denial Rate** | (Denied claims / Submitted claims) × 100 | % | <2% | Monthly |
| **Days Sales Outstanding (DSO)** | (Accounts receivable / Daily revenue) | Days | <35 | Monthly |
| **Net Collection Rate** | (Collected revenue / Net revenue) × 100 | % | >95% | Monthly |

**Use Case:** CFO, Finance leadership track revenue performance; identify collection issues.

---

### 10. Profitability

**Definition:** Financial margins and profitability.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Operating Margin** | (Operating revenue - Operating expenses) / Operating revenue | % | 5-15% | Monthly |
| **EBITDA Margin** | (EBITDA / Total revenue) | % | 15-20% | Monthly |
| **Margin by Modality** | Modality-specific margins | % | Monitor by modality | Monthly |
| **Margin by Facility** | Facility-specific margins | % | All facilities profitable | Monthly |
| **Cost of Service Ratio** | (Direct service costs / Revenue) | % | <70% | Monthly |

**Use Case:** Finance executives, board reporting, strategic planning.

---

## Quality & Compliance KPIs

### 11. Protocol Adherence

**Definition:** Compliance with clinical protocols.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Protocol Adherence %** | (Sessions following protocol / Total sessions) × 100 | % | ≥98% | Weekly |
| **Order Set Utilization %** | (Orders using protocol order set / Total orders) × 100 | % | ≥90% | Weekly |
| **Protocol Deviation Rate** | (Number of deviations / Total sessions) × 100 | % | <2% | Weekly |
| **Root Cause Analysis Completion %** | (Completed RCA / Quality events requiring RCA) × 100 | % | 100% | Weekly |

**Use Case:** Quality/Compliance tracks protocol adherence for regulatory compliance.

---

### 12. Regulatory Compliance

**Definition:** Meeting regulatory and accreditation requirements.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **CMS Compliance %** | (Compliant metrics / All required CMS metrics) × 100 | % | 100% | Continuously |
| **State License Compliance %** | (Compliant areas / All state-required areas) × 100 | % | 100% | Monthly |
| **Accreditation Status** | Accredited / Not accredited / Conditional | Status | Accredited | Continuously |
| **Audit Finding Rate** | (Audit findings / Total audits) | % | 0 | Per audit |
| **Corrective Action Closure %** | (Closed corrective actions / Total CAs) × 100 | % | 100% in target timeframe | Monthly |

**Use Case:** Compliance/Quality leadership maintains regulatory standing.

---

### 13. Data Quality

**Definition:** Completeness and accuracy of data.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Data Completeness %** | (Records with all required fields / Total records) × 100 | % | ≥99% | Daily |
| **Data Accuracy %** | (Validated records / Total records) × 100 | % | ≥99% | Daily |
| **Reconciliation Variance %** | (Variance from source / Total data) × 100 | % | <0.1% | Daily |
| **ETL Success Rate** | (Successful loads / Total load attempts) × 100 | % | 99.99% | Daily |
| **Data Freshness** | Hours since last refresh | Hours | <24 | Daily |

**Use Case:** Data engineers, analytics team maintain data quality.

---

## Patient Experience KPIs

### 14. Patient Satisfaction

**Definition:** Patient perception of care quality.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Patient Satisfaction Score** | Average of HCAHPS/NET satisfaction survey | Score (0-10) | ≥8 | Quarterly |
| **Likelihood to Recommend %** | (Would recommend / Total surveyed) × 100 | % | ≥90% | Quarterly |
| **Treatment Ease Score** | Perception of treatment ease | Score (0-10) | ≥7 | Quarterly |
| **Provider Communication Score** | Satisfaction with provider communication | Score (0-10) | ≥8 | Quarterly |

**Use Case:** Marketing, patient experience leadership; patient retention driver.

---

## Strategic Growth KPIs

### 15. Growth & Market Position

**Definition:** Expansion and competitive positioning.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Patient Census Growth %** | ((Current census - Prior year) / Prior year) × 100 | % | 5-10% annually | Monthly |
| **Market Share %** | (Organization patients / Total dialysis patients in region) × 100 | % | Monitor vs competitors | Quarterly |
| **New Facility Openings** | Number of new facilities opened | Count | 1-2 annually | Quarterly |
| **PD Penetration %** | (PD patients / Total dialysis patients) × 100 | % | 15-20% | Monthly |
| **Referral Growth %** | ((New referrals - Prior year) / Prior year) × 100 | % | 10-15% | Monthly |

**Use Case:** Executive leadership, business development, strategic planning.

---

## AI/ML & Innovation KPIs

### 16. Advanced Analytics Impact

**Definition:** Value created by AI/ML models and advanced analytics.

| KPI | Formula | Unit | Target | Frequency |
|-----|---------|------|--------|-----------|
| **Predictive Model Accuracy** | (Correct predictions / Total predictions) × 100 | % | ≥85% | Model evaluation |
| **Clinical Action Rate** | (Recommendations acted upon / Total recommendations) × 100 | % | ≥60% | Monthly |
| **Outcome Improvement from ML** | % improvement in target outcome (e.g., hospitalization reduction) | % | 10-20% | Quarterly |
| **Model Deployment Time** | Time from model training to production deployment | Weeks | <4 | Per model |
| **AI Model Performance Drift** | Performance degradation over time | % | Monitor <5% drift | Weekly |

**Use Case:** Chief Medical Officer, Data Science leadership, Innovation board.

---

## KPI Dashboard Hierarchy

```
EXECUTIVE DASHBOARD
├─ Strategic KPIs (15 metrics)
│  ├─ Revenue per session
│  ├─ Operating margin
│  ├─ Patient satisfaction
│  ├─ Survival rate (1-year)
│  ├─ Regulatory compliance status
│  └─ Patient census growth

CLINICAL DASHBOARD
├─ Quality KPIs (20+ metrics)
│  ├─ Treatment adequacy
│  ├─ Complication rates
│  ├─ Lab values control
│  ├─ Vital sign stability
│  └─ Patient outcomes

OPERATIONS DASHBOARD
├─ Efficiency KPIs (15 metrics)
│  ├─ Bed utilization
│  ├─ Cost per session
│  ├─ Schedule adherence
│  ├─ Session completion
│  └─ Staff productivity

COMPLIANCE DASHBOARD
├─ Governance KPIs (10 metrics)
│  ├─ Protocol adherence
│  ├─ Data quality
│  ├─ Audit findings
│  ├─ Corrective actions
│  └─ Regulatory status
```

---

## KPI Ownership & Escalation

| KPI Category | Owner | Escalation Path | Review Frequency |
|-------------|-------|-----------------|-----------------|
| Clinical Quality | CMO | CEO | Monthly |
| Operational | COO | CFO | Weekly |
| Financial | CFO | CEO | Weekly |
| Quality/Compliance | QA Director | CMO | Daily |
| Patient Experience | Patient Experience Lead | COO | Monthly |
| Strategic Growth | CEO | Board | Quarterly |

---

## Success Thresholds

KPIs use color coding to indicate performance:

- **Green (On Target):** KPI at or above target
- **Yellow (At Risk):** KPI 5-10% below target
- **Red (Off Target):** KPI >10% below target
- **Blue (Exceeding Expectations):** KPI >10% above target

Escalation triggers:
- Yellow status for 2 consecutive reporting periods → Manager review
- Red status → Immediate escalation and remediation plan required
- Trend analysis: 3-month negative trend triggers review even if currently green

---

*Last Updated: 2026-07-22*  
*Version: 1.0*
