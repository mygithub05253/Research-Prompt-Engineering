# GIC v12 DEFENSE MVP Implementation Plan

> **Status note:** This is the optional automation/coding plan. It is not the recommended first step if the target is a prompt-engineering product for ChatGPT, Claude Chat, or Gemini. For the no-code prompt-first MVP, use `docs/PROMPT_ENGINEERING_MVP_PLAN.md` and `prompts/08_NO_CODE_PROMPT_PACK.md`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first DEFENSE-sector MVP skeleton that turns source manifests and normalized public-data facts into driver maps, report-plan JSON, HTML preview drafts, and QA lint reports without weakening evidence traceability.

**Architecture:** Use a small Python package with typed domain objects, explicit loaders, deterministic fixture data, and a CLI that runs the end-to-end skeleton. Rendering remains downstream of validated intermediate data: source register -> normalized facts -> sector lens -> drivers -> report plan -> HTML preview -> QA report.

**Tech Stack:** Python 3.11+, pytest, YAML/JSON intermediate files, optional production dependencies requiring user confirmation before coding (`pydantic`, `PyYAML`, `jinja2`, `typer`, `ruff`).

---

## 0. Documents Read Before Planning

- `README.md`
- `specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md`
- `specs/01_SOURCE_AND_EVIDENCE_POLICY.md`
- `schemas/02_CANONICAL_DATA_SCHEMA.yaml`
- `specs/03_REPORT_AND_DESIGN_CONTRACTS.md`
- `schemas/04_SECTOR_FINANCIAL_LENSES.yaml`
- `prompts/05_PROMPT_ORCHESTRATION_SPEC.md`
- `qa/06_QA_ACCEPTANCE_TESTS.md`
- `AGENTS.md`
- `CLAUDE.md`
- `prompts/07_HANDOFF_PROMPT_CODEX_CLAUDE.md`

Observed repository state:

- The repository currently contains specifications, schemas, prompts, QA policy, a source manifest, and reference/baseline sources.
- There is no existing `src/`, `tests/`, `pyproject.toml`, or Git metadata in this folder.
- `sources/reference/` and `sources/baseline/` must remain immutable inputs.

## 1. Fixed Rules This MVP Must Preserve

- Facts, derived metrics, assumptions, forecasts, judgments, and falsifiers remain separate data objects.
- Every material claim in a report plan must point to fact, assumption, driver, or falsifier identifiers.
- The three modes remain separate: `COMPANY_REPORT`, `INDUSTRY_REPORT`, `INDUSTRY_TOP_PICK`.
- Official GIC forms are design-system references, not fixed content templates.
- `COMPANY_REPORT` and `INDUSTRY_REPORT` use portrait orientation; `INDUSTRY_TOP_PICK` uses 16:9 landscape orientation.
- `deep-research-report.md` is a methodology source, not a factual source for an investment conclusion.
- The first implementation target is `DEFENSE`; other sector lenses are loaded only enough to prove they are not broken.
- No PDF/PPTX output may be labeled release-ready until QA gates pass.

## 2. MVP Scope

In scope:

- Source manifest loader and generated audit manifest.
- Markdown/JSON normalization scaffold.
- OpenDART financial fact loader interface with mock-backed tests.
- Sector lens loader with `DEFENSE` KPI checklist.
- Deterministic facts -> drivers -> report plan pipeline.
- Static HTML preview prototype from report-plan JSON.
- QA lint runner that emits `PASS`, `FAIL`, and `WARNING` gates.
- At least five calculation/data-consistency unit tests.

Out of scope for the first MVP:

- Live OpenDART API calls as a required test path.
- Full PDF/PPTX rendering.
- Design token extraction from official PPTX/PDF.
- Automated web research or paid data ingestion.
- Full valuation engine beyond interface and provenance checks.
- Any mutation of files under `sources/reference/` or `sources/baseline/`.

## 3. Planned File Changes

### Create

- `pyproject.toml`  
  Defines package metadata, Python version, test command, and approved dependencies.

