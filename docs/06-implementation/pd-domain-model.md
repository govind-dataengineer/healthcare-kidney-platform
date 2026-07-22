# Peritoneal Dialysis (PD) Domain Model

## Overview

Peritoneal Dialysis is the first implemented therapy modality for the Kidney Care Analytics Platform. This document details the PD-specific extensions to the Common Data Model and Dimensional Model.

---

## PD-Specific Clinical Context

### PD Treatment Modality Types

**Continuous Ambulatory Peritoneal Dialysis (CAPD)**
- Patient performs manual exchanges 4-5 times daily
- Automated Machine (APD) is NOT used
- Nocturnal Intermittent Peritoneal Dialysis (NIPD) variant
- Day and night cycles

**Automated Peritoneal Dialysis (APD)**
- Cycler machine performs 3-6 cycles nightly
- Daytime dwell may occur
- Primarily overnight treatment

**Hybrid or Combination Regimens**
- Mix of manual and automated exchanges
- Often used for start of therapy or transition

---

## PD-Specific Business Entities

### 1. PD_PATIENT_PROFILE

Extended patient attributes specific to PD therapy.

| Attribute | Type | Description |
|-----------|------|-------------|
| patient_id | FK | Reference to patient |
| pd_start_date | DATE | When PD therapy initiated |
| pd_vintage_days | INTEGER | Days on PD therapy |
| current_pd_modality | ENUM | CAPD, APD, Hybrid |
| peritoneal_membrane_type | STRING | Native, Type I, Type II, Type III membrane classification |
| current_exchange_count_daily | INTEGER | Number of exchanges prescribed |
| dwell_volume_ml | INTEGER | Exchange volume in mL |
| solution_glucose_concentration | STRING | 1.5%, 2.5%, 4.25% |
| abdominal_exit_site_type | ENUM | Straight, Curled, Healed |
| exit_site_status | STRING | Healthy, Infection, Healing, History |
| tunnel_infection_history | BOOLEAN | History of tunnel infection |
| peritonitis_history_episodes | INTEGER | Number of prior peritonitis episodes |
| last_peritonitis_date | DATE | Date of most recent peritonitis |
| pd_adequacy_target_creatinine_clearance | DECIMAL | Target Ccr mL/min/1.73m2 |
| pd_adequacy_target_kt_v | DECIMAL | Target weekly Kt/V |
| catheter_placement_date | DATE | When catheter inserted |
| catheter_type | STRING | Tenckhoff, Swan Neck, Straight, Curled tip |
| last_exit_site_check_date | DATE | Most recent exit site assessment |
| effective_from_date | DATE | SCD effective date |
| effective_to_date | DATE | SCD end date |
| is_current | BOOLEAN | Current record indicator |

---

### 2. PD_EXCHANGE

A single peritoneal exchange event (the fundamental unit of PD therapy).

| Attribute | Type | Description |
|-----------|------|-------------|
| exchange_id | UUID | Unique identifier |
| session_id | FK | Parent treatment session |
| patient_id | FK | Patient performing exchange |
| exchange_date | DATE | Date of exchange |
| exchange_time | TIME | Time of exchange |
| exchange_sequence_number | INTEGER | Sequence within daily treatment (1st, 2nd, etc.) |
| exchange_type | ENUM | Manual, Cycler-Automated, Cycler-Daytime Dwell |
| prescribed_dwell_volume_ml | INTEGER | Prescribed fill volume |
| prescribed_dwell_duration_minutes | INTEGER | Prescribed dwell time |
| actual_dwell_volume_ml | INTEGER | Actual fill volume |
| actual_dwell_duration_minutes | INTEGER | Actual dwell time |
| solution_type | STRING | 1.5%, 2.5%, 4.25% glucose concentration |
| inflow_time_minutes | INTEGER | Time to complete inflow |
| outflow_time_minutes | INTEGER | Time to complete outflow |
| outflow_volume_ml | INTEGER | Actual dwell fluid drained |
| residual_volume_ml | INTEGER | Fluid remaining (outflow_volume vs. inflow_volume) |
| patient_performed_flag | BOOLEAN | Performed by patient or assistant |
| clinician_performed_flag | BOOLEAN | Performed by clinic staff |
| complications_during_exchange | ARRAY | [Leakage, Pain, Cloudiness, etc.] |
| clinical_notes | TEXT | Provider observations |

