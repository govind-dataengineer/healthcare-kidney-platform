# Dimensional Model (Kimball)

## Overview

This document details the Kimball dimensional model that implements the Common Data Model. The model organizes data into fact tables (business events) and dimension tables (reusable entities) to support analytics, machine learning, and semantic layer queries.

---

## Fact Tables

### 1. fct_treatment_session (Central Fact Table)

**Business Event:** A single treatment session delivered to a patient.

**Grain:** One row per treatment session.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| session_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| episode_sk | INT | FK to dim_episode_of_care |
| facility_sk | INT | FK to dim_facility |
| provider_sk | INT | FK to dim_provider |
| protocol_sk | INT | FK to dim_treatment_protocol |
| date_sk | INT | FK to dim_date (session date) |
| time_sk | INT | FK to dim_time (session start time) |
| modality_sk | INT | FK to dim_treatment_modality |
| session_status_sk | INT | FK to dim_session_status |
| scheduled_start_time | TIMESTAMP | Planned start time |
| actual_start_time | TIMESTAMP | Actual start time |
| scheduled_end_time | TIMESTAMP | Planned end time |
| actual_end_time | TIMESTAMP | Actual end time |
| scheduled_duration_minutes | INT | Planned duration |
| actual_duration_minutes | INT | Actual duration |
| intended_treatment_time_minutes | INT | Clinical target |
| actual_treatment_time_minutes | INT | Actual delivery |
| treatment_delivered_pct | DECIMAL(5,2) | Quality metric |
| arrived_on_time_flag | BOOLEAN | Started within 15 min of schedule |
| session_completed_flag | BOOLEAN | Session completed vs. abandoned |
| cancellation_reason | STRING | Reason if cancelled |
| quality_flag | STRING | Quality issues detected |
| session_load_ts | TIMESTAMP | ETL load timestamp |
| session_update_ts | TIMESTAMP | Last update timestamp |

**Measures:**
- Counts: session count, completed session count
- Rates: adherence rate, completion rate
- Averages: average duration, average treatment delivered %

**Late-Arriving Facts:** None (sessions finalized within 24 hours)

---

### 2. fct_lab_result

**Business Event:** A clinical laboratory test result.

**Grain:** One row per lab test per patient per specimen collection.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| lab_result_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| session_sk | INT | FK to fct_treatment_session (NULL if not session-specific) |
| episode_sk | INT | FK to dim_episode_of_care |
| facility_sk | INT | FK to dim_facility |
| provider_sk | INT | FK to dim_provider |
| test_sk | INT | FK to dim_lab_test |
| collection_date_sk | INT | FK to dim_date (specimen collection) |
| collection_time_sk | INT | FK to dim_time |
| report_date_sk | INT | FK to dim_date (result report) |
| numeric_value | DECIMAL(18,6) | Test result |
| numeric_unit_sk | INT | FK to dim_unit (unit of measurement) |
| reference_range_low | DECIMAL(18,6) | Normal range low |
| reference_range_high | DECIMAL(18,6) | Normal range high |
| abnormal_flag_sk | INT | FK to dim_abnormal_flag (Normal, High, Low, Critical) |
| test_method | STRING | Testing methodology |
| lab_notes | STRING | Lab notes |
| source_system | STRING | EHR system name |
| external_id | STRING | Source system ID |
| result_load_ts | TIMESTAMP | ETL load timestamp |

**Measures:**
- Test counts (per patient, per facility, per period)
- Abnormal test rates
- Average values (with handling of unit conversion)

---

### 3. fct_vital_sign

**Business Event:** A vital sign measurement.

**Grain:** One row per vital sign measurement per patient per time.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| vital_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| session_sk | INT | FK to fct_treatment_session |
| facility_sk | INT | FK to dim_facility |
| vital_type_sk | INT | FK to dim_vital_type (BP, HR, Temp, etc.) |
| measurement_date_sk | INT | FK to dim_date |
| measurement_time_sk | INT | FK to dim_time |
| numeric_value | DECIMAL(8,2) | Measurement value |
| numeric_unit_sk | INT | FK to dim_unit |
| body_site | STRING | Where measured (L arm, R arm, etc.) |
| measurement_device | STRING | Device used |
| measurement_method | STRING | Method (manual, automated, etc.) |
| measurement_notes | STRING | Clinical notes |
| vital_load_ts | TIMESTAMP | ETL load timestamp |

**Measures:**
- Vital sign counts
- Average values per patient, per modality
- Trend analysis (vitals over time)

