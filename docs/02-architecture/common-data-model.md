# Common Data Model (CDM)

## Overview

The Kidney Care Analytics Platform's Common Data Model is a therapy-agnostic representation of nephrology care delivery. It captures universal clinical, operational, and quality concepts that apply across Peritoneal Dialysis, Hemodialysis, Acute Renal Therapy, and future modalities.

The CDM forms the foundation upon which therapy-specific extensions are built, ensuring:
- **Data Unity** - Patients moving between modalities have unified data history
- **Consistency** - Clinical entities defined once, reused everywhere
- **Extensibility** - New modalities extend, not replace, existing structures
- **Governance** - Single source of truth for enterprise-wide definitions

---

## Core Entities

### 1. ORGANIZATION

The healthcare organization operating the platform.

| Attribute | Type | Description |
|-----------|------|-------------|
| organization_id | UUID | Unique identifier |
| organization_name | String | Legal organization name |
| organization_type | Enum | IDO, Hospital, Health System, Clinic, etc. |
| npi | String | National Provider Identifier |
| ein | String | Employer Identification Number |
| state | String | Primary operating state |
| region | String | Geographic region |
| founded_year | Integer | Year established |
| status | Enum | Active, Inactive, Acquired, Merged |

---

### 2. FACILITY

A physical location where patient care is delivered.

| Attribute | Type | Description |
|-----------|------|-------------|
| facility_id | UUID | Unique identifier |
| organization_id | FK | Parent organization |
| facility_name | String | Facility name |
| facility_type | Enum | Clinic, Hospital, Satellite, Home |
| address | Address | Complete address |
| npi | String | Facility NPI |
| state_license | String | State license number |
| cms_certification | String | CMS certification number |
| capacity_beds | Integer | Licensed bed capacity |
| supported_modalities | Array | [PD, HD, Acute] modalities supported |
| status | Enum | Active, Inactive, Planned |
| opened_date | Date | Facility opening date |

---

### 3. PROVIDER

A clinical or administrative staff member.

| Attribute | Type | Description |
|-----------|------|-------------|
| provider_id | UUID | Unique identifier |
| organization_id | FK | Primary organization |
| provider_name | String | Full name |
| provider_type | Enum | Nephrologist, Nurse, Tech, Social Worker, etc. |
| license_type | Enum | MD, DO, RN, LPN, CCHT, etc. |
| license_number | String | State license number |
| npi | String | National Provider Identifier |
| credentials | Array | Board certifications, specialties |
| primary_facility_id | FK | Primary work location |
| status | Enum | Active, Inactive, Leave, Retired |
| hire_date | Date | Employment start date |

---

### 4. PATIENT

The individual receiving nephrology care.

| Attribute | Type | Description |
|-----------|------|-------------|
| patient_id | UUID | Unique identifier (fully de-identified in analytics layer) |
| mrn | String | Medical Record Number (encrypted) |
| ssn | String | Social Security Number (encrypted, HIPAA-protected) |
| first_name | String | (encrypted) |
| last_name | String | (encrypted) |
| date_of_birth | Date | (encrypted) |
| gender | Enum | M, F, Other, Unknown |
| race | Array | [Race codes per OMB standards] |
| ethnicity | String | Hispanic/Latino, Non-Hispanic |
| primary_language | String | English, Spanish, etc. |
| marital_status | Enum | Single, Married, Divorced, Widowed, Unknown |
| insurance_primary | String | Primary insurance identifier |
| insurance_secondary | String | Secondary insurance identifier |

---

### 5. PATIENT_DEMOGRAPHIC

Extended patient demographic attributes (slowly changing).

| Attribute | Type | Description |
|-----------|------|-------------|
| patient_demographic_id | UUID | Unique identifier |
| patient_id | FK | Reference to patient |
| address | Address | Current residence |
| phone | String | Contact phone (encrypted) |
| email | String | Contact email (encrypted) |
| emergency_contact_name | String | (encrypted) |
| emergency_contact_phone | String | (encrypted) |
| employment_status | Enum | Employed, Unemployed, Retired, Disabled |
| education_level | Enum | <HS, HS, Some College, College, Graduate |
| effective_from_date | Date | SCD Type 2 effective date |
| effective_to_date | Date | SCD Type 2 end date |
| is_current | Boolean | Whether this is current record |

---

### 6. EPISODE_OF_CARE

A continuous period of nephrology care, potentially spanning multiple treatment sessions and modalities.

| Attribute | Type | Description |
|-----------|------|-------------|
| episode_id | UUID | Unique identifier |
| patient_id | FK | Patient receiving care |
| episode_type | Enum | Initial Assessment, Active Treatment, Transition, End of Life |
| primary_modality | Enum | PD, HD, Acute, Conservative |
| initial_encounter_date | Date | Episode start date |
| termination_date | Date | Episode end date (NULL if active) |
| termination_reason | Enum | Transplant, Transfer, Death, Recovery, Modality Change |
| nephrologist_id | FK | Primary nephrologist |
| primary_facility_id | FK | Primary care facility |
| ckd_stage | Enum | Stage 1-5 |
| dialysis_vintage_days | Integer | Days on dialysis at episode start |
| comorbidities | Array | [ICD-10 codes] |
| status | Enum | Active, Closed, Archived |