---

### 3. PD_PERITONITIS_EPISODE

Peritonitis is the most common and serious PD complication.

| Attribute | Type | Description |
|-----------|------|-------------|
| peritonitis_episode_id | UUID | Unique identifier |
| patient_id | FK | Affected patient |
| episode_start_date | DATE | When episode began |
| episode_start_time | TIME | Time episode detected |
| episode_end_date | DATE | When episode resolved |
| detection_method | ENUM | Cloudy effluent, WBC, Culture positive |
| presenting_symptoms | ARRAY | [Abdominal pain, Fever, Nausea, etc.] |
| initial_white_blood_cell_count | INTEGER | Initial WBC /mm3 |
| initial_polymorphonuclear_count | INTEGER | Initial PMN % |
| causative_organism | STRING | Bacterial culture result |
| organism_gram_status | ENUM | Positive, Negative |
| susceptibilities | ARRAY | Antibiotic susceptibilities |
| initial_antibiotic_therapy | ARRAY | Initial antibiotics prescribed |
| antibiotic_route | ARRAY | Intraperitoneal, IV, Oral routes |
| duration_antibiotic_therapy_days | INTEGER | Treatment duration |
| peritonitis_resolved_flag | BOOLEAN | Whether resolved |
| treatment_failure_flag | BOOLEAN | Whether required catheter removal |
| catheter_removal_required_flag | BOOLEAN | Whether temporary or permanent |
| hospital_admission_flag | BOOLEAN | Hospitalization required |
| clinical_outcome | ENUM | Resolved, Relapsed, Refractory, Catheter removal, Death |

---

### 4. PD_EXIT_SITE_ASSESSMENT

Regular exit site monitoring is critical for infection prevention.

| Attribute | Type | Description |
|-----------|------|-------------|
| exit_site_assessment_id | UUID | Unique identifier |
| patient_id | FK | Patient assessed |
| assessment_date | DATE | Date of assessment |
| assessment_by_provider_id | FK | Provider performing assessment |
| exit_site_appearance | ENUM | Clear, Edematous, Erythema, Purulent, Granulation |
| erythema_present_flag | BOOLEAN | Redness present |
| drainage_present_flag | BOOLEAN | Any drainage |
| drainage_type | ENUM | Clear, Serous, Purulent, Bloody |
| pain_present_flag | BOOLEAN | Patient-reported pain |
| culture_obtained_flag | BOOLEAN | Culture obtained |
| culture_result | STRING | Culture organism (if positive) |
| cellulitis_concern_flag | BOOLEAN | Concern for cellulitis |
| recommended_action | STRING | Observation, Antibiotics, Referral, Other |
| infection_prevention_teaching_provided_flag | BOOLEAN | Preventive education given |

---

### 5. PD_RESIDUAL_RENAL_FUNCTION (RRF)

Preservation of residual renal function is critical for PD patients.

| Attribute | Type | Description |
|-----------|------|-------------|
| rrf_assessment_id | UUID | Unique identifier |
| patient_id | FK | Patient assessed |
| assessment_date | DATE | Date of assessment |
| urine_collection_duration_hours | INTEGER | Collection period (typically 24h) |
| urine_volume_ml | INTEGER | Total urine volume collected |
| urine_creatinine_mg | INTEGER | Urine creatinine (24h) |
| urine_urea_nitrogen_g | DECIMAL | Urine urea nitrogen (24h) |
| serum_creatinine_mg_dl | DECIMAL | Serum creatinine at assessment |
| calculated_creatinine_clearance_ml_min | DECIMAL | Calculated Ccr |
| rrf_classification | ENUM | Excellent (>10), Good (5-10), Adequate (2-5), Minimal (<2) |
| urine_specific_gravity | DECIMAL | Urine SG |
| proteinuria_present_flag | BOOLEAN | Protein in urine |
| hematuria_present_flag | BOOLEAN | Blood in urine |
| infection_present_flag | BOOLEAN | Signs of UTI |
| treatment_recommendation | STRING | Continue current, Adjust regimen, etc. |