---

### 4. fct_medication_administration

**Business Event:** Administration of medication to a patient.

**Grain:** One row per medication administration event.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| med_admin_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| session_sk | INT | FK to fct_treatment_session |
| episode_sk | INT | FK to dim_episode_of_care |
| facility_sk | INT | FK to dim_facility |
| provider_sk | INT | FK to dim_provider |
| medication_sk | INT | FK to dim_medication |
| route_sk | INT | FK to dim_medication_route |
| admin_date_sk | INT | FK to dim_date |
| admin_time_sk | INT | FK to dim_time |
| dose_quantity | DECIMAL(18,6) | Dose administered |
| dose_unit_sk | INT | FK to dim_unit |
| indication | STRING | Clinical indication |
| provider_notes | STRING | Provider documentation |
| admin_load_ts | TIMESTAMP | ETL load timestamp |

**Measures:**
- Medication administration counts
- Adherence metrics (% of prescribed medications given)
- Drug utilization (frequency per patient)

---

### 5. fct_clinical_event

**Business Event:** A significant clinical occurrence.

**Grain:** One row per clinical event.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| event_id (PK) | UUID | Surrogate key |
| patient_sk | INT | FK to dim_patient |
| session_sk | INT | FK to fct_treatment_session (NULL if not session-specific) |
| episode_sk | INT | FK to dim_episode_of_care |
| facility_sk | INT | FK to dim_facility |
| provider_sk | INT | FK to dim_provider |
| event_type_sk | INT | FK to dim_clinical_event_type |
| event_code_sk | INT | FK to dim_icd_code |
| start_date_sk | INT | FK to dim_date |
| start_time_sk | INT | FK to dim_time |
| end_date_sk | INT | FK to dim_date (NULL if ongoing) |
| severity_sk | INT | FK to dim_severity |
| action_taken | STRING | Intervention taken |
| outcome_sk | INT | FK to dim_event_outcome |
| event_load_ts | TIMESTAMP | ETL load timestamp |

**Measures:**
- Event occurrence counts
- Complication rates
- Hospitalization counts and duration
- Severity distribution

---

### 6. fct_quality_event

**Business Event:** A quality or compliance issue.

**Grain:** One row per quality event.

**Key Columns:**

| Column | Type | Description |
|--------|------|-------------|
| quality_event_id (PK) | UUID | Surrogate key |
| session_sk | INT | FK to fct_treatment_session |
| facility_sk | INT | FK to dim_facility |
| protocol_sk | INT | FK to dim_treatment_protocol |
| quality_event_type_sk | INT | FK to dim_quality_event_type |
| severity_sk | INT | FK to dim_severity |
| detected_date_sk | INT | FK to dim_date |
| reported_by_provider_sk | INT | FK to dim_provider |
| root_cause | STRING | Root cause analysis |
| corrective_action | STRING | Corrective action taken |
| resolution_date_sk | INT | FK to dim_date |
| quality_event_status_sk | INT | FK to dim_quality_event_status |
| event_load_ts | TIMESTAMP | ETL load timestamp |

**Measures:**
- Quality event counts
- Event rates (events per 100 sessions)
- Resolution time averages
- Severity distribution

---

## Dimension Tables

### Conformed Dimensions (Used by Multiple Facts)

#### dim_patient

**Slowly Changing Dimension:** Type 2 (track history)

| Column | Type | Description |
|--------|------|-------------|
| patient_sk (PK) | INT | Surrogate key |
| patient_id | UUID | Natural key (de-identified) |
| mrn | STRING | Medical record number (encrypted, NOT in analytics layer for non-clinical users) |
| age_years | INT | Age in years (updated annually) |
| gender_code | CHAR(1) | M/F/O/U |
| race_code | VARCHAR(2) | OMB race code |
| ethnicity_code | VARCHAR(2) | Hispanic/Non-Hispanic |
| dialysis_vintage_years | DECIMAL(5,2) | Years on renal replacement therapy |
| ckd_stage | INT | CKD stage (1-5) |
| effective_from_date | DATE | SCD Type 2 effective date |
| effective_to_date | DATE | SCD Type 2 end date |
| is_current | BOOLEAN | Current record indicator |

**Conformed By:** fct_treatment_session, fct_lab_result, fct_vital_sign, fct_medication_administration, fct_clinical_event

---

#### dim_facility

**Slowly Changing Dimension:** Type 1 (overwrite)