---

### 7. TREATMENT_SESSION

The central business event: a single treatment delivered to a patient.

| Attribute | Type | Description |
|-----------|------|-------------|
| session_id | UUID | Unique identifier |
| episode_id | FK | Parent episode of care |
| patient_id | FK | Patient receiving treatment |
| facility_id | FK | Facility where treatment occurred |
| provider_id | FK | Primary clinical provider |
| treatment_modality | Enum | PD, HD, Acute |
| scheduled_start_time | DateTime | Planned start |
| actual_start_time | DateTime | Actual start |
| scheduled_end_time | DateTime | Planned end |
| actual_end_time | DateTime | Actual end |
| session_duration_minutes | Integer | Actual duration |
| treatment_protocol_id | FK | Protocol used |
| session_status | Enum | Scheduled, In Progress, Completed, Cancelled, Abandoned |
| cancellation_reason | String | If cancelled, why? |
| quality_flags | Array | [Quality issues detected] |
| intended_treatment_time | Integer | Target minutes |
| actual_treatment_time | Integer | Actual minutes |
| treatment_delivered_pct | Decimal | (actual_treatment_time / intended_treatment_time) * 100 |

---

### 8. TREATMENT_PROTOCOL

A standardized treatment protocol defining parameters for a specific therapy type.

| Attribute | Type | Description |
|-----------|------|-------------|
| protocol_id | UUID | Unique identifier |
| organization_id | FK | Organization that defined it |
| protocol_name | String | Name of protocol |
| protocol_type | Enum | PD, HD, Acute, Hybrid |
| description | String | Clinical description |
| version | String | Version number |
| effective_from_date | Date | Version effective date |
| effective_to_date | Date | Version end date |
| approved_by_provider_id | FK | Approving nephrologist |
| approval_date | Date | When approved |
| status | Enum | Draft, Active, Superseded, Retired |
| modality_specific_params | JSON | Modality-specific settings |

---

### 9. LABORATORY_TEST_RESULT

A clinical laboratory test result.

| Attribute | Type | Description |
|-----------|------|-------------|
| lab_result_id | UUID | Unique identifier |
| session_id | FK | Associated session (if session-specific) |
| episode_id | FK | Associated episode (if not session-specific) |
| patient_id | FK | Patient whose test |
| facility_id | FK | Facility where test performed |
| provider_id | FK | Ordering provider |
| test_code | String | LOINC or internal code |
| test_name | String | Test description |
| test_type | Enum | Chemistry, Hematology, Immunology, Microbiology |
| specimen_collection_time | DateTime | When specimen collected |
| result_report_time | DateTime | When result reported |
| numeric_value | Decimal | Test result value |
| numeric_unit | String | Unit of measurement |
| reference_range | String | Normal range |
| reference_gender | String | M, F, or both |
| abnormal_flag | Enum | Normal, Low, High, Critical |
| method | String | Test methodology |
| notes | String | Clinical notes about result |

---

### 10. VITAL_SIGN

A clinical vital sign measurement.

| Attribute | Type | Description |
|-----------|------|-------------|
| vital_id | UUID | Unique identifier |
| session_id | FK | Associated session |
| patient_id | FK | Patient measured |
| facility_id | FK | Facility where measured |
| measurement_time | DateTime | When measured |
| vital_type | Enum | Systolic BP, Diastolic BP, Heart Rate, Temperature, Respiratory Rate, Weight, Interdialytic Weight Gain |
| numeric_value | Decimal | Measurement value |
| numeric_unit | String | Unit of measurement |
| body_site | String | Where measured (e.g., "left arm") |
| measurement_device | String | Device used |
| measurement_method | String | Method used |
| notes | String | Clinical notes |

---

### 11. MEDICATION_ADMINISTRATION

Administration of medication to a patient.

| Attribute | Type | Description |
|-----------|------|-------------|
| med_admin_id | UUID | Unique identifier |
| session_id | FK | Associated session (if applicable) |
| patient_id | FK | Patient receiving medication |
| facility_id | FK | Facility where administered |
| provider_id | FK | Provider administering |
| medication_code | String | NDC or internal code |
| medication_name | String | Medication name |
| medication_route | Enum | IV, PO, IM, SC, Intraperitoneal, etc. |
| administration_time | DateTime | When administered |
| dose_value | Decimal | Dose quantity |
| dose_unit | String | Unit of measurement |
| dose_frequency | String | Frequency prescribed |
| indication | String | Clinical reason for administration |
| provider_notes | String | Provider documentation |

---

### 12. CLINICAL_EVENT

A significant clinical occurrence or intervention.