---

### 6. PD_ADEQUACY_ASSESSMENT

Regular adequacy assessments determine if PD is providing sufficient dialysis.

| Attribute | Type | Description |
|-----------|------|-------------|
| adequacy_assessment_id | UUID | Unique identifier |
| patient_id | FK | Patient assessed |
| assessment_date | DATE | Date of assessment |
| peritoneal_equilibration_test_date | DATE | Most recent PET date |
| transport_category | ENUM | High, High Average, Low Average, Low |
| transported_in_4h_creatinine_pct | DECIMAL | 4-hour creatinine % |
| dialysate_creatinine_plasma_ratio | DECIMAL | D/P creatinine ratio |
| glucose_absorption_pct | DECIMAL | % glucose absorbed in 4h |
| weekly_creatinine_clearance_ml_min | DECIMAL | Calculated Ccr |
| weekly_kt_v_peritoneal | DECIMAL | Peritoneal Kt/V contribution |
| weekly_kt_v_renal | DECIMAL | Renal Kt/V contribution |
| weekly_kt_v_total | DECIMAL | Total Kt/V |
| adequacy_target_met_flag | BOOLEAN | Kt/V target achieved |
| prescription_change_recommended_flag | BOOLEAN | Prescription adjustment needed |
| recommended_prescription_change | STRING | Increase exchanges, change solution strength, etc. |
| glucose_absorption_clinical_note | TEXT | Clinical assessment of absorption |

---

## PD-Specific Dimensions

### 1. dim_pd_solution

PD dialysate solutions with varying glucose concentrations.

| Column | Type | Description |
|--------|------|-------------|
| solution_sk | INT | Surrogate key |
| solution_code | VARCHAR(20) | Solution code |
| solution_name | VARCHAR(100) | Solution name |
| glucose_concentration_pct | DECIMAL(4,2) | 1.5%, 2.5%, 4.25%, etc. |
| glucose_concentration_mg_dl | INTEGER | mg/dL |
| dextrose_equivalency | DECIMAL(5,2) | Caloric equivalent |
| volume_options_ml | ARRAY | Available volumes (1500, 2000, 2500 mL, etc.) |
| manufacturer | VARCHAR(100) | Solution manufacturer |
| has_icodextrin | BOOLEAN | Contains icodextrin |
| has_amino_acids | BOOLEAN | Contains amino acids |
| osmolality_mosm_kg | DECIMAL(8,1) | Osmolality of solution |
| acidity_ph | DECIMAL(3,2) | Solution pH |
| electrolyte_composition | JSON | Na, K, Ca, Mg, Cl, HCO3 content |
| buffer_type | VARCHAR(20) | Lactate, Bicarbonate |

---

### 2. dim_pd_modality

PD-specific modalities.

| Column | Type | Description |
|--------|------|-------------|
| modality_sk | INT | Surrogate key |
| modality_code | VARCHAR(20) | CAPD, APD, NIPD, Hybrid |
| modality_name | VARCHAR(100) | Full modality name |
| exchanges_daily_typical_range | VARCHAR(20) | Typical range (e.g., "4-5" for CAPD) |
| automation_level | VARCHAR(50) | Manual, Fully Automated, Hybrid |
| typical_treatment_time_hours | INTEGER | Typical session duration |
| treatment_frequency_daily | ENUM | Multiple daily (CAPD), Once nightly (APD) |
| cycler_required_flag | BOOLEAN | Requires APD machine |
| typical_clinical_setting | VARCHAR(50) | Home, Clinic, Either |
| patient_training_complexity | VARCHAR(20) | Simple, Moderate, Complex |
| modality_description | VARCHAR(500) | Clinical description |