| Column | Type | Description |
|--------|------|-------------|
| facility_sk (PK) | INT | Surrogate key |
| facility_id | UUID | Natural key |
| facility_name | VARCHAR(255) | Facility name |
| facility_type_code | VARCHAR(20) | Clinic, Hospital, Satellite, etc. |
| state_code | CHAR(2) | State |
| region_code | VARCHAR(20) | Geographic region |
| npi | VARCHAR(10) | NPI identifier |
| cms_certification | VARCHAR(20) | CMS cert number |
| capacity_beds | INT | Licensed capacity |
| supported_modalities | VARCHAR(50) | Modalities supported |
| facility_status | VARCHAR(20) | Active/Inactive |

**Conformed By:** fct_treatment_session, fct_lab_result, fct_vital_sign, fct_medication_administration, fct_clinical_event, fct_quality_event

---

#### dim_provider

**Slowly Changing Dimension:** Type 2 (track history)

| Column | Type | Description |
|--------|------|-------------|
| provider_sk (PK) | INT | Surrogate key |
| provider_id | UUID | Natural key |
| provider_name | VARCHAR(255) | Provider name |
| provider_type_code | VARCHAR(20) | MD, DO, RN, LPN, CCHT, etc. |
| specialty_code | VARCHAR(50) | Nephrology, Internal Medicine, etc. |
| npi | VARCHAR(10) | National Provider Identifier |
| credentials | VARCHAR(255) | Board certifications |
| facility_id | UUID | Primary facility |
| employment_status | VARCHAR(20) | Active, Inactive, Leave, etc. |
| effective_from_date | DATE | SCD Type 2 effective date |
| effective_to_date | DATE | SCD Type 2 end date |
| is_current | BOOLEAN | Current record indicator |

**Conformed By:** fct_treatment_session, fct_medication_administration, fct_clinical_event, fct_quality_event

---

#### dim_date

**Static Dimension:** No SCD required

| Column | Type | Description |
|--------|------|-------------|
| date_sk (PK) | INT | Surrogate key (YYYYMMDD format) |
| calendar_date | DATE | Full date |
| calendar_year | INT | Year |
| calendar_quarter | INT | Quarter (1-4) |
| calendar_month | INT | Month (1-12) |
| calendar_week | INT | Week of year (1-53) |
| calendar_day_of_month | INT | Day of month (1-31) |
| calendar_day_of_week | INT | Day of week (1=Sunday, 7=Saturday) |
| is_weekday | BOOLEAN | Weekday flag |
| is_holiday_us | BOOLEAN | US holiday flag |
| fiscal_year | INT | Fiscal year |
| fiscal_quarter | INT | Fiscal quarter |
| fiscal_month | INT | Fiscal month |

**Conformed By:** All fact tables

---

#### dim_time

**Static Dimension:** No SCD required

| Column | Type | Description |
|--------|------|-------------|
| time_sk (PK) | INT | Surrogate key (HHMISS format) |
| time_of_day | TIME | Time as HH:MM:SS |
| hour_of_day | INT | Hour (0-23) |
| minute_of_hour | INT | Minute (0-59) |
| second_of_minute | INT | Second (0-59) |
| hour_of_business_day | INT | Hours from 6am (0-18) |
| shift_code | VARCHAR(20) | Night, Early, Day, Late |
| is_business_hours | BOOLEAN | 6am-6pm flag |

**Conformed By:** fct_treatment_session, fct_lab_result, fct_vital_sign, fct_medication_administration, fct_clinical_event

---

#### dim_episode_of_care

**Slowly Changing Dimension:** Type 1 (closed episodes) / Type 2 (active episodes)

| Column | Type | Description |
|--------|------|-------------|
| episode_sk (PK) | INT | Surrogate key |
| episode_id | UUID | Natural key |
| patient_sk | INT | FK to dim_patient |
| episode_type_code | VARCHAR(20) | Initial, Active, Transition, EOL |
| primary_modality_code | VARCHAR(20) | PD, HD, Acute, Conservative |
| start_date | DATE | Episode start |
| end_date | DATE | Episode end (NULL if active) |
| end_reason_code | VARCHAR(50) | Transplant, Transfer, Death, etc. |
| nephrology_provider_sk | INT | FK to dim_provider |
| facility_sk | INT | FK to dim_facility |
| ckd_stage | INT | CKD stage at episode start |
| dialysis_vintage_days | INT | Days on dialysis at start |
| episode_status_code | VARCHAR(20) | Active, Closed, Archived |

