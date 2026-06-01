# GIC v12 Repository Instructions

## Mission
Build a financial-data-modeling-based research system for GIC. Do not reduce the project to slide generation or prose generation.

## Read First
Before planning or editing code, read:
- `specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md`
- `specs/01_SOURCE_AND_EVIDENCE_POLICY.md`
- `schemas/02_CANONICAL_DATA_SCHEMA.yaml`
- `specs/03_REPORT_AND_DESIGN_CONTRACTS.md`
- `schemas/04_SECTOR_FINANCIAL_LENSES.yaml`
- `prompts/05_PROMPT_ORCHESTRATION_SPEC.md`
- `qa/06_QA_ACCEPTANCE_TESTS.md`

## Non-Negotiable Domain Rules
- Separate fact, derived metric, assumption, forecast, judgment, and falsifier.
- Require evidence linkage for material claims.
- Preserve three report modes: `COMPANY_REPORT`, `INDUSTRY_REPORT`, `INDUSTRY_TOP_PICK`.
- Treat official GIC templates as visual-design references, not fixed content templates.
- Keep company/industry outputs portrait and Top Pick output landscape.
- Do not release PDF/PPTX outputs unless QA gates pass.

## Implementation Expectations
- Prefer typed schemas and validation before rendering.
- Keep source files under `sources/reference/` and `sources/baseline/` immutable.
- Add tests for transformations and calculations.
- Document any external dependency before adding it.
- Start with an MVP skeleton and a DEFENSE-sector fixture; do not prematurely automate all sectors.

## Quality Gates
Run tests and report failures before claiming completion. A visually attractive output without evidence traceability or model assumptions is not accepted.
