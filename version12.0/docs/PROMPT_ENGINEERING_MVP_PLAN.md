# GIC v12 DEFENSE Prompt-Engineering MVP Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans only if this plan is later converted into implementation tasks. This plan itself is a no-code operating plan.

**Goal:** Build a copy-paste prompt system that lets a human analyst use ChatGPT, Claude Chat, or Gemini to transform public financial/industry evidence into a GIC v12 research report plan for the DEFENSE sector.

**Architecture:** Keep the system as a prompt chain, not a software application. Each prompt produces a durable intermediate artifact: request spec, source register, normalized facts, sector KPI checklist, driver map, assumptions, claim-evidence matrix, report plan, draft narrative, and QA report.

**Tech Stack:** No code required. Use Markdown, YAML, JSON, CSV tables, and copy-paste prompts. Optional later automation may use OpenDART API, HTML rendering, or scripts, but that is outside the prompt-first MVP.

---

## 1. Direct Answer: Is Coding Required?

For the recommended prompt-engineering MVP: **no coding is required.**

Coding appeared in the previous plan because the repository handoff documents describe a future Codex/Claude Code automation MVP with loaders, validators, HTML preview, and QA lint runner. That is useful later, but it is not required if the actual product is a prompt system for ChatGPT, Claude Chat, Gemini, or similar interfaces.

The practical recommendation is:

1. First build and test a no-code prompt pack.
2. Use manual or downloaded public-source data as inputs.
3. Require the model to output structured artifacts before prose.
4. Add optional HTML rendering or OpenDART automation only after the prompt chain proves the analysis quality.

## 2. API Key Handling

The OpenDART API key supplied by the user must not be written into prompts, specs, docs, or committed files.

Recommended handling:

- No-code MVP: do not use the API key. Use manually downloaded DART/OpenDART tables, screenshots, CSV exports, or pasted facts with source labels.
- Optional automation later: store the key outside documents as an environment variable named `OPENDART_API_KEY`.
- Never paste the key into ChatGPT, Claude Chat, Gemini, a report, or a public repository.
- If the key has already been exposed in a shared transcript, consider regenerating it before production use.

## 3. MVP Deliverables

Create and use:

- `prompts/08_NO_CODE_PROMPT_PACK.md`  
  Copy-paste prompts for all GIC v12 analysis agents.

- Analyst work artifacts, created manually during each report run:
  - `request.yaml`
  - `source_register.md`
  - `normalized_facts.json`
  - `sector_kpi_checklist.md`
  - `driver_map.yaml`
  - `assumptions.md`
  - `claim_evidence_matrix.md`
  - `report_plan.json`
  - `research_thesis.md`
  - `qa_report.md`

No `src/`, no tests folder, no package setup, and no automated loader are required for this MVP.

## 4. Recommended Operating Workflow

### Stage 1: Request Router

Input:

- Report mode: `COMPANY_REPORT`, `INDUSTRY_REPORT`, or `INDUSTRY_TOP_PICK`
- Sector: `DEFENSE`
- Target company or candidate universe
- As-of date
- Available public sources
- Desired output: report outline, full draft, PPT outline, HTML-ready structure, or QA only

Output:

- `request.yaml`
- Missing input list
- Orientation rule:
  - `COMPANY_REPORT`: portrait
  - `INDUSTRY_REPORT`: portrait
  - `INDUSTRY_TOP_PICK`: landscape

### Stage 2: Source Curator

Input:

- Public source files or pasted source summaries
- URLs or file names
- Publication date and as-of date

Output:

- `source_register.md`
- Source tier classification
- List of claims that cannot be made because T1/T2 evidence is missing

Rules:

- `deep-research-report.md` is methodology only.
- GIC PDF/PPTX templates are design references only.
- News cannot be the sole source for material financial claims.

### Stage 3: Data Normalizer

Input:

- Source register
- Pasted financial tables or manually extracted facts
- DART/OpenDART values if available

Output:

- `normalized_facts.json`

Rules:

- Do not mix actuals, guidance, analyst estimates, and assumptions.
- Do not mix CFS/OFS in one comparison table.
- Do not mix quarterly and cumulative values without a warning.

### Stage 4: DEFENSE Sector Lens

Required DEFENSE KPIs:

- 수주잔고
- 신규 수출계약 및 파이프라인
- 수출 비중/제품 믹스
- 생산능력과 납기
- 영업이익률 및 현금전환
- 환율/승인/현지화 조건

Output:

- `sector_kpi_checklist.md`
- Missing-data warnings

### Stage 5: Driver Modeler

Input:

- `normalized_facts.json`
- DEFENSE KPI checklist

Output:

- `driver_map.yaml`
- `assumptions.md`

Required driver structure:

- observed facts
- mechanism
- revenue transmission
- margin transmission
- cash-flow/balance-sheet transmission
- valuation implication
- timing lag
- falsifiers

### Stage 6: Claim-Evidence Matrix

Input:

- facts
- assumptions
- drivers
- draft claims

Output:

- `claim_evidence_matrix.md`

Every material claim must include:

- `claim_id`
- `claim_text`
- `claim_type`
- `fact_ids`
- `assumption_ids`
- `driver_ids`
- `falsifier_ids`
- `confidence`
- `citation_text`

### Stage 7: Report Planner

Input:

- claim-evidence matrix
- report/design contract
- selected report mode

Output:

- `report_plan.json`

The model must plan pages/slides before writing full prose.

### Stage 8: Research Writer

Input:

- report plan
- claim-evidence matrix
- driver map

Output:

- `research_thesis.md`

Each core paragraph must follow:

```text
Fact -> Mechanism -> Financial Impact -> Judgment -> Falsifier
```

### Stage 9: Auditor

Input:

- all artifacts above

Output:

- `qa_report.md`

Release rule:

- If any gate fails, the result is a draft.
- Final PDF/PPTX language is prohibited unless QA gates pass.

## 5. Practical First Run

Recommended first run:

- Sector: `DEFENSE`
- Mode: `COMPANY_REPORT`
- Entity: start with one company selected by the analyst
- Data method: paste manually extracted DART/OpenDART and company IR facts
- Output: report plan plus thesis draft, not final PPTX

Why this first:

- It verifies whether the prompt chain can preserve evidence links and financial-driver logic.
- It avoids premature automation.
- It allows comparison across ChatGPT, Claude Chat, and Gemini using the same inputs.

## 6. When Coding Becomes Useful Later

Coding becomes useful only if the workflow repeatedly needs:

- automatic OpenDART table fetching
- repeated source-register generation
- JSON schema validation
- HTML preview generation
- QA lint automation
- batch production across many companies

Until then, coding is optional and not part of the prompt-engineering MVP.

## 7. Acceptance Criteria

The no-code MVP is accepted when:

- A user can copy one master prompt and one stage prompt into ChatGPT, Claude Chat, or Gemini.
- The model produces structured artifacts before prose.
- `DEFENSE` KPIs appear in the driver map.
- No material claim lacks evidence linkage.
- Missing evidence is marked `N/A` or `additional source required`.
- The report mode and orientation rules are preserved.
- The final draft is not labeled release-ready unless QA gates pass.