**Conformed By:** fct_treatment_session, fct_lab_result, fct_medication_administration, fct_clinical_event

---

### Dimension Tables (Specialized)

#### dim_treatment_modality

| Column | Type | Description |
|--------|------|-------------|
| modality_sk (PK) | INT | Surrogate key |
| modality_code | VARCHAR(20) | PD, HD, Acute, Conservative, Transplant, etc. |
| modality_name | VARCHAR(100) | Full name |
| modality_category | VARCHAR(50) | RRT, Non-RRT, etc. |
| is_active_treatment | BOOLEAN | Flag for active treatment modalities |

**Used By:** fct_treatment_session

---

#### dim_treatment_protocol

| Column | Type | Description |
|--------|------|-------------|
| protocol_sk (PK) | INT | Surrogate key |
| protocol_id | UUID | Natural key |
| protocol_name | VARCHAR(255) | Protocol name |
| protocol_type_code | VARCHAR(20) | PD, HD, Acute, etc. |
| description | VARCHAR(1000) | Clinical description |
| version | VARCHAR(20) | Version number |
| effective_from_date | DATE | Version effective date |
| effective_to_date | DATE | Version end date |
| approver_provider_sk | INT | FK to dim_provider |
| protocol_status_code | VARCHAR(20) | Draft, Active, Superseded, Retired |

**Used By:** fct_treatment_session, fct_quality_event

---

#### dim_lab_test

| Column | Type | Description |
|--------|------|-------------|
| test_sk (PK) | INT | Surrogate key |
| test_code | VARCHAR(50) | LOINC or internal code |
| test_name | VARCHAR(255) | Test name |
| test_category_code | VARCHAR(50) | Chemistry, Hematology, Immunology, Microbiology |
| normal_range_low | DECIMAL(18,6) | Default normal range low |
| normal_range_high | DECIMAL(18,6) | Default normal range high |
| normal_unit | VARCHAR(50) | Standard unit |
| test_method | VARCHAR(100) | Standard method |

**Used By:** fct_lab_result

---

#### dim_vital_type

| Column | Type | Description |
|--------|------|-------------|
| vital_type_sk (PK) | INT | Surrogate key |
| vital_code | VARCHAR(50) | Vital code |
| vital_name | VARCHAR(100) | Vital name (Systolic BP, Heart Rate, etc.) |
| vital_category | VARCHAR(50) | Cardiovascular, Respiratory, Temperature, Weight |
| measurement_unit | VARCHAR(50) | Unit of measurement |
| normal_range_low | DECIMAL(8,2) | Expected normal low |
| normal_range_high | DECIMAL(8,2) | Expected normal high |

**Used By:** fct_vital_sign

---

#### dim_medication

| Column | Type | Description |
|--------|------|-------------|
| medication_sk (PK) | INT | Surrogate key |
| medication_code | VARCHAR(50) | NDC or internal code |
| medication_name | VARCHAR(255) | Medication name |
| medication_class | VARCHAR(100) | Drug class |
| route_codes | VARCHAR(200) | Applicable routes (IV, PO, IM, etc.) |
| active_ingredient | VARCHAR(255) | Active ingredient(s) |
| strength | VARCHAR(100) | Standard strength |
| is_nephrology_specific | BOOLEAN | Nephrology-specific drug flag |

**Used By:** fct_medication_administration

---

#### dim_medication_route

| Column | Type | Description |
|--------|------|-------------|
| route_sk (PK) | INT | Surrogate key |
| route_code | VARCHAR(20) | IV, PO, IM, SC, Intraperitoneal, etc. |
| route_name | VARCHAR(100) | Route description |

**Used By:** fct_medication_administration

---

#### dim_unit

| Column | Type | Description |
|--------|------|-------------|
| unit_sk (PK) | INT | Surrogate key |
| unit_code | VARCHAR(20) | UCUM code |
| unit_name | VARCHAR(50) | Unit name |
| unit_system | VARCHAR(20) | Metric, Imperial, etc. |

**Used By:** fct_lab_result, fct_vital_sign, fct_medication_administration

---

#### dim_abnormal_flag

| Column | Type | Description |
|--------|------|-------------|
| abnormal_flag_sk (PK) | INT | Surrogate key |
| flag_code | CHAR(1) | N, H, L, C (Normal, High, Low, Critical) |
| flag_name | VARCHAR(20) | Normal, High, Low, Critical |

**Used By:** fct_lab_result

