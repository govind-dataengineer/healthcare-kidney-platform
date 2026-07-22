# Architecture Principles

## Core Principles

### 1. Therapy-Agnostic Common Data Model (CDM)

**Principle:** Design a unified data model that represents common nephrology care concepts independent of specific therapy modalities.

**Rationale:** 
- Patients transition between therapies throughout their kidney disease journey
- Clinical entities (Patient, Provider, Laboratory Results, Vital Signs) are universal
- Therapy-specific details extend, not replace, the common model
- Avoids data silos and duplication

**Implementation:**
- Core entities: Patient, Provider, Facility, Episode of Care, Treatment Session
- Therapy-specific dimensions: PD-specific parameters, HD-specific parameters, Acute-specific parameters
- Shared fact tables: Lab Results, Vital Signs, Clinical Events, Quality Events
- Therapy-specific fact tables: PD_Session_Facts, HD_Session_Facts, Acute_Session_Facts

**Design Constraint:** 
> A patient's clinical history must be queryable in a single fact table regardless of therapy modality without requiring manual union queries.

---

### 2. Kimball Dimensional Modeling

**Principle:** Structure analytics data using Ralph Kimball's dimensional modeling approach with facts (business events) and dimensions (reusable business entities).

**Rationale:**
- Proven approach for healthcare analytics
- Supports complex queries with excellent performance
- Dimensions are reusable across multiple fact tables
- Intuitive for business users and BI tool developers

**Structure:**
```
FACTS (Business Events)
├─ fct_treatment_session (central event)
├─ fct_lab_result
├─ fct_vital_sign
├─ fct_medication_administration
├─ fct_clinical_event
└─ fct_quality_event

DIMENSIONS (Reusable Entities)
├─ dim_patient
├─ dim_provider
├─ dim_facility
├─ dim_date
├─ dim_time
├─ dim_treatment_modality
├─ dim_clinical_protocol
├─ dim_episode_of_care
└─ dim_patient_demographic
```

**Design Constraint:**
> All fact tables must join to dim_patient and dim_date. No orphaned facts.

---

### 3. Treatment Session as Central Business Event

**Principle:** Treat a single treatment session as the central, atomic business event around which all other events orbit.

**Rationale:**
- A treatment session is a discrete, measurable unit of therapy delivery
- Sessions generate clinical data, quality metrics, operational data, and financial data
- Cross-modality comparable: PD session, HD session, Acute session
- Enables cohort analysis and quality measurement

**Key Attributes:**
- Session ID (globally unique)
- Patient ID
- Therapy Modality
- Session Start/End Time
- Duration
- Clinical Protocol Used
- Treatment Parameters
- Outcomes (pre/post vitals, labs, complications)
- Quality Flags

**Design Constraint:**
> Every clinical event, measurement, or outcome must be traceable to a specific treatment session (or Episode of Care if not session-specific).

---

### 4. Facts Represent Business Events, Dimensions Represent Entities

**Principle:** Facts capture "what happened" (events); dimensions describe "what it was about" (entities).

**Rationale:**
- Clear separation of concerns
- Dimensions are stable; facts are immutable and ever-growing
- Enables efficient slowly-changing-dimension (SCD) handling
- Supports time-based analysis (trends, comparisons)

**Examples:**

| Fact Table | Event | Key Dimensions |
|-----------|-------|-----------------|
| fct_treatment_session | Therapy delivered | Patient, Provider, Facility, Date/Time, Modality |
| fct_lab_result | Lab test performed | Patient, Test Type, Provider, Date, Facility |
| fct_vital_sign | Vital sign measured | Patient, Date/Time, Vital Type, Facility |
| fct_quality_event | Quality issue detected | Facility, Protocol, Date, Event Type |

**Design Constraint:**
> Dimensions must not change at session granularity (SCD Type 1 or 2 implementation required).

---

### 5. Build Once, Extend for Each Modality

**Principle:** Design the common model and dimensional structure to accommodate new therapy modalities without redesign; extensions should be additive, not disruptive.

**Rationale:**
- Organizations support multiple modalities simultaneously
- Patient journey spans modalities
- Reduces rework and maintains data integrity
- Enables comparative analytics across modalities

**Extension Pattern:**

```
Phase 1: Common + PD Specifics
├─ Common Dimensions (Patient, Provider, Facility, Date, etc.)
├─ Common Facts (Lab Results, Vital Signs, etc.)
├─ PD Dimensions (pd_dimension_patient_peritoneal_profile, etc.)
└─ PD Facts (fct_pd_session, fct_pd_exchange, etc.)

Phase 2: Add HD (No redesign of Phase 1)
├─ Common Dimensions (unchanged)
├─ Common Facts (unchanged)
├─ HD Dimensions (hd_dimension_patient_vascular_access, etc.)
└─ HD Facts (fct_hd_session, fct_hd_treatment, etc.)

Phase 3: Add Acute (No redesign of Phases 1-2)
├─ Common Dimensions (unchanged)
├─ Common Facts (unchanged)
├─ Acute Dimensions (acute_dimension_patient_arf_profile, etc.)
└─ Acute Facts (fct_acute_session, fct_acute_monitoring, etc.)
```

