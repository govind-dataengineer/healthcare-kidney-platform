# Enterprise Bus Matrix

## Overview

The Enterprise Bus Matrix is a cross-functional data requirements matrix that identifies which business processes need which dimensions. It ensures alignment between data architecture and business needs, and helps prioritize analytics development.

The matrix answers: "What data do different departments need to make decisions?"

---

## Business Processes vs. Dimensions

|  | Patient | Facility | Provider | Treatment Modality | Episode of Care | Date/Time |
|---|---|---|---|---|---|---|
| **Treatment Delivery** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Lab Testing** | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| **Vital Sign Monitoring** | ✓ | ✓ |  |  | ✓ | ✓ |
| **Medication Management** | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| **Clinical Events** | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| **Quality Assurance** | ✓ | ✓ | ✓ | ✓ |  | ✓ |
| **Scheduling** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Staff Productivity** |  | ✓ | ✓ |  |  | ✓ |
| **Financial/Billing** | ✓ | ✓ |  | ✓ | ✓ | ✓ |
| **Patient Outcomes** | ✓ |  | ✓ | ✓ | ✓ | ✓ |

---

## Detailed Business Process Requirements

### 1. Treatment Delivery

**Stakeholders:** Clinic Managers, Nephrologists, Nurses, Technicians

**Key Metrics:**
- Sessions scheduled vs. completed
- Treatment adherence (intended vs. actual time)
- Session utilization by facility/provider
- Cancellation rates and reasons
- On-time arrival rates

**Required Dimensions:**
- Patient (identify who received treatment)
- Facility (where treatment occurred)
- Provider (who delivered treatment)
- Treatment Modality (therapy type)
- Episode of Care (continuity of care)
- Date/Time (trend analysis)

**Data Needs:**
- Treatment session facts (central fact table)
- Historical treatment patterns
- Treatment protocol adherence
- Quality flags associated with sessions

---

### 2. Lab Testing

**Stakeholders:** Nephrologists, Lab Directors, Clinical Scientists

**Key Metrics:**
- Test volumes by type and modality
- Abnormal result rates
- Result turnaround time
- Lab utilization
- Trending of key markers (Creatinine, KT/V, URR, etc.)

**Required Dimensions:**
- Patient (who was tested)
- Facility (where test performed)
- Provider (who ordered test)
- Date/Time (trend analysis)
- Episode of Care (disease progression)

**Data Needs:**
- Lab result facts with historic values
- Test reference ranges
- Abnormal flag indicators
- Specimen collection vs. result reporting times

---

### 3. Vital Sign Monitoring

**Stakeholders:** Nurses, Nephrologists, Quality Directors

**Key Metrics:**
- Pre/post session vital sign changes
- Hemodynamic stability
- Blood pressure control rates
- Weight trending (interdialytic weight gain)
- Hypotensive episode rates

**Required Dimensions:**
- Patient (whose vitals)
- Facility (measurement location)
- Date/Time (high-frequency measurements)
- Episode of Care (clinical context)

**Data Needs:**
- Vital sign facts with frequent measurements
- Session-linked pre/post vital signs
- Historical trending data
- Normal range definitions

---

### 4. Medication Management

**Stakeholders:** Nephrologists, Pharmacists, Nurses, Compliance Officers

**Key Metrics:**
- Medication administration rates vs. prescription
- Drug adherence by class
- Nephrology-specific medication utilization
- Drug-related adverse events
- Cost per medication class

**Required Dimensions:**
- Patient (who received medication)
- Facility (where administered)
- Provider (who prescribed)
- Episode of Care (clinical context)
- Date/Time (administration patterns)

**Data Needs:**
- Medication administration facts
- Prescribed vs. administered reconciliation
- Drug-disease interaction flags
- Route and dosing information

---

### 5. Clinical Events

**Stakeholders:** Nephrologists, Infection Prevention, Risk Management, QA

**Key Metrics:**
- Complication rates
- Infection rates and types
- Hospitalization rates and duration
- Preventable adverse events
- Readmission rates

**Required Dimensions:**
- Patient (who experienced event)
- Facility (where event occurred)
- Provider (who documented)
- Treatment Modality (event modality-specific?)
- Date/Time (trend analysis)

**Data Needs:**
- Clinical event facts
- ICD-10 coding
- Severity ratings
- Episode linkage
- Outcome tracking

---

### 6. Quality Assurance

**Stakeholders:** Quality Directors, Compliance Officers, Nephrologists

**Key Metrics:**
- Protocol adherence rates
- Quality event rates
- Root cause distribution
- Corrective action effectiveness
- Trend analysis of quality issues

**Required Dimensions:**
- Facility (where issue occurred)
- Provider (who reported)
- Treatment Modality (modality of session)
- Date/Time (incident timing)

**Data Needs:**
- Quality event facts
- Protocol definitions
- Root cause classifications
- Corrective action tracking
- Resolution timing

---

### 7. Scheduling

**Stakeholders:** Clinic Managers, Schedulers, Nurses