- `src/gic_v12/__init__.py`  
  Package marker and version constant.

- `src/gic_v12/domain.py`  
  Typed domain objects for source records, facts, derived metrics, assumptions, drivers, claims, report pages, and QA gates.

- `src/gic_v12/io/source_manifest.py`  
  Loads `sources/SOURCE_MANIFEST.yaml`, classifies method/design/baseline sources, and writes `outputs/<run_id>/audit/source_register.md`.

- `src/gic_v12/io/normalizers.py`  
  Provides `MarkdownNormalizer` and `JsonFactNormalizer` interfaces. Markdown normalization extracts metadata, headings, tables, and source references; JSON normalization validates pre-structured facts.

- `src/gic_v12/io/opendart.py`  
  Defines an `OpenDartClient` protocol and mockable loader methods for `fnlttSinglAcntAll`, `fnlttSinglIndx`, and XBRL metadata.

- `src/gic_v12/sector_lens.py`  
  Loads `schemas/04_SECTOR_FINANCIAL_LENSES.yaml`, exposes `DEFENSE` required KPIs, valuation methods, and falsifiers.

- `src/gic_v12/calculations.py`  
  Implements deterministic derived calculations for OPM, YoY, FCF, net debt, and contamination checks.

- `src/gic_v12/pipeline.py`  
  Orchestrates source register, normalized facts, sector lens, driver map, claim evidence matrix, and report plan generation.

- `src/gic_v12/render/html_preview.py`  
  Renders a static HTML draft from `report_plan.json`, visibly marking it as draft until `release_approved` is true.

- `src/gic_v12/qa/lint.py`  
  Runs evidence, calculation, scenario, narrative, mode/design, and render-integrity lint gates.

- `src/gic_v12/cli.py`  
  Provides a command to run the DEFENSE fixture pipeline and write an `outputs/<run_id>/` bundle.

- `tests/fixtures/defense_source_manifest.yaml`  
  Minimal source manifest fixture with method/design/baseline entries and one synthetic primary financial source.

- `tests/fixtures/defense_normalized_facts.json`  
  Synthetic but schema-shaped DEFENSE facts for backlog, export pipeline, export mix, capacity/delivery, OPM, cash conversion, and FX/risk conditions.

- `tests/fixtures/opendart_fnltt_mock.json`  
  Mock OpenDART payload containing required metadata: `corp_code`, `bsns_year`, `reprt_code`, `fs_div`, `rcept_no`, `currency`, and `retrieved_at`.

- `tests/test_source_manifest.py`  
  Verifies manifest loading, source type separation, and generated source-register fields.

- `tests/test_normalizers.py`  
  Verifies JSON fact validation and Markdown normalization scaffold output.

- `tests/test_opendart_loader.py`  
  Verifies mock OpenDART records become `financial_fact` objects with provenance metadata.

- `tests/test_sector_lens.py`  
  Verifies `DEFENSE` lens loads required KPIs, valuation methods, and falsifiers.

- `tests/test_calculations.py`  
  Verifies OPM, YoY, FCF, net debt, CFS/OFS contamination, and FY/Q/YTD contamination checks.

- `tests/test_pipeline.py`  
  Verifies facts -> drivers -> report plan output contains linked `fact_ids`, `driver_ids`, `falsifier_ids`, and correct orientation by mode.

- `tests/test_qa_lint.py`  
  Verifies missing evidence fails, draft preview is not released, and a well-linked fixture produces non-fatal `PASS`/`WARNING` gates.

- `outputs/.gitkeep`  
  Keeps the output folder available without committing generated run artifacts.

### Modify

- `docs/IMPLEMENTATION_PLAN.md`  
  This planning document only.

No planned MVP edit should touch:

- `sources/reference/*`
- `sources/baseline/*`
- Existing specs/schemas/prompts/QA policy, unless the user explicitly approves a schema-policy revision.

## 4. Proposed Runtime Contract

### CLI Command