| Attribute | Type | Description |
|-----------|------|-------------|
| event_id | UUID | Unique identifier |
| session_id | FK | Associated session (if applicable) |
| episode_id | FK | Associated episode |
| patient_id | FK | Patient experiencing event |
| facility_id | FK | Facility where event occurred |
| event_type | Enum | Complication, Infection, Hospitalization, Emergency, Intervention, Transfusion |
| event_code | String | Clinical code (ICD-10, SNOMED CT) |
| event_description | String | Description of event |
| event_start_time | DateTime | When event began |
| event_end_time | DateTime | When event resolved |
| severity | Enum | Mild, Moderate, Severe, Critical |
| provider_id | FK | Provider documenting |
| action_taken | String | Intervention or treatment |
| outcome | Enum | Resolved, Ongoing, Worsened, Improved |

---

### 13. QUALITY_EVENT

A quality or compliance issue detected.

| Attribute | Type | Description |
|-----------|------|-------------|
| quality_event_id | UUID | Unique identifier |
| session_id | FK | Associated session |
| facility_id | FK | Facility where detected |
| protocol_id | FK | Protocol potentially violated |
| event_type | Enum | Protocol Violation, Data Quality Issue, Equipment Failure, Staff Issue |
| event_code | String | Standardized event code |
| severity | Enum | Minor, Major, Critical |
| description | String | Detailed description |
| detected_time | DateTime | When detected |
| reported_by_provider_id | FK | Provider reporting |
| root_cause | String | Root cause analysis result |
| corrective_action | String | Action taken to correct |
| resolution_date | Date | When resolved |
| status | Enum | Open, In Progress, Resolved, Escalated |

---

## Relationship Model

```
ORGANIZATION
  ├─ operates → FACILITY (1:N)
  ├─ employs → PROVIDER (1:N)
  └─ defines → TREATMENT_PROTOCOL (1:N)

FACILITY
  ├─ admits → PATIENT (1:N)
  └─ executes → TREATMENT_SESSION (1:N)

PROVIDER
  ├─ manages → PATIENT (1:N)
  ├─ manages → EPISODE_OF_CARE (1:N)
  └─ delivers → TREATMENT_SESSION (1:N)

PATIENT
  ├─ has → PATIENT_DEMOGRAPHIC (1:1 or 1:N with SCD)
  ├─ has → EPISODE_OF_CARE (1:N)
  ├─ undergoes → TREATMENT_SESSION (1:N)
  ├─ has → LABORATORY_TEST_RESULT (1:N)
  ├─ has → VITAL_SIGN (1:N)
  ├─ receives → MEDICATION_ADMINISTRATION (1:N)
  ├─ experiences → CLINICAL_EVENT (1:N)
  └─ subject of → QUALITY_EVENT (0:N)

EPISODE_OF_CARE
  ├─ contains → TREATMENT_SESSION (1:N)
  ├─ supervised_by → PROVIDER (N:1)
  └─ located_at → FACILITY (N:1)

TREATMENT_SESSION
  ├─ uses → TREATMENT_PROTOCOL (N:1)
  ├─ generates → LABORATORY_TEST_RESULT (0:N)
  ├─ generates → VITAL_SIGN (0:N)
  ├─ includes → MEDICATION_ADMINISTRATION (0:N)
  ├─ may_include → CLINICAL_EVENT (0:N)
  └─ may_have → QUALITY_EVENT (0:N)
```

---

## Key Design Decisions

### Why Treatment Session is Central
- Atomic unit of therapy delivery
- Can be measured and compared across modalities
- Generates all downstream clinical data
- Supports time-series and cohort analysis
- Can be aggregated to sessions/month, sessions/modality, etc.

### Why Episode of Care Exists
- Some data (e.g., comorbidities, CKD stage) is episode-level, not session-level
- Patients have multiple episodes over time
- Episodes span therapy transitions
- Supports longitudinal patient analytics

### Why Dimensions Are Separate
- Patient/Provider/Facility attributes change slowly
- Fact tables must remain immutable
- Supports efficient slowly-changing dimension (SCD) handling
- Enables dimensional analysis ("all sessions by male patients age 65+")

### Why Modality is in Fact Tables
- Must support cross-modality queries
- Modality determines which extensions apply
- Enables modality-comparison analytics
- Future-proofs for new modalities

---

## Extension Pattern

When adding a new therapy modality:

1. **Extend TREATMENT_PROTOCOL** with modality-specific parameters
2. **Create modality-specific dimensions** (e.g., `dim_pd_exchange_protocol`)
3. **Create modality-specific fact tables** (e.g., `fct_pd_exchange`)
4. **Ensure all modality-specific dimensions join through shared core dimensions**

Example for PD:
```
fct_pd_exchange
  ├─ joins to dim_patient (shared)
  ├─ joins to dim_treatment_session (shared)
  ├─ joins to dim_pd_exchange_type (PD-specific)
  └─ joins to dim_pd_solution (PD-specific)
```

---

## Data Quality Rules

For all CDM entities:
1. **Uniqueness** - Each entity has a unique surrogate key (UUID)
2. **Referential Integrity** - All foreign keys reference valid parent records
3. **Not Null** - All required attributes populated
4. **Domain Validation** - Enum values are valid; dates are logical
5. **Business Rule Validation** - End dates ≥ start dates; quality flags valid
6. **Temporal Integrity** - Session times are consistent and logical
7. **Audit Trail** - All modifications tracked with timestamp and user

---

*Last Updated: 2026-07-22*  
*Version: 1.0*
