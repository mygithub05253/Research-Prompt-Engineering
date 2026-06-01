# GIC v13 Local Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-first automation system where non-subscribing GIC members can use only an OpenDART API Key to collect financial data, generate an HTML research preview, and run QA lint checks.

**Architecture:** Python local CLI/UI collects OpenDART data, normalizes it into canonical artifacts, runs deterministic calculations and rule-based DEFENSE driver modeling, renders static HTML, and writes QA lint reports. No paid LLM or paid financial API is required.

**Tech Stack:** Python 3.11+, `requests`, `pydantic`, `PyYAML`, `jinja2`, `pytest`, optional `beautifulsoup4` for document XML parsing. Browser-only HTML preview; no paid SaaS dependency.

---

## 1. Planned Files for Future Coding

Create:

- `pyproject.toml`
- `src/gic_v13/__init__.py`
- `src/gic_v13/cli.py`
- `src/gic_v13/config.py`
- `src/gic_v13/opendart/client.py`
- `src/gic_v13/opendart/corp_codes.py`
- `src/gic_v13/opendart/financials.py`
- `src/gic_v13/opendart/disclosures.py`
- `src/gic_v13/normalize/facts.py`
- `src/gic_v13/model/calculations.py`
- `src/gic_v13/model/defense_lens.py`
- `src/gic_v13/model/drivers.py`
- `src/gic_v13/report/report_plan.py`
- `src/gic_v13/render/html.py`
- `src/gic_v13/qa/lint.py`
- `src/gic_v13/server/app.py`
- `templates/html/report.html.j2`
- `tests/fixtures/opendart/*.json`
- `tests/test_*.py`

Keep design docs:

- `README.md`
- `specs/00_GIC_v13_LOCAL_AUTOMATION_MASTER_SPEC.md`
- `specs/01_OPENDART_DATA_CONTRACT.md`
- `specs/02_HTML_RENDERING_AND_QA_CONTRACT.md`
- `schemas/03_V13_RUN_AND_ARTIFACT_SCHEMA.yaml`
- `docs/API_KEY_AND_SETUP_GUIDE.md`
- `docs/MEMBER_WORKFLOW.md`
- `qa/04_QA_LINT_RULES.md`

## 2. Task Breakdown

### Task 1: Project Skeleton

- [ ] Add package metadata and CLI entry point.
- [ ] Add import smoke test.
- [ ] Add example request loading.

### Task 2: OpenDART Client

- [ ] Implement API key loading from runtime input or `OPENDART_API_KEY`.
- [ ] Implement request wrapper with status/message handling.
- [ ] Add raw response cache.
- [ ] Test error statuses with fixtures.

### Task 3: Corp Code Resolver

- [ ] Download and parse `corpCode.xml` zip.
- [ ] Resolve by corp name and stock code.
- [ ] Cache corp code map.
- [ ] Test ambiguous company names.

### Task 4: Financial Collectors

- [ ] Implement `fnlttSinglAcntAll` collector.
- [ ] Implement `fnlttSinglIndx` collector.
- [ ] Preserve endpoint metadata.
- [ ] Test report code and fs_div handling.

### Task 5: Normalization

- [ ] Convert OpenDART records to canonical facts.
- [ ] Preserve period type, source locator, currency, CFS/OFS.
- [ ] Add unavailable/conflicted handling.

### Task 6: Calculations

- [ ] Implement OPM, YoY, FCF, net debt.
- [ ] Add period compatibility checks.
- [ ] Add CFS/OFS contamination checks.

### Task 7: DEFENSE Lens and Drivers

- [ ] Encode DEFENSE KPI checklist.
- [ ] Generate driver map from verified facts and KPI statuses.
- [ ] Mark missing defense KPIs as warning/fail conditions.

### Task 8: Report Plan and HTML

- [ ] Generate report plan JSON.
- [ ] Render static HTML.
- [ ] Include source labels and QA draft banner.
- [ ] Verify orientation for mode.

### Task 9: QA Lint

- [ ] Implement G1-G6 gates.
- [ ] Emit `qa_report.md` and `qa_report.json`.
- [ ] Keep `release_approved` false unless all gates and human review pass.

### Task 10: Member Packaging

- [ ] Add `setup_windows.ps1`.
- [ ] Add `run_v13.bat`.
- [ ] Add `README_QUICKSTART.md`.
- [ ] Ensure no key is logged or written to outputs.

## 3. Test Plan

- Unit tests for API wrapper, corp code resolver, normalization, calculations, driver generation, HTML rendering, QA lint.
- Fixture tests with recorded OpenDART-like payloads.
- No live API required for CI.
- Manual smoke test with a real key only after fixture tests pass.

## 4. User Confirmation Needed Before Coding

- Whether to build CLI first or local browser UI first.
- Whether to keep dependencies minimal or optimize developer speed.
- Whether the first sample company should be Hanwha Aerospace or a synthetic fixture.
- Whether PDF export helper is required in v13 MVP or can remain manual browser print.