```powershell
python -m gic_v12.cli run-fixture `
  --sector DEFENSE `
  --mode COMPANY_REPORT `
  --as-of-date 2026-05-31 `
  --run-id defense_mvp_fixture
```

Expected generated bundle:

```text
outputs/defense_mvp_fixture/
├─ audit/
│  ├─ source_register.md
│  ├─ evidence_matrix.csv
│  └─ qa_report.md
├─ data/
│  ├─ normalized_facts.json
│  ├─ driver_map.json
│  └─ sector_kpi_checklist.json
├─ narrative/
│  └─ report_plan.json
└─ deliverables/
   └─ preview.html
```

Release behavior:

- `preview.html` is always labeled `DRAFT`.
- `qa_report.release_approved` is `false` until every required gate passes.
- PDF/PPTX outputs are not generated by default in the first MVP.

## 5. Data Boundaries

### Source Register

Minimum accepted source record:

```json
{
  "source_id": "S_DART_DEFENSE_001",
  "source_type": "PRIMARY_FINANCIAL",
  "title": "Mock OpenDART annual financial statement",
  "publisher": "Financial Supervisory Service OpenDART",
  "published_date": "2026-03-15",
  "as_of_date": "2025-12-31",
  "retrieved_at": "2026-05-31T09:00:00+09:00",
  "local_path_or_uri": "tests/fixtures/opendart_fnltt_mock.json",
  "coverage": ["revenue", "operating_income", "cash", "debt"],
  "reliability_note": "Mock fixture shaped after OpenDART; not a factual company conclusion."
}
```

### Financial Fact

Minimum accepted fact record:

```json
{
  "fact_id": "F_DEFENSE_BACKLOG_FY2025",
  "entity": "DEFENSE_FIXTURE_CO",
  "metric_group": "sector_kpi",
  "metric_name": "수주잔고",
  "period": "FY2025",
  "period_type": "FY",
  "value": 12500,
  "value_text": null,
  "unit": "KRW_billion",
  "currency": "KRW",
  "fs_div": "NA",
  "actual_or_estimate": "actual",
  "source_id": "S_COMPANY_DEFENSE_001",
  "source_locator": "fixture table: backlog",
  "validation_status": "verified",
  "notes": "Synthetic fixture for pipeline validation."
}
```

### Driver Output

The DEFENSE driver map must include at least:

- `DEFENSE_BACKLOG_TO_REVENUE`
- `DEFENSE_EXPORT_PIPELINE_TO_GROWTH`
- `DEFENSE_EXPORT_MIX_TO_MARGIN`
- `DEFENSE_CAPACITY_DELIVERY_TO_RECOGNITION`
- `DEFENSE_CASH_CONVERSION_TO_FCF`
- `DEFENSE_FX_APPROVAL_LOCALIZATION_RISK`

Each driver must include:

- `input_fact_ids`
- `input_kpi_ids`
- `transmission.revenue`
- `transmission.margin`
- `transmission.cash_flow`
- `transmission.valuation`
- `lag_or_timing`
- `falsifiers`

## 6. Task Plan

### Task 1: Project Skeleton

**Files:**

- Create: `pyproject.toml`
- Create: `src/gic_v12/__init__.py`
- Create: `src/gic_v12/cli.py`
- Create: `tests/test_imports.py`

- [ ] **Step 1: Write the import smoke test**

```python
def test_package_imports():
    import gic_v12

    assert gic_v12.__version__ == "12.0.0-mvp"
```

- [ ] **Step 2: Run the smoke test**

Run:

```powershell
python -m pytest tests/test_imports.py -q
```

Expected before implementation: fails because `gic_v12` does not exist.

- [ ] **Step 3: Implement the package marker**

Create `src/gic_v12/__init__.py` with:

```python
__version__ = "12.0.0-mvp"
```

- [ ] **Step 4: Run the smoke test again**

Expected after implementation: `1 passed`.

### Task 2: Domain Model and Validation Layer

**Files:**