**Key Metrics:**
- Schedule utilization rates
- Cancellation rates by reason
- Provider scheduling efficiency
- Patient appointment adherence
- Room/machine utilization

**Required Dimensions:**
- Patient (who is scheduled)
- Facility (where scheduled)
- Provider (who is assigned)
- Treatment Modality (type of treatment)
- Episode of Care (treatment context)
- Date/Time (detailed time slots)

**Data Needs:**
- Scheduled vs. actual treatment sessions
- No-show tracking
- Cancellation reasons
- Provider availability
- Resource constraints

---

### 8. Staff Productivity

**Stakeholders:** Clinic Managers, HR, Finance

**Key Metrics:**
- Sessions per FTE
- Productivity trends over time
- Staff utilization rates
- Overtime patterns
- Cost per session per provider

**Required Dimensions:**
- Facility (where worked)
- Provider (productivity metric)
- Date/Time (shift patterns, monthly trends)

**Data Needs:**
- Treatment sessions assigned per provider
- Staffing levels and shifts
- Hours worked tracking
- Productive vs. non-productive time

---

### 9. Financial/Billing

**Stakeholders:** Finance, Billing, Operations Leadership

**Key Metrics:**
- Revenue per session
- Cost per session
- Reimbursement rates by payer
- Cost center profitability
- Treatment modality margins

**Required Dimensions:**
- Patient (insurance information)
- Facility (cost center)
- Treatment Modality (revenue drivers)
- Date/Time (monthly/quarterly reporting)

**Data Needs:**
- Treatment session facts with treatment time delivered
- Provider costs
- Supply costs
- Reimbursement rates by payer/procedure code

---

### 10. Patient Outcomes

**Stakeholders:** Chief Medical Officer, Nephrologists, Executives

**Key Metrics:**
- Survival rates by modality
- Mortality trends
- Morbidity rates (hospitalizations, infections)
- Quality of life metrics
- Patient satisfaction scores
- Modality comparison outcomes

**Required Dimensions:**
- Patient (demographic/comorbidity context)
- Provider (nephrologist effect)
- Treatment Modality (modality comparison)
- Date/Time (long-term trending)

**Data Needs:**
- Clinical event facts (mortality, morbidity)
- Lab result trending
- Vital sign stability
- Patient-reported outcomes
- Longitudinal patient cohorts

---

## Implementation Priority

### Phase 1 (Q3 2026) - PD Foundation
- ✓ Treatment Delivery
- ✓ Lab Testing
- ✓ Vital Sign Monitoring
- ✓ Quality Assurance
- ✓ Patient Outcomes (basic)

### Phase 1+ (Q4 2026) - PD Optimization
- ✓ Medication Management
- ✓ Clinical Events
- ✓ Scheduling
- ✓ Staff Productivity
- ✓ Patient Outcomes (advanced)

### Phase 2 (Q1-Q2 2027) - HD Integration
- ✓ All Phase 1 for HD
- ✓ Cross-modality comparisons
- ✓ Financial/Billing

### Phase 3 (Q3+ 2027) - Enterprise Analytics
- ✓ All processes across all modalities
- ✓ Enterprise financial analytics
- ✓ Advanced AI/ML outcomes modeling

---

## Data Flow by Process

```
Treatment Delivery
└─ Treatment Session → Quality Events
                    → Lab Results
                    → Vital Signs
                    → Medication Administration
                    → Clinical Events

Patient Outcomes
└─ Episode of Care → Clinical Events (complications, infections)
               → Lab Results (trending)
               → Vital Signs (stability)
               → Treatment Sessions (adherence impact)
```

---

## Stakeholder Engagement

Each business process requires engagement with specific stakeholders for requirements definition:

| Process | Primary Stakeholder | Secondary Stakeholders |
|---------|-------------------|----------------------|
| Treatment Delivery | Clinic Manager | Nephrologist, Nurse, Tech |
| Lab Testing | Lab Director | Nephrologist, Clinical Scientist |
| Vital Sign Monitoring | Nurse Manager | Nephrologist, QA Director |
| Medication Management | Chief Pharmacist | Nephrologist, Nurse, Compliance |
| Clinical Events | Chief Medical Officer | Nephrologist, Risk Manager |
| Quality Assurance | Quality Director | Compliance, Nephrologist |
| Scheduling | Clinic Coordinator | Manager, Provider |
| Staff Productivity | Operations Manager | Finance, HR |
| Financial/Billing | CFO | Finance Manager, Operations |
| Patient Outcomes | CMO | Nephrologist, Researcher |

---

## Success Metrics

The Enterprise Bus Matrix is successful when:

1. **Coverage** - All 10 business processes supported with required dimensions
2. **Adoption** - 80%+ of stakeholders actively using process-specific analytics
3. **Quality** - Data quality scores >95% for all covered processes
4. **Performance** - Query performance <100ms for 95th percentile
5. **Extensibility** - New processes can be added without data model redesign
6. **Governance** - Clear ownership of each dimension and process
7. **Alignment** - Analytics align with stated business objectives

---

*Last Updated: 2026-07-22*  
*Version: 1.0*