---

### 3. dim_pd_catheter_type

PD catheter specifications.

| Column | Type | Description |
|--------|------|-------------|
| catheter_type_sk | INT | Surrogate key |
| catheter_type_code | VARCHAR(20) | Tenckhoff, Swan Neck, Curled, Straight |
| catheter_name | VARCHAR(100) | Descriptive name |
| cuff_count | INT | Number of cuffs (0, 1, or 2) |
| positioning | VARCHAR(50) | Downward, Lateral, Curled |
| infection_risk | VARCHAR(20) | Low, Moderate, High (relative) |
| ease_of_insertion | VARCHAR(20) | Easy, Moderate, Difficult |
| common_complications | ARRAY | Known complications for type |
| typical_lifespan_months | INTEGER | Expected functional lifespan |
| exit_site_care_requirements | VARCHAR(200) | Specific care requirements |

---

### 4. dim_pd_peritoneal_membrane

Peritoneal membrane characteristics.

| Column | Type | Description |
|--------|------|-------------|
| membrane_sk | INT | Surrogate key |
| membrane_type_code | VARCHAR(20) | Native, Type I, Type II, Type III |
| membrane_description | VARCHAR(200) | Clinical description |
| transport_category_typical | ENUM | High, High Average, Low Average, Low |
| creatinine_transport_rate | DECIMAL(4,2) | Typical D/P creatinine ratio |
| glucose_absorption_rate | VARCHAR(20) | Typical % in 4h |
| glucose_peritonitis_risk | VARCHAR(50) | High, Moderate, Low |
| ultrafiltration_capacity | VARCHAR(50) | Good, Moderate, Poor |
| longevity_years | INTEGER | Typical membrane longevity on PD |
| comorbidity_implications | VARCHAR(500) | Special considerations |

---

## PD-Specific Fact Tables

### 1. fct_pd_exchange

**Grain:** One row per exchange event.

| Column | Type | Description |
|--------|------|-------------|
| exchange_id (PK) | UUID | Surrogate key |
| session_sk | INT | FK to fct_treatment_session |
| patient_sk | INT | FK to dim_patient |
| exchange_date_sk | INT | FK to dim_date |
| exchange_time_sk | INT | FK to dim_time |
| modality_sk | INT | FK to dim_pd_modality |
| solution_sk | INT | FK to dim_pd_solution |
| inflow_volume | INT | Actual fill volume (mL) |
| outflow_volume | INT | Actual drainage volume (mL) |
| dwell_duration_minutes | INT | Actual dwell time |
| net_ultrafiltration_ml | INT | (Outflow - Inflow) volume |
| complications_present_flag | BOOLEAN | Any complications noted |
| exchange_quality_rating | INT | 1-5 quality rating |
| patient_performed_flag | BOOLEAN | Patient vs. clinician performed |

**Measures:**
- Exchange count (daily, weekly, monthly totals)
- Average ultrafiltration
- Complication rates
- Patient-performed exchange %

---

### 2. fct_pd_peritonitis_episode

**Grain:** One row per peritonitis episode.

| Column | Type | Description |
|--------|------|-------------|
| peritonitis_episode_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| episode_start_date_sk | INT | FK to dim_date (episode start) |
| episode_end_date_sk | INT | FK to dim_date (episode end) |
| episode_duration_days | INT | Days from start to resolution |
| causative_organism_sk | INT | FK to dim_organism (if applicable) |
| severity_sk | INT | FK to dim_severity |
| hospitalization_flag | BOOLEAN | Hospitalization required |
| catheter_removal_flag | BOOLEAN | Catheter removed |
| mortality_flag | BOOLEAN | Peritonitis-related death |
| treatment_success_flag | BOOLEAN | Successfully treated |

**Measures:**
- Peritonitis rates (per patient-months)
- Episode duration average
- Treatment success rate
- Hospitalization rate from peritonitis
- Organism distribution

---