- Create: `src/gic_v12/domain.py`
- Create: `tests/test_domain.py`

- [ ] **Step 1: Add tests for object separation**

The test must instantiate one `FinancialFact`, one `DerivedMetric`, one `Assumption`, one `FinancialDriver`, one `ClaimEvidence`, and one `QaReport`. The test must assert that no class has fields that belong to another class, especially that `FinancialFact` has no `assumption_ids` and `Assumption` has no `source_locator`.

- [ ] **Step 2: Implement explicit domain types**

Use dataclasses or Pydantic models according to the dependency decision. Required type names:

- `SourceRecord`
- `FinancialFact`
- `DerivedMetric`
- `Assumption`
- `FinancialDriver`
- `ClaimEvidence`
- `ReportPlan`
- `QaGate`
- `QaReport`

- [ ] **Step 3: Verify schema-aligned enums**

Tests must cover report modes, source types, period types, financial statement division, actual/estimate status, and QA gate status.

### Task 3: Source Manifest Loader

**Files:**

- Create: `src/gic_v12/io/source_manifest.py`
- Create: `tests/fixtures/defense_source_manifest.yaml`
- Create: `tests/test_source_manifest.py`

- [ ] **Step 1: Write fixture manifest**

Fixture must include:

- one `METHOD` source for `reference/deep-research-report.md`
- one `DESIGN` source for the official GIC PPTX
- one `PRIMARY_FINANCIAL` source for the mock OpenDART fixture
- one `PRIMARY_COMPANY` source for synthetic DEFENSE KPI facts
- one baseline source that is explicitly marked non-factual

- [ ] **Step 2: Test source type separation**

Assert that methodology/design/baseline sources cannot be used as primary factual evidence.

- [ ] **Step 3: Implement loader and audit writer**

The loader must output source records with `source_id`, `source_type`, `title`, `publisher`, `published_date`, `as_of_date`, `retrieved_at`, `local_path_or_uri`, `coverage`, and `reliability_note`.

### Task 4: Markdown/JSON Normalization Scaffold

**Files:**

- Create: `src/gic_v12/io/normalizers.py`
- Create: `tests/test_normalizers.py`
- Create: `tests/fixtures/defense_normalized_facts.json`

- [ ] **Step 1: Test JSON fact fixture validation**

The fixture must include facts for all required DEFENSE KPIs and at least four financial statement facts: revenue, operating income, operating cash flow, and capex.

- [ ] **Step 2: Test Markdown scaffold behavior**

The Markdown normalizer must return document metadata, headings, extracted table blocks, and source references. It must not infer financial facts from prose in the first MVP.

- [ ] **Step 3: Implement normalizer interfaces**

Expose:

- `MarkdownNormalizer.normalize(path: Path) -> NormalizedDocument`
- `JsonFactNormalizer.load(path: Path) -> list[FinancialFact]`

### Task 5: OpenDART Loader Interface

**Files:**

- Create: `src/gic_v12/io/opendart.py`
- Create: `tests/fixtures/opendart_fnltt_mock.json`
- Create: `tests/test_opendart_loader.py`

- [ ] **Step 1: Write mock payload test**

The test must prove that a mock `fnlttSinglAcntAll` payload becomes financial facts with `corp_code`, `bsns_year`, `reprt_code`, `fs_div`, `rcept_no`, `currency`, and `retrieved_at` preserved in notes or metadata fields.

- [ ] **Step 2: Implement client protocol**

Expose:

- `OpenDartClient.fetch_single_account_all(corp_code, bsns_year, reprt_code, fs_div)`
- `OpenDartClient.fetch_financial_index(corp_code, bsns_year, reprt_code)`
- `OpenDartFactLoader.load_annual_facts(...)`

- [ ] **Step 3: Keep live API optional**

Live OpenDART calls must require `OPENDART_API_KEY`. Unit tests must not require network access.

### Task 6: DEFENSE Sector Lens Loader

**Files:**