**Design Constraint:**
> Adding a new therapy modality must not require schema changes to existing fact or dimension tables.

---

### 6. Quality First, Performance Second

**Principle:** Prioritize data quality and governance over raw query performance; optimize performance within quality constraints.

**Rationale:**
- Healthcare analytics has regulatory and patient safety implications
- Poor quality data leads to incorrect clinical decisions
- Compliance and audit trail requirements are non-negotiable
- Performance optimization opportunities exist after quality baseline

**Quality Framework:**
- Data Lineage: Track all transformations from source to BI layer
- Audit Trails: Maintain immutable change logs
- Data Validation: Schema validation, referential integrity, business rule checks
- Reconciliation: Regular validation against source systems
- Documentation: Complete data dictionaries and business logic definitions

**Design Constraint:**
> No data loads without passing automated quality validation gates. Audit trail required for all modifications.

---

### 7. Multi-Use Design (Analytics, Semantic Layer, AI/ML, GenAI)

**Principle:** Design the dimensional model and data marts to support multiple use cases: traditional BI, semantic layer queries, machine learning models, and generative AI applications.

**Rationale:**
- Single platform reduces infrastructure complexity and cost
- Consistent data definitions across use cases
- Supports advanced analytics without custom pipelines
- Enables AI/ML models to benefit from governed data

**Use Case Support:**

| Use Case | Requirements | Data Access |
|----------|--------------|------------|
| **Traditional BI** | Pre-aggregated data, optimized for OLAP queries | Dimensional fact tables, cubes |
| **Semantic Layer** | Business entity definitions, metric definitions, attributes | Semantic models, governed metrics |
| **AI/ML Models** | Granular event-level data, feature engineering support | Fact tables, feature stores, time-series data |
| **Generative AI** | Structured data + context, lineage, explanations | Semantic layer + metadata, prompt engineering |

**Design Constraint:**
> The data model must support queries from OLAP tools, semantic layer engines (e.g., dbt Semantic Layer), Python/R ML frameworks, and LLM interfaces without transformation.

---

### 8. DEV → QA → PROD Engineering Practices

**Principle:** Maintain strict separation between development, quality assurance, and production environments with automated testing, validation, and deployment gates.

**Rationale:**
- Healthcare data requires rigorous validation before production use
- Prevents data corruption and ensures regulatory compliance
- Enables safe iteration and feature rollout
- Supports rollback and incident recovery

**Pipeline Requirements:**
- DEV: Sandbox for schema design, data model iteration, testing
- QA: Production-like environment with subset of real data, automated test suite, reconciliation
- PROD: Production data, read-only analytics access, audit logging, backup/disaster recovery

**Design Constraint:**
> Every change must pass automated tests in DEV and QA before production promotion. Manual deployments prohibited.

---

### 9. Reusable Dimensions, Conformed Dimensions

**Principle:** Design dimensions to be reusable across multiple fact tables; maintain conformed dimensions where the same entity appears in multiple contexts.

**Rationale:**
- Enables consistent drill-down and filtering across fact tables
- Reduces data redundancy and maintenance burden
- Supports enterprise-wide analytics
- Facilitates cross-functional analysis

**Patterns:**

| Conformed Dimension | Fact Tables Using It |
|-------------------|-------------------.|
| dim_patient | fct_treatment_session, fct_lab_result, fct_vital_sign, fct_medication |
| dim_facility | fct_treatment_session, fct_quality_event, fct_lab_result |
| dim_provider | fct_treatment_session, fct_clinical_event, fct_quality_event |
| dim_date | All fact tables |

**Design Constraint:**
> Dimensions must have stable, globally unique surrogate keys. No fact table should contain dimension attributes.

---

### 10. Privacy by Design

**Principle:** Build privacy, security, and compliance requirements into the data architecture from inception, not as afterthoughts.

**Rationale:**
- Healthcare data is protected health information (PHI)
- HIPAA compliance is mandatory
- Data governance and audit trails support compliance
- Patient privacy is an ethical imperative

**Requirements:**
- Role-based access control (RBAC) at row and column levels
- PII masking for non-clinical users
- Data lineage and audit logging
- Encryption at rest and in transit
- Regular security assessments and penetration testing
- Incident response and breach notification procedures

**Design Constraint:**
> No PII in fact tables. PII isolation in secure dimensions. Audit logs for all PHI access.

---

## Design Decision Framework

When designing data structures or making architectural choices:

1. **Align with CDM** - Does it fit the therapy-agnostic common model?
2. **Kimball Adherence** - Are facts and dimensions properly separated?
3. **Centrality** - Does it relate clearly to treatment sessions or patient episodes?
4. **Extensibility** - Can new modalities extend this without redesign?
5. **Quality** - Can we validate and audit this data?
6. **Multi-Use** - Will this support BI, ML, semantic layer, and GenAI?
7. **Governance** - Can we control access and maintain lineage?

---

*Last Updated: 2026-07-22*  
*Version: 1.0*
