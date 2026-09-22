# Kidney Care Analytics Platform

A therapy-agnostic analytics platform for nephrology care delivery supporting Peritoneal Dialysis (PD), Hemodialysis (HD), and Acute Renal Therapy.

## Documentation Structure

- **[Vision & Strategy](./docs/01-vision/vision.md)** - Platform vision, business objectives, and strategic goals
- **[Architecture Principles](./docs/02-architecture/principles.md)** - Core design principles guiding the platform
- **[Common Data Model](./docs/02-architecture/common-data-model.md)** - Therapy-agnostic business entities
- **[Dimensional Model](./docs/02-architecture/dimensional-model.md)** - Kimball fact and dimension tables
- **[Enterprise Bus Matrix](./docs/03-enterprise/enterprise-bus-matrix.md)** - Cross-functional data requirements
- **[Stakeholders](./docs/04-stakeholders/stakeholders.md)** - Stakeholder profiles and requirements
- **[KPIs & Metrics](./docs/05-kpis/kpis.md)** - Business metrics and performance indicators
- **[PD Domain Model](./docs/06-implementation/pd-domain-model.md)** - Phase 1: Peritoneal Dialysis specifics
- **[Phased Implementation](./docs/06-implementation/phased-approach.md)** - Implementation roadmap
- **[Platform Tooling](./docs/07-tooling/platform-tooling.md)** - Data platform tooling requirements (MinIO, ingest, dbt, CI/CD)
- **[MVP Local Foundation](./docs/07-tooling/mvp-local-foundation.md)** - Run the local AWS-shaped learning environment
- **[Device Simulator](./services/device-simulator/README.md)** - Generate synthetic APD therapy events for Kinesis

## Platform Principles

1. **Therapy-Agnostic Common Data Model** - Single source of truth for all modalities
2. **Kimball Dimensional Modeling** - Facts (business events) and Dimensions (reusable entities)
3. **Treatment Session Centric** - Central business event across all therapies
4. **Analytics First** - Support for BI, semantic layers, AI/ML, and GenAI
5. **Production Ready** - DEV → QA → PROD engineering practices

## Quick Links

- **Phase 1 Focus:** Peritoneal Dialysis (PD)
- **Central Event:** Treatment Session
- **Data Modeling:** Kimball Dimensional Model
- **Support:** Analytics, Semantic Layer, AI/ML, Generative AI

---

*Last Updated: 2026-07-22*