- Create: `src/gic_v12/sector_lens.py`
- Create: `tests/test_sector_lens.py`

- [ ] **Step 1: Test DEFENSE lens**

Assert that the lens includes the six required KPIs from `schemas/04_SECTOR_FINANCIAL_LENSES.yaml`, three valuation methods, and four falsifiers.

- [ ] **Step 2: Implement loader**

Expose:

- `load_sector_lenses(path: Path) -> dict[str, SectorLens]`
- `get_sector_lens("DEFENSE") -> SectorLens`
- `SectorLens.required_kpi_names() -> list[str]`

### Task 7: Calculations and Consistency Checks

**Files:**

- Create: `src/gic_v12/calculations.py`
- Create: `tests/test_calculations.py`

- [ ] **Step 1: Test MVP calculations**

Required tests:

- `OPM = operating_income / revenue`
- `YoY = current / previous - 1`
- `FCF = operating_cash_flow - capex`
- `Net debt = total_debt - cash`
- CFS/OFS contamination check fails mixed tables
- FY/Q/YTD contamination check fails mixed period bases

- [ ] **Step 2: Implement calculation functions**

Functions:

- `calculate_op_margin(revenue, operating_income)`
- `calculate_yoy(current, previous)`
- `calculate_free_cash_flow(operating_cash_flow, capex)`
- `calculate_net_debt(total_debt, cash)`
- `assert_single_fs_div(facts)`
- `assert_compatible_period_basis(facts)`

### Task 8: Facts-to-Drivers-to-Report-Plan Pipeline

**Files:**

- Create: `src/gic_v12/pipeline.py`
- Create: `tests/test_pipeline.py`

- [ ] **Step 1: Test driver map generation**

Given DEFENSE facts, pipeline output must include the six DEFENSE drivers listed in this document. Each driver must carry at least one `input_fact_id`, one falsifier, and a financial transmission field.

- [ ] **Step 2: Test report mode separation**

For `COMPANY_REPORT` and `INDUSTRY_REPORT`, generated report plans must use `orientation: portrait`. For `INDUSTRY_TOP_PICK`, generated report plans must use `orientation: landscape`.

- [ ] **Step 3: Implement deterministic report plan builder**

The builder must create:

- `mode`
- `design_system: GIC_NAVY_ORANGE`
- `orientation`
- `pages_or_slides`
- `key_claim_ids`
- chart/table source labels
- visual QA notes

### Task 9: HTML Preview Prototype

**Files:**

- Create: `src/gic_v12/render/html_preview.py`
- Create: `tests/test_html_preview.py`

- [ ] **Step 1: Test draft labeling**

The rendered HTML must include a visible draft state and must not include the phrase `release approved` unless `qa_report.release_approved` is true.

- [ ] **Step 2: Test source labels**

Every rendered chart/table block in the fixture report plan must display a source label.

- [ ] **Step 3: Implement renderer**

The renderer must produce a static HTML file using GIC navy/orange design cues, Korean-compatible font fallback, and explicit source labels.

### Task 10: QA Lint Runner

**Files:**

- Create: `src/gic_v12/qa/lint.py`
- Create: `tests/test_qa_lint.py`

- [ ] **Step 1: Test fatal evidence failure**

A claim without `fact_ids`, `assumption_ids`, `driver_ids`, or `falsifier_ids` must fail `factual_traceability`.

- [ ] **Step 2: Test orientation gate**

`INDUSTRY_TOP_PICK` with portrait orientation must fail `design_compliance`.

- [ ] **Step 3: Test release approval gate**

`release_approved` must be true only when all fatal gates pass and render warnings are absent or explicitly allowed.

- [ ] **Step 4: Implement lint runner**

The runner must emit:

- `factual_traceability`
- `calculation_integrity`
- `scenario_transparency`
- `narrative_quality`
- `design_compliance`
- `render_integrity`
- `fatal_errors`
- `warnings`
- `recommended_fixes`
- `release_approved`

### Task 11: End-to-End Fixture Run