### 3. fct_pd_adequacy_assessment

**Grain:** One row per adequacy assessment.

| Column | Type | Description |
|--------|------|-------------|
| adequacy_assessment_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| assessment_date_sk | INT | FK to dim_date |
| episode_sk | INT | FK to dim_episode_of_care |
| weekly_kt_v_peritoneal | DECIMAL(5,2) | Peritoneal Kt/V contribution |
| weekly_kt_v_renal | DECIMAL(5,2) | Renal Kt/V contribution |
| weekly_kt_v_total | DECIMAL(5,2) | Total weekly Kt/V |
| kt_v_target_met_flag | BOOLEAN | Adequacy target achieved |
| creatinine_clearance_ml_min | DECIMAL(8,2) | Ccr value |
| membrane_type_sk | INT | FK to dim_pd_peritoneal_membrane |
| transport_category_sk | INT | FK to transport category dimension |
| rrf_status_sk | INT | FK to residual renal function status |
| prescription_change_required_flag | BOOLEAN | Protocol modification needed |

**Measures:**
- Adequacy achievement rate
- Average Kt/V values
- Trend in adequacy over time
- Prescription change frequency

---

## PD-Specific KPIs

| KPI | Formula | Target | Frequency |
|-----|---------|--------|-----------|
| **Peritonitis Rate** | (Episodes / Patient-months) × 1000 | <0.5 per 1000 pt-mo | Monthly |
| **Exit Site Infection Rate** | (ESI episodes / Patient-months) × 1000 | <0.5 per 1000 pt-mo | Monthly |
| **Technique Survival (1-yr)** | (Patients on PD at 1 year / Cohort start) | >80% | Annually |
| **Patient Survival (1-yr)** | (Living patients at 1 year / Cohort start) | >95% | Annually |
| **Average Weekly Kt/V** | Mean Kt/V across cohort | ≥1.7 | Monthly |
| **Adequacy Achievement %** | (Patients with Kt/V ≥1.7 / Total) × 100 | ≥85% | Monthly |
| **Net Ultrafiltration (avg)** | Mean daily ultrafiltration | Varies by membrane | Monthly |
| **RRF Preservation Rate** | (Patients with RRF maintained / Cohort) | >60% at 2 years | Quarterly |
| **Modality Transition Rate** | (Transitions to HD / Total PD patients) | <10% annually | Annually |
| **Home Training Success %** | (Successful home training / Total trained) | >95% | Quarterly |

---

## PD Clinical Workflows

### Daily Exchange Documentation
```
Exchange Event
  ├─ Date & Time
  ├─ Exchange sequence
  ├─ Solution type & volume
  ├─ Dwell duration
  ├─ Inflow/outflow volumes
  ├─ Net ultrafiltration
  ├─ Complications
  ├─ Quality assessment
  └─ Provider notes
```

### Monthly Monitoring Protocol
```
Patient Assessment
  ├─ Exit site assessment
  ├─ Vital signs
  ├─ Weight trending
  ├─ Lab results (creatinine, BUN, electrolytes)
  ├─ Adequacy review
  ├─ RRF assessment
  ├─ Comorbidity review
  └─ Prescription adjustment if needed
```

### Peritonitis Management Workflow
```
Peritonitis Episode
  ├─ Detection (cloudy effluent)
  ├─ Initial assessment (WBC, culture)
  ├─ Antibiotic initiation (IP/IV)
  ├─ Culture monitoring
  ├─ Response assessment (48-72h)
  ├─ Continuation or modification
  ├─ Resolution (72h+ WBC <100, <50% PMN)
  └─ Outcome documentation
```

---

## Data Integration Points

### Source Systems
- **EHR:** Patient demographics, provider orders, clinical notes, vital signs
- **Lab System:** Lab results, cultures, adequacy parameters
- **PD Cycler Machines:** Automated exchange parameters (if machine-connected)
- **Clinic Documentation:** Assessments, interventions, teaching records

---

*Last Updated: 2026-07-22*  
*Version: 1.0*