---

#### dim_severity

| Column | Type | Description |
|--------|------|-------------|
| severity_sk (PK) | INT | Surrogate key |
| severity_code | VARCHAR(20) | Minor, Moderate, Severe, Critical |
| severity_level | INT | Numeric level (1-4) |

**Used By:** fct_clinical_event, fct_quality_event

---

#### dim_clinical_event_type

| Column | Type | Description |
|--------|------|-------------|
| event_type_sk (PK) | INT | Surrogate key |
| event_type_code | VARCHAR(50) | Complication, Infection, Hospitalization, etc. |
| event_type_name | VARCHAR(100) | Full description |
| event_category | VARCHAR(50) | Category for grouping |

**Used By:** fct_clinical_event

---

#### dim_icd_code

| Column | Type | Description |
|--------|------|-------------|
| icd_code_sk (PK) | INT | Surrogate key |
| icd_code | VARCHAR(20) | ICD-10-CM code |
| icd_description | VARCHAR(500) | Code description |
| icd_category | VARCHAR(100) | Major category |

**Used By:** fct_clinical_event

---

#### dim_event_outcome

| Column | Type | Description |
|--------|------|-------------|
| outcome_sk (PK) | INT | Surrogate key |
| outcome_code | VARCHAR(20) | Resolved, Ongoing, Worsened, Improved |
| outcome_name | VARCHAR(50) | Full name |

**Used By:** fct_clinical_event

---

#### dim_quality_event_type

| Column | Type | Description |
|--------|------|-------------|
| quality_event_type_sk (PK) | INT | Surrogate key |
| event_type_code | VARCHAR(50) | Protocol Violation, Data Quality, Equipment Failure, etc. |
| event_type_name | VARCHAR(100) | Full description |
| severity_category | VARCHAR(50) | Expected severity category |

**Used By:** fct_quality_event

---

#### dim_quality_event_status

| Column | Type | Description |
|--------|------|-------------|
| status_sk (PK) | INT | Surrogate key |
| status_code | VARCHAR(20) | Open, In Progress, Resolved, Escalated |
| status_name | VARCHAR(50) | Full status name |

**Used By:** fct_quality_event

---

## Star Schema Diagrams

### Central Treatment Session Schema

```
                    dim_patient
                         |
         dim_provider ----+---- dim_facility
              |           |           |
              +-----------+-----------+
                          |
        dim_treatment_modality ---- fct_treatment_session ---- dim_date
                |                   |                           |
    dim_treatment_protocol      dim_episode_of_care        dim_time
                                    |
                            dim_session_status
```

### Lab Results Schema

```
         dim_patient      dim_facility
              |               |
              +-------+-------+
                      |
              dim_lab_test ---- fct_lab_result ---- dim_date
                  |             |                    |
          dim_abnormal_flag     dim_unit         dim_time
                              |
                    dim_episode_of_care (optional)
```

---

## Design Patterns

### 1. Conformed Dimensions
All fact tables that need patient information use the same `dim_patient` surrogate key, ensuring consistency across queries and dashboards.

### 2. Junk Dimensions (Flags and Status)
Boolean and categorical flags are moved to separate dimension tables (e.g., `dim_abnormal_flag`) for cleanliness and performance.

### 3. Slowly Changing Dimensions
- **Type 1 (Overwrite):** Used for facility data where history is not important
- **Type 2 (Track History):** Used for patient, provider, and episode data to support historical analysis

### 4. Degenerate Dimensions
Session-specific identifiers (e.g., `cancellation_reason`) remain in the fact table rather than creating single-column dimensions.

### 5. Late-Arriving Facts
None expected in the treatment session domain (sessions finalize within 24 hours).

---

## Aggregation Hierarchy

For performant dashboards, the following pre-aggregated tables can be created:

```
fct_treatment_session_by_modality_day
  ├─ Grain: One row per facility per modality per day
  ├─ Columns: facility_sk, modality_sk, date_sk, session_count, completed_count, avg_duration_minutes

fct_treatment_session_by_provider_month
  ├─ Grain: One row per provider per month
  ├─ Columns: provider_sk, date_sk, session_count, completed_count, avg_treatment_delivered_pct

fct_lab_result_by_test_type_patient_year
  ├─ Grain: One row per patient per test type per year
  ├─ Columns: patient_sk, test_sk, date_sk, avg_value, min_value, max_value, abnormal_count
```

---

*Last Updated: 2026-07-22*  
*Version: 1.0*