**Files:**

- Modify: `src/gic_v12/cli.py`
- Create: `tests/test_cli_fixture_run.py`
- Create: `outputs/.gitkeep`

- [ ] **Step 1: Test CLI output bundle**

Run the CLI against fixture data and assert that it writes:

- `audit/source_register.md`
- `audit/evidence_matrix.csv`
- `audit/qa_report.md`
- `data/normalized_facts.json`
- `data/driver_map.json`
- `data/sector_kpi_checklist.json`
- `narrative/report_plan.json`
- `deliverables/preview.html`

- [ ] **Step 2: Implement fixture command**

The command must run without OpenDART API credentials by using fixtures.

- [ ] **Step 3: Run full MVP tests**

Run:

```powershell
python -m pytest tests -q
```

Expected MVP target: all tests pass.

## 7. Test Plan

Minimum automated checks before claiming MVP completion:

- `python -m pytest tests/test_source_manifest.py -q`
- `python -m pytest tests/test_normalizers.py -q`
- `python -m pytest tests/test_opendart_loader.py -q`
- `python -m pytest tests/test_sector_lens.py -q`
- `python -m pytest tests/test_calculations.py -q`
- `python -m pytest tests/test_pipeline.py -q`
- `python -m pytest tests/test_html_preview.py -q`
- `python -m pytest tests/test_qa_lint.py -q`
- `python -m pytest tests/test_cli_fixture_run.py -q`
- `python -m pytest tests -q`

Manual review checklist after automated tests:

- Confirm `outputs/<run_id>/deliverables/preview.html` is visibly a draft.
- Confirm source labels appear below every chart/table block.
- Confirm company/industry modes are portrait and Top Pick is landscape.
- Confirm no generated artifact claims final PDF/PPTX release approval.
- Confirm `sources/reference/` and `sources/baseline/` have not been modified.

## 8. User Confirmation Needed Before Coding

1. Dependency policy  
   Recommended: approve `pydantic`, `PyYAML`, `jinja2`, `pytest`, and `ruff` for the MVP. If dependency minimization is preferred, implement dataclasses plus `PyYAML` and `pytest` only, and postpone `pydantic`, `jinja2`, `typer`, and `ruff`.

2. First fixture entity  
   Recommended: use synthetic `DEFENSE_FIXTURE_CO` data for the first end-to-end skeleton, then add Hanwha Aerospace only after live OpenDART/source evidence is configured.

3. Live OpenDART timing  
   Recommended: keep live OpenDART disabled in MVP tests and require `OPENDART_API_KEY` only for a manual smoke command after the mock interface passes.

4. Report mode for first demo run  
   Recommended: generate one `COMPANY_REPORT` fixture first because it exercises financial facts, drivers, claims, and valuation-provenance checks. Then run `INDUSTRY_TOP_PICK` orientation tests with the same data structure.

5. HTML design depth  
   Recommended: implement a minimal GIC navy/orange preview with source labels and overflow-aware blocks now; postpone official PPTX token extraction until the data pipeline and QA lint runner are stable.

## 9. Acceptance Criteria

The MVP is complete only when:

- A source manifest can be loaded and an audit source register can be generated.
- DEFENSE fixture facts produce `normalized_facts.json`.
- The `DEFENSE` lens loads a KPI checklist from `schemas/04_SECTOR_FINANCIAL_LENSES.yaml`.
- Facts produce driver maps with falsifiers and financial transmission fields.
- Driver maps and claims produce `report_plan.json`.
- HTML preview renders from the report plan and remains draft-labeled.
- QA lint report uses `PASS`, `FAIL`, and `WARNING` gate values.
- At least five calculation/data-consistency tests run.
- No reference or baseline source is overwritten.
- No final PDF/PPTX is marked release-ready before QA approval.

## 10. Execution Handoff

After user confirmation, execute this plan task-by-task. Preferred execution mode is subagent-driven development for isolated tasks, followed by review of each task's tests and artifacts before moving on.
