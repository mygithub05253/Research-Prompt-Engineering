

---

<!-- SOURCE FILE: README.md -->

# GIC v12 Financial Research System — Handoff Pack

## 문서의 목적

이 패키지는 GIC 리서치 프롬프트 엔지니어링 프로젝트를 **재무 데이터 모델링 기반 리서치 생성 시스템**으로 발전시키기 위한 구현 준비 문서이다. 현재 단계의 목표는 코드 완성이 아니라, ChatGPT에서 합의된 분석·데이터·보고서·디자인·QA 규격을 고정하여 이후 Codex 또는 Claude Code가 구현 작업을 시작해도 핵심 품질 기준이 손상되지 않도록 하는 것이다.

## 확정된 사용자 요구사항

1. 기업 리서치 리포트와 산업 리서치 리포트는 제공된 `GIC 리서치 리포트 양식 ver2`의 **디자인 정체성만 유지**한다. 내부 목차·페이지별 논리·지표는 보고서 목적에 맞게 변경할 수 있다.
2. 산업 Top Pick은 별도 공식 양식은 없으며, **가로형 PDF/PPTX** 제출을 원칙으로 한다. 단, GIC의 디자인 정체성은 계승한다.
3. `deep-research-report.md`는 이후 모든 발전 작업에서 **방법론 소스**로 상시 참조한다.
4. v12의 중심은 단순 문장·슬라이드 생성이 아니라 **산업별 KPI → 재무 드라이버 → 실적 전망 → 가치평가 → 리포트 해석**의 흐름이다.
5. 최종 구현은 나중에 Codex/Claude Code로 넘길 수 있으나, 분석 품질·근거성·디자인 규칙은 먼저 문서로 고정한다.

## 읽는 순서

| 순서 | 파일 | 용도 |
|---:|---|---|
| 1 | `specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md` | 프로젝트 전체 설계와 의사결정 기준 |
| 2 | `specs/01_SOURCE_AND_EVIDENCE_POLICY.md` | 출처·인용·데이터 추적 규칙 |
| 3 | `schemas/02_CANONICAL_DATA_SCHEMA.yaml` | 구현 가능한 데이터 모델 스키마 |
| 4 | `specs/03_REPORT_AND_DESIGN_CONTRACTS.md` | 세 가지 리포트 모드와 디자인 규격 |
| 5 | `schemas/04_SECTOR_FINANCIAL_LENSES.yaml` | 산업별 KPI·드라이버·밸류에이션 렌즈 |
| 6 | `prompts/05_PROMPT_ORCHESTRATION_SPEC.md` | LLM 프롬프트 체인 및 출력 계약 |
| 7 | `qa/06_QA_ACCEPTANCE_TESTS.md` | 내용·수치·디자인·렌더링 검수 기준 |
| 8 | `prompts/07_HANDOFF_PROMPT_CODEX_CLAUDE.md` | 구현 에이전트에게 그대로 전달할 착수 지시문 |
| 9 | `AGENTS.md` / `CLAUDE.md` | Codex/Claude Code 프로젝트 상시 규칙 |

## 포함된 기준 자료

### 필수 참조 자료
- `sources/reference/GIC 리서치 리포트 양식 ver2 (2).pdf`
- `sources/reference/GIC 리서치 리포트 양식 ver2 (2).pptx`
- `sources/reference/deep-research-report.md`

### 회귀 테스트용 기존 결과물
- `sources/baseline/한화에어로스페이스_GIC_3기_이동원.pptx`
- `sources/baseline/한화에어로스페이스_GIC_Weekly_Report_v1 (1).html`

기존 결과물은 디자인을 그대로 복제하기 위한 기준이 아니라, v12에서 **경영·경제·금융 해석력, 데이터 추적성, 렌더링 완성도**가 실제로 개선되었는지를 비교하는 회귀 테스트 자료로 사용한다.

## 실행 단계의 원칙

- ChatGPT 단계: 분석 규칙 고정, 프롬프트 설계, 실제 샘플 리포트 검증.
- Codex/Claude Code 단계: 데이터 전처리, 모델 계산, 렌더러, 자동 QA를 코드화.
- 구현 중 어떤 편의 기능도 `출처 추적`, `가정 명시`, `반증 조건`, `디자인 QA`를 생략하게 해서는 안 된다.

## 참고한 공개 1차 자료

- 금융감독원 OpenDART 개발가이드: XBRL 기반 재무제표 및 재무지표 API.
- IFRS Foundation: Digital Financial Reporting 및 XBRL 기반 구조화 비교 가능성.
- Microsoft MarkItDown: LLM/텍스트 분석용 Markdown 전처리 도구.
- Docling: 문서 구조·표·멀티포맷 변환 문서 처리 도구.
- PptxGenJS 공식 문서: 객체 기반 PPTX와 Slide Master, Asian font 지원.
- Marp CLI 공식 저장소: Markdown 기반 HTML/PDF/PPTX 변환과 editable PPTX 제한.
- OpenAI Codex 공식 문서: 프로젝트 지침 파일 `AGENTS.md`.
- Anthropic Claude Code 공식 문서: 프로젝트 지침 파일 `CLAUDE.md` 및 `AGENTS.md` import.


---

<!-- SOURCE FILE: specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md -->

# GIC v12 Financial Research System — Master Specification

- 문서 상태: Implementation-Ready Blueprint
- 버전: v12.0 draft-1
- 목적: ChatGPT에서 품질 규칙을 확정하고, 이후 Codex/Claude Code 구현에 손실 없이 인계
- 프로젝트 성격: 프롬프트 엔지니어링 + 재무 데이터 모델링 + 리서치 문서 렌더링

---

## 1. 프로젝트 재정의

### 1.1 기존 프로젝트의 한계

v11까지의 결과물은 수치 시각화와 프롬프트의 정돈 상태는 양호하나, 다음 네 가지 한계를 가진다.

1. 숫자가 왜 중요한지 설명하는 **경제적 메커니즘**이 부족하다.
2. 산업 성장과 기업 투자 판단이 서술상 혼재할 수 있다.
3. PPTX/PDF 생성이 분석과 분리되지 않아 출력 품질과 분석 품질을 동시에 안정화하기 어렵다.
4. 산업별로 달라야 하는 KPI와 가치평가 논리가 공통 문장 규칙에 묻힐 위험이 있다.

### 1.2 v12의 목표 정의

> GIC v12는 산업별 핵심 변수를 구조화하고, 이 변수가 기업의 매출·마진·현금흐름·가치평가에 미치는 경로를 모델링한 뒤, 그 결과를 GIC 디자인 체계의 리서치 리포트와 Top Pick 발표자료로 변환하는 AI 기반 재무 리서치 시스템이다.

### 1.3 핵심 성공 기준

| 영역 | v12 성공 기준 |
|---|---|
| 근거성 | 핵심 주장마다 원천 자료, 기준 시점, 단위, 데이터 상태가 추적된다. |
| 모델링 | 산업 KPI가 실적·현금흐름·밸류에이션과 연결된다. |
| 설명력 | 수치 → 메커니즘 → 재무 영향 → 판단 → 반증 조건이 문장에 드러난다. |
| 보고서 적합성 | 기업/산업/Top Pick 세 모드를 분리하고 목적에 맞는 구조를 사용한다. |
| 디자인 | 기업·산업은 세로형 GIC 디자인, Top Pick은 가로형 GIC 디자인을 유지한다. |
| 기술 인계성 | Codex/Claude Code가 스키마와 acceptance test를 읽고 구현을 시작할 수 있다. |

---

## 2. 확정된 비즈니스 규칙

### 2.1 산출물 모드

| 모드 | 주된 질문 | 기본 출력 | 디자인 방향 |
|---|---|---|---|
| `COMPANY_REPORT` | 이 기업의 투자 가설은 무엇이며 재무적으로 검증 가능한가? | 세로형 PDF/PPTX | 공식 양식의 브랜드·구성 밀도 계승 |
| `INDUSTRY_REPORT` | 이 산업의 가치 풀이 커지는가, 누구에게 이익이 이동하는가? | 세로형 PDF/PPTX | 공식 양식 디자인만 계승, 항목 자유 재구성 |
| `INDUSTRY_TOP_PICK` | 같은 산업 내에서 어느 기업이 상대적으로 우월한가? | 가로형 PDF/PPTX | 신규 16:9 양식, GIC 브랜드 계승 |

### 2.2 디자인과 콘텐츠의 분리

- 공식 양식은 **콘텐츠 고정 템플릿이 아니라 디자인 시스템 레퍼런스**이다.
- 세로형 보고서에서 `BUY`, `목표주가`, `밸류에이션`은 기업 리포트에는 사용 가능하나 산업 리포트에는 강제하지 않는다.
- 산업 리포트는 `산업 매력도`, `핵심 드라이버`, `시장 구조`, `수혜군`, `리스크·모니터링 KPI` 중심으로 새로 구성한다.
- Top Pick은 가로형 비교 발표물로 별도 설계하되, 네이비/오렌지 계열의 시각적 정체성, 표·차트·출처 표기 문법을 공유한다.

### 2.3 방법론 소스의 역할

`deep-research-report.md`는 매 리포트의 사실 근거가 아니라 **항상 적용되는 작성·렌더링·QA 방법론**이다. 개별 보고서의 결론은 공시, IR, XBRL 재무자료, 정부/기관 산업통계 등 원천 자료에 의존해야 한다.

---

## 3. 전체 시스템 구조

```text
USER REQUEST
  - mode, sector, company/candidate universe, as_of_date, output format
  - source documents and optional template assets
        │
        ▼
[0] REQUEST ROUTER
  - COMPANY_REPORT / INDUSTRY_REPORT / INDUSTRY_TOP_PICK 판정
  - 필요한 sector lens 및 필수 입력 목록 결정
        │
        ▼
[1] SOURCE INGESTION & REGISTRY
  - 공시/IR/통계/보고서/CSV/PDF/PPTX/HTML 수집
  - source_id, 발행일, 기준일, 자료종류, 신뢰등급 기록
        │
        ▼
[2] DOCUMENT NORMALIZATION
  - 분석 자료: Markdown + table JSON + metadata로 정규화
  - 디자인 자료: 원본 보존 + design tokens 추출
  - 수치 단위, 연결/별도, 실제/추정, FY/Q 표준화
        │
        ▼
[3] FINANCIAL FACT STORE
  - historical financials
  - industry KPIs
  - market/valuation metrics
  - claim-evidence links
        │
        ▼
[4] SECTOR DRIVER MODEL
  - 산업별 KPI → 매출/마진/현금흐름/멀티플 연결 경로
  - 주요 가정과 반증 지표 생성
        │
        ▼
[5] FORECAST / COMPARISON / VALUATION
  - 기업: Base/Bull/Bear 전망 및 가치평가
  - 산업: 시장/수익 풀/수혜군 시나리오
  - Top Pick: 동일 KPI 기반 상대평가와 최종 선정
        │
        ▼
[6] RESEARCH WRITER
  - 사실 → 메커니즘 → 재무 영향 → 판단 → 반증 조건 서술
  - 모든 결론에 evidence id 연결
        │
        ▼
[7] REPORT PLANNER & DESIGN RENDERER
  - portrait/company, portrait/industry, landscape/top-pick
  - charts/tables/source labels/layout schema 생성
  - HTML preview, PDF, PPTX 산출
        │
        ▼
[8] AUDIT & QA GATE
  - 계산, 출처, 논리, 디자인, 한글/영문 렌더링, 넘침 검수
  - gate 통과 전 final 산출물 표시 금지
```

---

## 4. 구현 우선순위: MVP에서 확장까지

### Phase 0 — 지금 ChatGPT에서 확정할 것

목표는 코드가 아니라 **분석 규격 고정**이다.

| 작업 | 결과물 | 완료 기준 |
|---|---|---|
| 공통 원칙 고정 | 본 Master Spec | 보고서 모드·모델링·디자인 규칙이 모순 없이 정의됨 |
| Source policy 고정 | `01_SOURCE_AND_EVIDENCE_POLICY.md` | 주장의 증거 등급과 인용 규칙 정의 |
| 데이터 스키마 고정 | `02_CANONICAL_DATA_SCHEMA.yaml` | 구현자가 데이터 객체를 그대로 만들 수 있음 |
| 산업 렌즈 초안 | `04_SECTOR_FINANCIAL_LENSES.yaml` | 동아리 섹터 전부에 KPI·모델·리스크 존재 |
| 프롬프트 체인 | `05_PROMPT_ORCHESTRATION_SPEC.md` | 각 에이전트 입력/출력/실패 조건 정의 |
| QA 기준 | `06_QA_ACCEPTANCE_TESTS.md` | 샘플 결과를 pass/fail로 판정 가능 |

### Phase 1 — ChatGPT 샘플 검증

- 대상: 기존 한화에어로스페이스 결과물을 v12 기준으로 재작성 또는 검토.
- 목적: 모델링 문체와 보고서 설계가 실제 한 건에서 작동하는지 확인.
- 산출: `source_register`, `fact_table`, `driver_map`, `report_outline`, `qa_report`.
- 중요한 원칙: 이 단계에서는 자동화보다 분석의 정합성을 우선한다.

### Phase 2 — Codex/Claude Code MVP 구현

- 목표: 입력 파일과 정형 데이터에서 표준 중간 산출물 생성.
- 최소 기능:
  1. 파일 수집 및 manifest 생성
  2. Markdown/JSON 정규화
  3. OpenDART 기반 재무 facts 수집 모듈 골격
  4. 수동 입력 KPI CSV validator
  5. report plan JSON 생성
  6. HTML preview 및 최소 PDF/PPTX renderer prototype
  7. QA lint report

### Phase 3 — 재무모델·렌더러 고도화

- 전망/밸류에이션 계산 모듈
- 산업별 렌즈 주입
- PPTX master 기반 객체 렌더링
- PDF 렌더링·폰트 검수 자동화
- 샘플 회귀 테스트 체계

---

## 5. 입력과 소스 설계

### 5.1 소스 분류

| Source Tier | 설명 | 사용 가능 범위 | 예시 |
|---|---|---|---|
| T1 | 공식 원천·규제 공시·감사된 보고 | 핵심 수치와 주요 사실의 1차 근거 | DART 사업보고서, OpenDART XBRL, 기업 IR 실적자료 |
| T2 | 공식 산업·정책·협회·통계 | 산업 추세와 거시 가정의 주 근거 | 산업부, 통계청, 전력거래소, 협회 자료 |
| T3 | 신뢰 가능한 해설·리서치 | 맥락, 컨센서스 비교, 논점 보완 | 증권사 리포트, 신뢰도 높은 리서치 기관 |
| T4 | 뉴스·검색 결과 | 이벤트 탐지 또는 추가 확인용 | 기사, 일반 웹 문서 |
| M | 방법론·디자인 자료 | 결론 근거가 아닌 작성/출력 규칙 | GIC 양식, deep-research-report.md |

### 5.2 핵심 주장에 필요한 최소 증거

- 과거 재무 숫자: T1 필수.
- 회사가 제시한 가이던스/수주/제품 계획: T1 또는 기업 공식 자료 필수, 회사 주장임을 명시.
- 산업 규모·정책·수요 전망: T2 우선, T3 보조.
- 미래 실적 예측: 실제 사실처럼 인용하지 않으며, 근거 facts와 가정 ids를 모두 제시.
- Top Pick 최종 선택: 후보 전부에 대해 동일 기준·동일 기간·동일 단위 데이터가 존재해야 함.

### 5.3 OpenDART 활용 원칙

한국 상장사 재무 모델링의 정형 데이터 기반은 OpenDART로 둔다.

- `fnlttSinglAcntAll`: 단일회사 전체 재무제표, 연결/별도 구분과 주요 재무제표 계정 수집.
- `fnlttSinglIndx`: 수익성·안정성·성장성·활동성 재무지표 수집.
- XBRL 원문: 계정 매핑 검증 또는 세부 계정이 필요한 경우 수집.
- 반드시 저장할 메타데이터: `corp_code`, `bsns_year`, `reprt_code`, `fs_div`, `rcept_no`, `currency`, `retrieved_at`.
- 정정 공시 가능성을 고려하여 모든 보고서에는 `as_of_date`와 조회 시점을 기록한다.

---

## 6. 금융 데이터 모델의 핵심 객체

### 6.1 사실(Fact)과 가정(Assumption)의 엄격한 분리

| 객체 | 정의 | 예시 |
|---|---|---|
| `fact` | 출처에서 직접 확인 가능한 수치/문장 | 2025년 연결 매출액, 수주잔고, 정책 발표일 |
| `derived_metric` | facts로 계산한 값 | YoY 증가율, 영업이익률, 순차입금/EBITDA |
| `assumption` | 전망을 위해 설정한 조건 | 수출 믹스 증가, ASP 변화, 할인율 |
| `forecast` | facts와 assumptions로 산출한 예상 값 | FY2027 매출, OPM, EPS |
| `judgment` | 모델 결과를 투자/산업 결론으로 해석 | Top Pick 선정, 산업 매력도 상향 |
| `falsifier` | 판단이 틀렸음을 보여줄 모니터링 지표 | 납기 지연, 재고 확대, NIM 하락 |

### 6.2 공통 재무 모델 구조

| 구간 | 기본 항목 | 비고 |
|---|---|---|
| Historical | 매출, 영업이익, EBITDA, 순이익, CFO, CAPEX, FCF, 순차입금, 자본 | 최소 3개년; 가능 시 분기 추가 |
| Profitability | GPM, OPM, EBITDA margin, ROE, ROIC | 산업별 선택적 강조 |
| Growth | 매출/이익 CAGR, YoY/QoQ | 실제와 추정 분리 |
| Balance Sheet | 현금, 차입금, 순차입금, 부채비율, 자본비율 | 금융업 별도 구조 적용 |
| Valuation | PER, PBR, EV/EBITDA, DCF inputs, dividend yield | 산업별 적합성 판정 필요 |
| Sector KPI | 산업 렌즈가 지정 | 수주잔고, HBM 비중, CET1 등 |

### 6.3 산업 변수의 재무 연결 체계

모든 핵심 드라이버는 다음 형식으로 표현한다.

```yaml
driver_id: DEFENSE_EXPORT_BACKLOG
driver_name: 수출 수주잔고 확대
observed_facts:
  - fact_id: F001
mechanism: "수주잔고가 확보되면 미래 매출 인식 가시성이 개선되며, 생산능력과 납기가 충족될 때 실제 인도가 매출로 전환된다."
financial_transmission:
  revenue: "인도 물량 및 매출 인식 일정에 따라 증가"
  margin: "수출 제품 믹스와 생산 레버리지에 따라 개선 가능"
  cash_flow: "선수금·운전자본 조건에 따라 시차 발생"
  valuation: "이익 가시성 상승 시 적용 멀티플 재평가 가능"
falsifiers:
  - "수출 승인 지연"
  - "생산능력 병목 또는 납기 지연"
  - "고마진 믹스 효과를 상쇄하는 원가 상승"
```

---

## 7. 모델링과 가치평가 규칙

### 7.1 예측 모델의 기본 원칙

- 예측은 2~3개 연도 또는 필요한 기간만 작성하며, 장기 전망은 가정 불확실성을 명시한다.
- Base/Bull/Bear 세 시나리오를 기본으로 하되, 산업 리포트는 수치 예측보다 드라이버 시나리오 중심으로 작성할 수 있다.
- 과거 실적 평균을 기계적으로 연장하지 않는다. 산업 KPI와 연결된 가정을 반드시 사용한다.
- 예측 테이블의 모든 행은 `assumption_id` 또는 `driver_id`와 연결되어야 한다.
- 기업의 공시 가이던스와 작성자의 가정을 명시적으로 분리한다.

### 7.2 밸류에이션 선택 규칙

| 기업/산업 특성 | 우선 모델 | 보조 모델 | 주의사항 |
|---|---|---|---|
| 제조·방산·조선·전력기기 | PER / EV/EBITDA / DCF | PBR, FCF yield | 수주와 실적 인식 시차 반영 |
| 금융 | PBR-ROE / 배당·주주환원 | PER | EV/EBITDA·일반 FCFF는 부적합할 수 있음 |
| 반도체 | Forward PER / EV/EBITDA / cycle-normalized multiples | DCF | 사이클과 재고 정상화 가정 필요 |
| 바이오 초기·적자 | rNPV / milestone-based scenario | peer EV/pipeline | 임상 성공 확률·현금 runway 중심 |
| 고성장 로봇/AI 초기 | scenario revenue multiple / unit economics | DCF는 제한적 | 상용화·현금소진 불확실성 강조 |
| 소비재/콘텐츠 | PER / EV/EBITDA / DCF | 브랜드/사용자 KPI 비교 | 흥행 지속성·마케팅비 반영 |

### 7.3 Top Pick의 비교 원칙

- 산업마다 KPI가 달라도, 동일 산업의 후보 기업에는 동일 KPI 정의·기간·단위·계산법을 적용한다.
- 단순 점수 합산만으로 결론을 내리지 않는다. 점수표는 비교를 돕는 도구이며, `valuation-adjusted thesis`와 `falsifier`를 별도로 서술한다.
- 데이터 미확보 항목은 임의 추정하지 않고 `N/A — 공개 확인 불가`로 표시한다.
- 좋은 기업과 좋은 투자 대상을 구분한다: 우위가 이미 높은 밸류에이션에 반영되었는지 검토한다.

---

## 8. 보고서 서술 규칙

### 8.1 핵심 문단의 의무 구조

모든 핵심 슬라이드/페이지의 결론은 다음 다섯 요소를 포함해야 한다.

1. **Fact**: 확인된 숫자 또는 사건.
2. **Mechanism**: 산업·사업 구조상 의미.
3. **Financial Impact**: 매출, 마진, 현금흐름, 밸류에이션 중 영향 경로.
4. **Judgment**: 투자 또는 산업 결론.
5. **Falsifier**: 해석이 틀릴 수 있는 조건과 모니터링 지표.

### 8.2 금지되는 서술

- “긍정적이다”, “성장이 기대된다”처럼 메커니즘 없는 추상 결론.
- 실제 수치와 전망 수치를 혼합한 표.
- 회사 IR의 주장과 작성자의 판단을 구분하지 않는 문장.
- 수치 없이 Top Pick 선정.
- 산업 구조 설명 없이 특정 기업으로 바로 결론 점프.
- 출처, 기간, 단위가 없는 차트.

### 8.3 좋은 리서치 문장의 형식

```text
[Fact] FY2025 수주잔고가 전년 대비 X% 증가했다.
[Mechanism] 이는 향후 매출 인식의 가시성을 높이는 선행지표이며, 생산 병목이 없다면 인도 증가로 이어질 수 있다.
[Financial Impact] 고마진 수출 제품의 매출 비중이 확대될 경우 영업이익률과 영업현금흐름의 개선 폭은 매출 성장률을 상회할 수 있다.
[Judgment] 따라서 핵심 가정이 유지되는 한 이익 추정치 상향과 밸류에이션 재평가 여지가 있다.
[Falsifier] 다만 승인·납기 지연 또는 원가 급등은 이익 전환 속도를 낮추는 반증 변수다.
```

---

## 9. 디자인·렌더링 전략

### 9.1 중간표현 원칙

- 분석 본문: Markdown.
- 표·차트·layout·source tag·page plan: JSON/YAML schema.
- 최종 결과물: HTML preview, PDF, PPTX.
- 공식 PPTX/PDF는 디자인 추출·검수의 기준 원본으로 보존한다; Markdown 변환본으로 대체하지 않는다.

### 9.2 권장 구현 분기

| 용도 | 권장 경로 | 이유 |
|---|---|---|
| 분석 자료 전처리 | MarkItDown / 필요 시 Docling | LLM 분석용 구조화 Markdown 생성 |
| 공식 양식 기반 정교한 PPTX | PptxGenJS 객체 기반 렌더링 | 텍스트/표/차트/shape/master 제어와 편집성 |
| Top Pick 빠른 가로형 초안·preview | Marp 또는 HTML preview | 빠른 반복과 검토 |
| 최종 제출 PDF | 검증된 렌더 파이프라인에서 산출 | 폰트·레이아웃 고정 검수 필요 |

### 9.3 렌더링의 필수 QA

- 한글/영문/숫자/%, 통화, 괄호, `EV/EBITDA` 표기가 깨지지 않는다.
- 표 영역과 페이지 경계를 넘는 객체가 없다.
- 출처와 기준일이 모든 핵심 차트·표에 보인다.
- 텍스트가 이미지로만 고정된 PPTX는 “편집 가능 결과물”로 표시하지 않는다.
- 폰트가 사용 환경에 없을 수 있으므로, 구현 단계에서는 제공 가능한 CJK 호환 폰트 fallback과 PDF 렌더 스모크 테스트를 반드시 만든다.

---

## 10. 최종 산출물 묶음

개별 리포트 실행 시 아래 파일 세트를 생성한다.

```text
outputs/<run_id>/
├─ audit/
│  ├─ source_register.md
│  ├─ evidence_matrix.csv
│  ├─ model_assumptions.md
│  ├─ calculation_checks.md
│  └─ qa_report.md
├─ data/
│  ├─ normalized_facts.json
│  ├─ historical_financials.csv
│  ├─ sector_kpis.csv
│  ├─ forecast_scenarios.csv        # 기업/Top Pick 사용
│  └─ valuation_summary.csv          # 필요한 모드만 사용
├─ narrative/
│  ├─ research_thesis.md
│  └─ report_plan.json
└─ deliverables/
   ├─ preview.html
   ├─ final.pdf
   └─ final.pptx
```

---

## 11. Codex/Claude 인계 시 변경 금지 원칙

구현 에이전트는 아래 항목을 편의상 삭제하거나 약화할 수 없다.

1. facts와 assumptions의 분리.
2. 핵심 주장과 evidence의 연결.
3. 산업별 KPI 렌즈.
4. Base/Bull/Bear 또는 이에 준하는 불확실성 표현.
5. 판단마다 falsifier 작성.
6. 기업/산업/Top Pick 모드 분리.
7. 공식 디자인은 시각 시스템으로 유지하며 산업 콘텐츠를 기업 템플릿에 억지로 맞추지 않는 원칙.
8. 최종 PDF/PPTX 이전 QA gate.

---

## 12. 다음 실제 작업

가장 높은 품질을 위해 다음 작업은 자동화 코드가 아니라 **샘플 1건의 v12 모델링 산출물 작성**으로 시작한다.

### 권장 샘플
- 기존 자료가 존재하는 한화에어로스페이스 기업 리포트 또는 방산 Top Pick.

### 샘플에서 작성할 내부 파일
1. `source_register.md`
2. `historical_financials.csv`
3. `sector_kpis.csv`
4. `driver_map.yaml`
5. `assumptions.md`
6. `report_outline.md`
7. `qa_report.md`

이 1건이 만족스러울 때, 그 형태를 Codex/Claude가 자동으로 재생성하도록 구현한다. 자동화가 분석 설계보다 먼저 진행되면, 잘못된 분석 흐름을 빠르게 반복하는 결과가 된다.


---

<!-- SOURCE FILE: specs/01_SOURCE_AND_EVIDENCE_POLICY.md -->

# GIC v12 — Source and Evidence Policy

## 1. 목적

본 문서는 리포트가 “좋아 보이는 설명”이 아니라 **재현 가능한 근거 기반 분석**이 되도록 소스·증거·가정·출처 표기를 표준화한다.

## 2. 소스 역할 구분

| 분류 | 역할 | 결론의 직접 근거 가능 여부 | 포함 예시 |
|---|---|---:|---|
| `METHOD` | 방법론·품질 규칙 | 불가 | `deep-research-report.md` |
| `DESIGN` | 디자인·출력 기준 | 불가 | GIC 양식 PDF/PPTX |
| `PRIMARY_FINANCIAL` | 공식 재무·공시 | 가능 | OpenDART XBRL, 사업보고서, 분·반기 보고서 |
| `PRIMARY_COMPANY` | 기업 공식 비재무/IR | 가능, 회사 주장임을 표시 | IR deck, 수주 공시, 보도자료 |
| `PRIMARY_INDUSTRY` | 공식 산업·정책·통계 | 가능 | 정부·공공기관·협회 자료 |
| `SECONDARY_RESEARCH` | 비교·맥락 보완 | 보조 근거 | 증권사·리서치 기관 |
| `NEWS` | 이벤트 탐지 | 단독 핵심 근거 금지 | 언론 보도 |

## 3. Source Register 필수 필드

| 필드 | 설명 |
|---|---|
| `source_id` | 문서 고유 ID |
| `source_type` | 위 분류 중 하나 |
| `title` | 문서명 |
| `publisher` | 발행 주체 |
| `published_date` | 발행일 |
| `as_of_date` | 자료가 설명하는 기준일 |
| `retrieved_at` | 수집일시 |
| `url_or_file` | 원본 위치 또는 파일 경로 |
| `coverage` | 이 자료에서 가져온 항목 |
| `reliability_note` | 정정공시 여부, 기업 주장 여부, 한계 |

## 4. Fact Register 규칙

모든 숫자는 아래 필드를 가져야 한다.

| 필드 | 필수 여부 | 예시 |
|---|---:|---|
| `fact_id` | 필수 | `F_FIN_REV_2025_CFS` |
| `metric_name` | 필수 | 매출액 |
| `entity` | 필수 | 한화에어로스페이스 |
| `period` | 필수 | `FY2025` |
| `period_type` | 필수 | FY / Q / YTD / Point-in-time |
| `amount` | 필수 | `123456` |
| `unit` | 필수 | KRW million |
| `currency` | 필요 시 | KRW |
| `fs_div` | 재무수치 필수 | CFS / OFS |
| `actual_or_estimate` | 필수 | actual / company_guidance / analyst_estimate |
| `source_id` | 필수 | `S_DART_001` |
| `source_locator` | 필수 | API field, 페이지, 표명 |
| `validation_status` | 필수 | verified / pending / conflicted |

## 5. Evidence Matrix

모든 핵심 슬라이드 또는 페이지는 다음 표의 한 행 이상과 연결되어야 한다.

| claim_id | 결론 문장 | fact_ids | assumption_ids | source_tier | falsifier | 사용 위치 |
|---|---|---|---|---|---|---|
| C001 | 수출 수주 확대가 실적 가시성을 높인다 | F001, F002 | A001 | T1/T2 | 납기 지연 | 회사 리포트 p.5 |

## 6. 인용과 문장 표시 원칙

- 실제 발생한 과거 수치는 “~했다”, “~로 집계되었다”로 표기한다.
- 회사가 제시한 목표나 계획은 “회사 가이던스/회사 발표에 따르면”으로 표기한다.
- 작성자의 전망은 “당사/본 분석의 Base case에서는”, “가정 시”로 표기한다.
- 데이터가 충돌하면 어느 숫자를 채택했는지와 이유를 기록한다.
- 단위와 기간을 변경해 비교할 때 변환 규칙을 기록한다.
- 산업 전망 수치가 제3자 전망이면 출처와 산정 범위를 명시한다.

## 7. OpenDART 기반 기본 데이터 원칙

- 한국 기업의 기본 재무 facts는 가능한 경우 OpenDART의 XBRL 기반 데이터를 우선 사용한다.
- 연결재무제표(`CFS`)와 별도재무제표(`OFS`)를 혼용하지 않는다.
- 분·반기 손익의 당기 금액과 누적 금액을 구분한다.
- API 조회값은 정정 제출로 변경될 수 있으므로 `retrieved_at`을 반드시 기록한다.
- DART 데이터가 없는 sector KPI는 기업 IR 또는 공식 통계로 채우되 `source_type`을 구분한다.

## 8. 출처 부족 처리

| 상황 | 처리 방식 |
|---|---|
| 핵심 KPI 공개 없음 | `N/A — 공개자료에서 확인 불가` 표기, 추정 금지 |
| 출처 간 수치 상충 | `conflicted` 플래그 후 보고서 결론에 사용 금지 또는 차이를 설명 |
| 기업 주장만 존재 | 사실이 아니라 company disclosure로 라벨링 |
| 전망 근거 부족 | 결론 강도를 낮추고 추가 데이터 필요 목록 출력 |


---

<!-- SOURCE FILE: schemas/02_CANONICAL_DATA_SCHEMA.yaml -->

project:
  name: GIC_v12_financial_research_system
  version: "12.0-draft-1"
  required_report_modes:
    - COMPANY_REPORT
    - INDUSTRY_REPORT
    - INDUSTRY_TOP_PICK

request:
  request_id: string
  report_mode: enum[COMPANY_REPORT, INDUSTRY_REPORT, INDUSTRY_TOP_PICK]
  as_of_date: date
  sector_id: string
  primary_entity: string|null
  candidate_entities: [string]
  output_formats: [html, pdf, pptx]
  page_orientation: enum[portrait, landscape]
  language: ko-KR

source_register:
  - source_id: string
    source_type: enum[METHOD, DESIGN, PRIMARY_FINANCIAL, PRIMARY_COMPANY, PRIMARY_INDUSTRY, SECONDARY_RESEARCH, NEWS]
    title: string
    publisher: string
    published_date: date|null
    as_of_date: date|null
    retrieved_at: datetime
    local_path_or_uri: string
    coverage: [string]
    reliability_note: string

financial_fact:
  - fact_id: string
    entity: string
    metric_group: enum[income_statement, balance_sheet, cash_flow, valuation, share_data, sector_kpi, market_data]
    metric_name: string
    period: string
    period_type: enum[FY, Q, YTD, LTM, spot, range]
    value: number|null
    value_text: string|null
    unit: string
    currency: string|null
    fs_div: enum[CFS, OFS, NA]
    actual_or_estimate: enum[actual, company_guidance, analyst_estimate, derived]
    source_id: string
    source_locator: string
    validation_status: enum[verified, pending, conflicted, unavailable]
    notes: string|null

normalized_financials:
  entity: string
  historical_periods: [string]
  forecast_periods: [string]
  metrics:
    revenue: {unit: KRW_million, facts: [string]}
    operating_income: {unit: KRW_million, facts: [string]}
    net_income_attributable: {unit: KRW_million, facts: [string]}
    depreciation_amortization: {unit: KRW_million, facts: [string]}
    operating_cash_flow: {unit: KRW_million, facts: [string]}
    capex: {unit: KRW_million, facts: [string]}
    free_cash_flow: {formula: "operating_cash_flow - capex", derived_from: [string]}
    cash: {unit: KRW_million, facts: [string]}
    total_debt: {unit: KRW_million, facts: [string]}
    net_debt: {formula: "total_debt - cash", derived_from: [string]}
    equity: {unit: KRW_million, facts: [string]}
    op_margin: {formula: "operating_income / revenue", derived_from: [string]}
    roe: {formula_or_source: string, derived_from: [string]}

sector_kpi:
  - kpi_id: string
    sector_id: string
    entity: string|null
    kpi_name: string
    definition: string
    value: number|null
    unit: string
    period: string
    source_id: string
    financial_link: [revenue, margin, cash_flow, balance_sheet, valuation]
    missing_data_policy: enum[required, acceptable_na, proxy_allowed]

assumption:
  - assumption_id: string
    scope: enum[company, industry, top_pick]
    driver_id: string
    description: string
    scenario: enum[base, bull, bear]
    value_or_direction: string
    basis_fact_ids: [string]
    sensitivity: enum[high, medium, low]
    rationale: string
    falsifier_ids: [string]

financial_driver:
  - driver_id: string
    sector_id: string
    name: string
    description: string
    input_fact_ids: [string]
    input_kpi_ids: [string]
    transmission:
      revenue: string|null
      margin: string|null
      cash_flow: string|null
      balance_sheet: string|null
      valuation: string|null
    lag_or_timing: string|null
    falsifiers: [string]

forecast:
  entity: string
  scenario: enum[base, bull, bear]
  periods: [string]
  metrics:
    - metric_name: string
      values: [number|null]
      unit: string
      formula_or_method: string
      assumption_ids: [string]
      confidence: enum[high, medium, low]

valuation:
  entity: string
  selected_methods: [string]
  method_selection_rationale: string
  inputs:
    - input_name: string
      value: number|null
      unit: string
      source_or_assumption_id: string
  outputs:
    - method: string
      implied_value: number|null
      implied_price: number|null
      scenario: enum[base, bull, bear]
  sensitivity_tables: [string]
  caveats: [string]

claim_evidence_matrix:
  - claim_id: string
    report_section: string
    claim_text: string
    claim_type: enum[fact, mechanism, financial_impact, judgment, risk]
    fact_ids: [string]
    assumption_ids: [string]
    driver_ids: [string]
    falsifier_ids: [string]
    confidence: enum[high, medium, low]
    citation_text: string

report_plan:
  mode: enum[COMPANY_REPORT, INDUSTRY_REPORT, INDUSTRY_TOP_PICK]
  design_system: GIC_NAVY_ORANGE
  orientation: enum[portrait, landscape]
  pages_or_slides:
    - index: integer
      section: string
      objective: string
      title: string
      key_claim_ids: [string]
      charts:
        - chart_id: string
          chart_type: string
          fact_or_forecast_ids: [string]
          unit: string
          source_label: string
      tables: [string]
      narrative_blocks: [string]
      visual_qa_notes: [string]

qa_report:
  run_id: string
  gates:
    factual_traceability: enum[PASS, FAIL, WARNING]
    calculation_integrity: enum[PASS, FAIL, WARNING]
    scenario_transparency: enum[PASS, FAIL, WARNING]
    narrative_quality: enum[PASS, FAIL, WARNING]
    design_compliance: enum[PASS, FAIL, WARNING]
    render_integrity: enum[PASS, FAIL, WARNING]
  fatal_errors: [string]
  warnings: [string]
  recommended_fixes: [string]
  release_approved: boolean


---

<!-- SOURCE FILE: specs/03_REPORT_AND_DESIGN_CONTRACTS.md -->

# GIC v12 — Report and Design Contracts

## 1. 공통 디자인 시스템 계약

### 1.1 고정되는 시각 언어

공식 양식은 내부 항목을 고정하지 않으며, 다음 시각 요소의 레퍼런스로 사용한다.

- 네이비 중심의 신뢰도 높은 리서치 톤과 오렌지 포인트 강조.
- 상단/표지의 GIC 브랜드 표현과 정돈된 리서치 보고서 분위기.
- 섹션 제목, 본문, 표, 차트, 출처 각주의 위계.
- 표/차트 영역과 서술 영역을 명확히 분리하는 정보 밀도.
- Compliance Notice 및 출처 표기 습관.

### 1.2 구현 시 추출할 Design Tokens

PPTX 원본을 구현 단계에서 분석해 아래 파일로 고정한다.

```yaml
design_tokens:
  colors:
    primary_navy: "TBD_FROM_TEMPLATE"
    accent_orange: "TBD_FROM_TEMPLATE"
    secondary_blue: "TBD_FROM_TEMPLATE"
    background: "TBD_FROM_TEMPLATE"
    text_primary: "TBD_FROM_TEMPLATE"
  typography:
    korean_primary: "EXTRACT_OR_SET_FALLBACK"
    latin_primary: "EXTRACT_OR_SET_FALLBACK"
    title_sizes: "TBD"
    body_sizes: "TBD"
    source_sizes: "TBD"
  layout:
    portrait_size: "match official template"
    landscape_size: "16:9"
    footer_rule: "TBD"
    source_location: "bottom of visual block"
```

폰트는 원본 이름을 추출해 기록하되, 실행 환경에서 존재하지 않는 경우 CJK 호환 fallback을 고정하고 PDF 렌더 후 줄바꿈을 검수한다.

## 2. COMPANY_REPORT 계약 — 세로형

### 2.1 목적

개별 기업의 투자 가설을 산업 환경, 경쟁력, 실적 전망, 가치평가, 반증 조건까지 연결하여 제시한다.

### 2.2 권장 9페이지 구성

| Page | 제목 유형 | 반드시 답해야 하는 질문 | 필수 모델 산출물 |
|---:|---|---|---|
| 1 | Investment Summary | 왜 지금 이 회사를 보는가? | 목표 판단, 핵심 thesis 3개, 핵심 실적/valuation 표 |
| 2 | Contents & Thesis Map | 보고서의 논리 흐름은 무엇인가? | 핵심 driver map 요약 |
| 3 | Industry Context | 산업 환경이 기업에 어떤 기회를 제공하는가? | 산업 KPI와 company exposure |
| 4 | Business & Competitive Position | 기업이 수익을 확보할 구조적 이유는 무엇인가? | segment/BM/경쟁우위 |
| 5 | Investment Point 1 | 가장 큰 실적 드라이버는 무엇인가? | fact → driver → forecast |
| 6 | Investment Point 2/3 | 추가 upside의 조건은 무엇인가? | KPI·민감도·시나리오 |
| 7 | Risks & Falsifiers | 어떤 지표가 thesis를 깨는가? | risk map와 monitoring KPI |
| 8 | Forecast & Valuation | 판단이 숫자로 정당화되는가? | 추정 실적, valuation, 민감도 |
| 9 | Appendix & Compliance | 출처와 책임 범위가 명확한가? | sources, caveats, notice |

### 2.3 필수 규칙

- 투자의견/목표가를 제시한다면 valuation output과 연결한다.
- 목표가를 제시하지 않는 학습형 리포트 모드도 허용하되, 그 경우 “투자 가설 평가”로 표기한다.
- 투자포인트는 최소 한 개의 실적 드라이버와 반증 조건을 포함한다.

## 3. INDUSTRY_REPORT 계약 — 세로형

### 3.1 목적

특정 기업 추천 이전에 산업 자체의 구조적 성장성, 가치사슬, 수익 풀 이동, 리스크와 관찰 KPI를 설명한다.

### 3.2 권장 9페이지 구성

| Page | 제목 유형 | 핵심 질문 | 필수 시각화/모델 |
|---:|---|---|---|
| 1 | Industry View | 왜 이 산업을 지금 봐야 하는가? | 매력도/전망 요약, 성장 드라이버 3개 |
| 2 | Executive Summary | 결론과 핵심 논거는 무엇인가? | thesis map |
| 3 | Market Definition & Value Chain | 산업의 범위와 수익 발생 지점은 어디인가? | value-chain map |
| 4 | Market Size & Demand | 시장은 얼마나, 왜 성장하는가? | 시장/수요 지표 시계열 |
| 5 | Growth Driver 1 | 구조적 수요 드라이버는 무엇인가? | driver transmission |
| 6 | Supply / Technology / Competition | 누가 이익을 가져가는가? | capacity/competition/profit pool |
| 7 | Policy & Macro Variables | 거시·규제는 성장에 어떤 영향을 미치는가? | policy/FX/rate/supply indicators |
| 8 | Risks & Falsifiers | 산업 논리가 깨지는 조건은 무엇인가? | bear case와 monitoring KPI |
| 9 | Beneficiary Map & Conclusion | 이후 Top Pick 분석에서 무엇을 비교해야 하는가? | 수혜군/피해군, 핵심 KPI 리스트 |

### 3.3 금지 규칙

- 산업 전체 분석에서 특정 기업의 목표가를 결론처럼 사용하지 않는다.
- 시장 성장률만으로 산업 매력도를 선언하지 않는다; 마진·경쟁·CAPEX·규제 구조를 함께 분석한다.

## 4. INDUSTRY_TOP_PICK 계약 — 가로형 16:9

### 4.1 목적

같은 산업 내 후보 기업을 산업별 KPI와 가치평가 기준으로 상대 비교해 최종 선호 기업을 선택한다.

### 4.2 권장 8슬라이드 구성

| Slide | 제목 유형 | 목적 | 필수 요소 |
|---:|---|---|---|
| 1 | Sector Top Pick | 결론을 첫 장에 제시 | Top Pick, 핵심 이유 1문장, 주요 KPI 하이라이트 |
| 2 | Sector Backdrop | 비교가 필요한 산업 배경 설명 | 모멘텀·cycle·정책 지표 |
| 3 | Selection Framework | 어떤 기준으로 비교했는가 | KPI 정의, 가중치가 있다면 근거 |
| 4 | Candidate Scorecard | 동일 기준 비교 | 수치 비교표, N/A 표시 규칙 |
| 5 | Winner’s Edge | 1위의 구조적 우위 | 드라이버-재무 연결 |
| 6 | Earnings & Valuation | 좋은 기업이 좋은 가격인가 | 실적 전망/멀티플/상대평가 |
| 7 | Risks & Scenario | 순위가 바뀔 조건은 무엇인가 | bull/base/bear 또는 sensitivity |
| 8 | Final Call & Monitorables | 무엇을 모니터링할 것인가 | 결론, KPI watchlist, 출처 |

### 4.3 비교표 원칙

- 비교 대상 전부에 동일한 KPI 정의를 사용한다.
- 동일 기간과 동일 단위가 확보되지 않으면 비교 셀에 경고를 표시한다.
- 정성 평가를 점수화할 경우 scoring rubric을 별도 노출한다.
- 점수 1위가 곧 Top Pick이 아닐 수 있다. valuation·리스크·반증 조건을 결론에 포함한다.

## 5. 차트·표·출처 계약

| 항목 | 규칙 |
|---|---|
| 차트 제목 | 단순 항목명이 아니라 관점을 담은 문장형 제목 사용 |
| 축/단위 | 통화, 기간, 단위, actual/estimate 구분 표시 |
| 표 | 비교기간, 연결/별도, 예측 여부 표기 |
| 출처 | 시각화 블록 하단에 발행자·자료명·기준일 표기 |
| 예측 | 실제값과 다른 색/패턴 또는 `(E)` 표시 |
| 위험 | 결론 페이지뿐 아니라 해당 주장 근처에 falsifier 표기 |


---

<!-- SOURCE FILE: schemas/04_SECTOR_FINANCIAL_LENSES.yaml -->

sectors:
  INFRA_BATTERY:
    label: "인프라 - 2차전지"
    thesis_question: "출하 성장과 가동률 회복이 CAPEX 및 재무부담을 상쇄하며 현금흐름 개선으로 이어지는가?"
    required_kpis:
      - {name: "출하량/판매량", financial_link: revenue, status: required}
      - {name: "ASP 및 제품 믹스", financial_link: [revenue, margin], status: required}
      - {name: "가동률/수율", financial_link: margin, status: required}
      - {name: "고객사 다변화", financial_link: [revenue, valuation], status: required}
      - {name: "CAPEX 및 순차입금", financial_link: [cash_flow, balance_sheet], status: required}
      - {name: "핵심 원재료 가격", financial_link: margin, status: required}
    valuation_methods: ["EV/EBITDA", "Forward PER", "DCF"]
    falsifiers: ["가동률 회복 지연", "고객사 발주 축소", "CAPEX 대비 현금창출 부진", "원재료·판매가 스프레드 악화"]

  INFRA_POWER_ENERGY:
    label: "인프라 - 전력/에너지"
    thesis_question: "전력수요와 송배전·발전 투자 확대가 수주와 프로젝트 마진으로 전환되는가?"
    required_kpis:
      - {name: "수주잔고와 신규수주", financial_link: revenue, status: required}
      - {name: "수주잔고/매출 배수", financial_link: valuation, status: required}
      - {name: "프로젝트/제품 믹스", financial_link: margin, status: required}
      - {name: "납기 및 생산능력", financial_link: [revenue, margin], status: required}
      - {name: "운전자본과 현금전환", financial_link: cash_flow, status: required}
    valuation_methods: ["EV/EBITDA", "PER", "DCF"]
    falsifiers: ["송배전 투자 지연", "수주 후 원가 상승", "납기 병목", "현금전환 악화"]

  FINANCIALS:
    label: "금융"
    thesis_question: "수익성과 자본여력이 대손 리스크를 흡수하고 주주환원으로 이어지는가?"
    required_kpis:
      - {name: "NIM", financial_link: revenue, status: required}
      - {name: "대출성장률", financial_link: revenue, status: required}
      - {name: "대손비용률/연체율", financial_link: margin, status: required}
      - {name: "CET1 또는 자본적정성", financial_link: [balance_sheet, valuation], status: required}
      - {name: "ROE", financial_link: valuation, status: required}
      - {name: "배당/자사주/주주환원", financial_link: valuation, status: required}
    valuation_methods: ["PBR-ROE", "PER", "Dividend/Capital Return Framework"]
    avoid_methods: ["일반 기업형 EV/EBITDA 중심 평가"]
    falsifiers: ["건전성 악화", "CET1 하락", "NIM 급락", "환원정책 후퇴"]

  SEMICONDUCTOR:
    label: "반도체"
    thesis_question: "제품 믹스와 수요 사이클 개선이 ASP·가동률·마진을 동시에 개선하는가?"
    required_kpis:
      - {name: "HBM/고부가 제품 비중 또는 기술 인증", financial_link: [revenue, margin], status: required}
      - {name: "출하량/bit growth", financial_link: revenue, status: required}
      - {name: "ASP", financial_link: [revenue, margin], status: required}
      - {name: "재고일수/재고 정상화", financial_link: [margin, cash_flow], status: required}
      - {name: "가동률 및 CAPEX", financial_link: [margin, cash_flow], status: required}
    valuation_methods: ["Cycle-normalized PER", "EV/EBITDA", "DCF"]
    falsifiers: ["인증 지연", "ASP 하락", "재고 재확대", "CAPEX 과잉"]

  ROBOTICS_PHYSICAL_AI:
    label: "로봇/피지컬 AI"
    thesis_question: "기술 시연이 반복 가능한 상용 매출과 단위경제성으로 변환되는가?"
    required_kpis:
      - {name: "유료 고객/도입 건수", financial_link: revenue, status: required}
      - {name: "반복매출 또는 서비스 매출 비중", financial_link: valuation, status: required}
      - {name: "제품/프로젝트 gross margin", financial_link: margin, status: required}
      - {name: "R&D 및 현금소진", financial_link: cash_flow, status: required}
      - {name: "양산·통합 파트너십", financial_link: revenue, status: acceptable_na}
    valuation_methods: ["Scenario revenue multiple", "Unit economics", "Milestone-adjusted DCF"]
    falsifiers: ["상용 고객 전환 실패", "현금 runway 단축", "양산 원가 악화", "기술 대체"]

  SHIPBUILDING:
    label: "조선"
    thesis_question: "고선가·친환경 선종 수주가 인도 시점의 마진과 현금흐름으로 실현되는가?"
    required_kpis:
      - {name: "수주잔고/매출 배수", financial_link: revenue, status: required}
      - {name: "신조선가/수주선가", financial_link: margin, status: required}
      - {name: "LNG·친환경선 비중", financial_link: [revenue, margin], status: required}
      - {name: "후판가 및 원가", financial_link: margin, status: required}
      - {name: "인도 일정 및 현금흐름", financial_link: cash_flow, status: required}
    valuation_methods: ["Forward PER", "PBR/ROE", "EV/EBITDA"]
    falsifiers: ["후판가 상승", "인도 지연", "선가 하락", "발주 cycle 둔화"]

  DEFENSE:
    label: "방산"
    thesis_question: "국방비와 수출 파이프라인이 계약·인도·고마진 매출로 이어지는가?"
    required_kpis:
      - {name: "수주잔고", financial_link: revenue, status: required}
      - {name: "신규 수출계약 및 파이프라인", financial_link: revenue, status: required}
      - {name: "수출 비중/제품 믹스", financial_link: margin, status: required}
      - {name: "생산능력과 납기", financial_link: [revenue, margin], status: required}
      - {name: "영업이익률 및 현금전환", financial_link: [margin, cash_flow], status: required}
      - {name: "환율/승인/현지화 조건", financial_link: [margin, risk], status: required}
    valuation_methods: ["Forward PER", "EV/EBITDA", "DCF"]
    falsifiers: ["수출승인 지연", "납기·생산병목", "원가상승", "지정학 완화 또는 조달정책 변화"]

  CONSUMER_GAME_ENTERTAINMENT:
    label: "소비재/게임/엔터"
    thesis_question: "브랜드·IP·사용자 기반이 글로벌 매출과 지속 가능한 마진으로 연결되는가?"
    required_kpis:
      - {name: "글로벌 매출 비중", financial_link: revenue, status: required}
      - {name: "신제품/IP/콘텐츠 라인업", financial_link: revenue, status: required}
      - {name: "MAU/ARPU/객단가/팬덤 지표", financial_link: revenue, status: proxy_allowed}
      - {name: "마케팅비 및 영업이익률", financial_link: margin, status: required}
      - {name: "현금창출 및 주주환원", financial_link: valuation, status: acceptable_na}
    valuation_methods: ["PER", "EV/EBITDA", "DCF"]
    falsifiers: ["흥행 실패", "사용자 이탈", "마케팅 효율 악화", "글로벌 확장 둔화"]

  BIO:
    label: "바이오"
    thesis_question: "임상·허가·기술이전 이벤트의 확률가중 가치가 자금소진 리스크를 상회하는가?"
    required_kpis:
      - {name: "파이프라인 단계/임상 이벤트", financial_link: valuation, status: required}
      - {name: "허가·데이터 공개 일정", financial_link: valuation, status: required}
      - {name: "기술이전 계약 및 마일스톤", financial_link: [revenue, cash_flow], status: acceptable_na}
      - {name: "현금 및 cash runway", financial_link: cash_flow, status: required}
      - {name: "R&D 지출", financial_link: cash_flow, status: required}
    valuation_methods: ["rNPV", "Milestone scenario valuation", "Cash runway analysis"]
    avoid_methods: ["이익이 없는 초기 바이오에 단순 PER 적용"]
    falsifiers: ["임상 실패", "허가 지연", "기술이전 무산", "증자/희석 리스크"]


---

<!-- SOURCE FILE: prompts/05_PROMPT_ORCHESTRATION_SPEC.md -->

# GIC v12 — Prompt Orchestration Specification

## 1. 원칙

v12는 하나의 거대한 프롬프트가 아니라, 각 단계가 명시적 입력과 구조화 출력을 갖는 prompt chain이다. 에이전트는 prose를 먼저 쓰지 말고 facts·assumptions·drivers·claims를 먼저 작성해야 한다.

## 2. Orchestration Flow

| Step | Agent/Prompt | 입력 | 출력 | 실패 시 행동 |
|---:|---|---|---|---|
| 0 | `REQUEST_ROUTER` | 사용자 요청, 제공 파일 | `request.yaml`, missing inputs | 모드/섹터 불명확 시 최소 질문 |
| 1 | `SOURCE_CURATOR` | request, files/web data | `source_register.md` | T1/T2 부족 시 결론 보류 |
| 2 | `DATA_NORMALIZER` | 원천 문서/CSV/API | `normalized_facts.json`, tables | 단위·기간 혼란 시 conflict flag |
| 3 | `SECTOR_MODEL_SELECTOR` | sector_id | sector lens, KPI checklist | 없는 sector는 신규 lens 요구 |
| 4 | `DRIVER_MODELER` | facts, KPI lens | `driver_map.yaml`, assumptions | 메커니즘이 증거 없이 점프하면 reject |
| 5 | `FORECAST_VALUATION_ANALYST` | facts, drivers, assumptions | scenario/valuation files | 자료 부족이면 정성 결론으로 downgrade |
| 6 | `RESEARCH_WRITER` | claims/evidence/model | `research_thesis.md` | 근거 없는 문장 삭제 |
| 7 | `REPORT_PLANNER` | thesis, design contract | `report_plan.json` | 내용 과밀 시 페이지 배치 재설계 |
| 8 | `RENDERER` | report plan, tokens | HTML/PDF/PPTX | 렌더 오류 QA로 전달 |
| 9 | `AUDITOR` | 모든 산출물 | `qa_report.md` | FAIL이면 final 배포 차단 |

## 3. 공통 시스템 지시문

```text
당신은 GIC v12 Financial Research System의 분석 에이전트다.
목표는 장식적인 보고서를 쓰는 것이 아니라, 공개 근거와 재무 드라이버를 연결해 검증 가능한 리서치 산출물을 만드는 것이다.

절대 규칙:
1. 사실(fact), 계산(derived metric), 가정(assumption), 전망(forecast), 판단(judgment)을 섞지 않는다.
2. 모든 핵심 판단은 fact_id, driver_id, assumption_id, falsifier와 연결한다.
3. 데이터가 없으면 추정하거나 일반론으로 메우지 말고 N/A 또는 추가 필요 자료로 남긴다.
4. 산업별 KPI와 적합한 가치평가 방법을 사용한다.
5. 보고서 문장은 fact → mechanism → financial impact → judgment → falsifier 구조를 따른다.
6. 디자인 규격은 내용 논리를 억지로 바꾸는 제약이 아니라 최종 표시 규칙이다.
```

## 4. REQUEST_ROUTER prompt

```text
입력된 요청과 파일 목록을 읽고 아래만 출력하라.

판정 대상:
- report_mode: COMPANY_REPORT / INDUSTRY_REPORT / INDUSTRY_TOP_PICK
- sector_id: 지정 섹터 코드
- entities: 대상 기업 또는 비교 후보
- as_of_date: 분석 기준일
- output_format: html/pdf/pptx
- orientation: portrait 또는 landscape
- required_source_gaps: 분석 전 추가 확보가 필요한 자료

판정 규칙:
- 개별 기업 투자 가설·목표가·valuation 중심이면 COMPANY_REPORT.
- 산업 구조·발전 가능성·수혜군 중심이면 INDUSTRY_REPORT.
- 동일 산업 기업을 비교하여 최종 선정하면 INDUSTRY_TOP_PICK.
- INDUSTRY_TOP_PICK은 항상 landscape.
- COMPANY_REPORT/INDUSTRY_REPORT은 GIC 공식 세로형 디자인을 기본으로 한다.
```

## 5. SOURCE_CURATOR prompt

```text
주어진 요청에 대해 필요한 소스를 수집·평가하라.
핵심 숫자에는 공식 공시 또는 공식 통계를 우선한다.
방법론 문서와 디자인 템플릿은 사실 근거로 사용하지 않는다.

출력:
1. source_register 표
2. 필수인데 누락된 소스 목록
3. 결론 도출 가능 범위와 도출 불가 범위
4. 정정/기준일/연결·별도/추정치 위험 경고
```

## 6. DATA_NORMALIZER prompt

```text
원천 자료에서 facts를 추출하라. 문장을 작성하지 말고 데이터 구조만 출력하라.

각 숫자에 필수로 기록할 것:
- entity, metric, period, unit, currency
- actual/company_guidance/analyst_estimate/derived 구분
- 연결(CFS)/별도(OFS)/해당 없음(NA)
- source_id와 locator
- 검증 상태

규칙:
- 단위를 임의로 합치지 말고 변환 로그를 남긴다.
- 누적 손익과 분기 손익을 혼동하지 않는다.
- 동종 비교 시 기준이 다르면 conflict를 기록한다.
```

## 7. DRIVER_MODELER prompt

```text
sector lens와 facts를 기반으로 산업 변수의 재무 전달 경로를 작성하라.

각 driver마다 반드시 포함:
- observed facts
- mechanism
- revenue impact
- margin impact
- cash-flow/balance-sheet impact
- valuation implication
- time lag
- falsifiers

금지:
- '수혜', '긍정적', '성장 기대'만 작성하고 재무 전달 경로를 누락하는 것
- 공개 데이터가 없는 KPI를 임의 점수화하는 것
```

## 8. FORECAST_VALUATION_ANALYST prompt

```text
기업 또는 Top Pick 모드에만 실적 전망과 가치평가를 수행하라.
산업 리포트에서는 산업 시나리오와 수혜군 매핑을 우선하라.

기업/Top Pick 출력:
- historical summary
- Base/Bull/Bear assumptions
- forecast table
- valuation method selection rationale
- sensitivity and downside triggers

가치평가 선택:
- 산업 렌즈의 valuation_methods 및 avoid_methods를 따른다.
- 예측 자료가 부족하면 목표가처럼 보이는 정밀 수치를 생성하지 않는다.
```

## 9. RESEARCH_WRITER prompt

```text
구조화된 facts, drivers, scenarios, valuation 결과만 사용하여 한국어 리서치 문장을 작성하라.

핵심 문단은 아래 순서로 작성한다.
1. Fact: 확인된 수치 또는 사건 1문장
2. Mechanism: 산업/경영 구조상 의미 1~2문장
3. Financial Impact: 매출·마진·현금흐름·valuation 영향 1~2문장
4. Judgment: 투자/산업 판단 1문장
5. Falsifier: 확인해야 할 반증 조건 1문장

문체:
- 경제적 인과를 분명히 한다.
- 회사 발표, 작성자 추정, 실제 실적을 구분한다.
- 과도한 수식어보다 비교 가능하고 검증 가능한 문장을 우선한다.

출력:
- executive thesis
- section narratives
- chart interpretation captions
- risk/falsifier paragraphs
- citation/evidence tags
```

## 10. REPORT_PLANNER prompt

```text
리서치 본문을 선택된 report contract에 맞춰 페이지/슬라이드 plan JSON으로 변환하라.
디자인은 GIC 시각 언어를 따르되, 내부 콘텐츠 구조는 목적에 맞게 배치한다.

각 page/slide 필수 필드:
- objective
- one-sentence takeaway title
- key_claim_ids
- chart/table requirement
- source label
- narrative word budget
- overflow risk note
```

## 11. AUDITOR prompt

```text
보고서를 재작성하지 말고 release 가능 여부를 판단하라.

검사:
A. 사실 추적성: 핵심 결론에 evidence가 존재하는가?
B. 계산 정합성: 합계/변화율/마진/valuation 계산이 맞는가?
C. 예측 투명성: actual과 forecast가 명확히 구분되는가?
D. 리서치 설명력: 수치가 메커니즘과 재무 영향으로 번역되었는가?
E. 모드 적합성: 산업 보고서가 기업 추천문처럼 변질되지 않았는가?
F. 디자인 적합성: GIC 디자인·출처·페이지 규격을 지켰는가?
G. 렌더링 무결성: 폰트 깨짐, 글자 넘침, 표 잘림이 없는가?

출력:
- fatal errors
- warnings
- page/slide level fixes
- release_approved: true/false
```


---

<!-- SOURCE FILE: qa/06_QA_ACCEPTANCE_TESTS.md -->

# GIC v12 — QA Gates and Acceptance Tests

## 1. Release Gate 원칙

최종 PDF/PPTX는 아래 6개 gate 모두 `PASS` 또는 허용된 `WARNING`일 때만 제출 가능하다. `FAIL`이 하나라도 존재하면 deliverable을 “초안”으로만 표시한다.

| Gate | 핵심 질문 | FAIL 조건 |
|---|---|---|
| G1 Evidence | 결론이 근거와 연결되는가? | 핵심 결론에 source/fact 없음 |
| G2 Calculation | 숫자 계산이 정확한가? | 마진·증감률·valuation 오류 |
| G3 Scenario | 예측 가정이 투명한가? | actual/estimate 혼합, 가정 미표기 |
| G4 Research Quality | 경영·경제·금융 해석이 있는가? | 숫자 반복 또는 추상적 긍정 문구만 존재 |
| G5 Mode & Design | 목적과 디자인을 지켰는가? | 산업 보고서를 기업 추천 양식으로 강제; 가로형 규칙 위반 |
| G6 Render | 제출파일이 정상인가? | 폰트 깨짐, 표 잘림, 빈 차트, 출처 누락 |

## 2. 내용 QA Checklist

### 2.1 모든 리포트 공통

- [ ] 기준일(`as_of_date`)이 표지 또는 서두에 있다.
- [ ] 핵심 수치마다 단위와 기간이 있다.
- [ ] 핵심 차트/표마다 출처가 있다.
- [ ] actual, company guidance, analyst estimate가 구분된다.
- [ ] 핵심 판단마다 최소 한 개의 falsifier가 있다.
- [ ] 방법론 자료를 사실 근거처럼 인용하지 않는다.
- [ ] 공개 확인 불가 데이터는 N/A로 남겼다.

### 2.2 COMPANY_REPORT 전용

- [ ] 기업 실적 드라이버가 산업 상황과 연결된다.
- [ ] 전망 수치가 가정표와 연결된다.
- [ ] valuation 방법 선택 이유가 있다.
- [ ] 목표주가/상승여력이 있다면 계산 근거가 있다.
- [ ] 리스크가 실적/valuation에 미치는 경로를 설명한다.

### 2.3 INDUSTRY_REPORT 전용

- [ ] 산업 범위와 가치사슬이 정의되어 있다.
- [ ] 성장률 외에 수익 풀·경쟁·기술·정책 변수가 있다.
- [ ] 특정 기업 결론을 산업 분석보다 앞세우지 않는다.
- [ ] 마지막에 수혜군 또는 Top Pick용 비교 KPI로 연결한다.

### 2.4 INDUSTRY_TOP_PICK 전용

- [ ] 모든 후보 기업이 동일 KPI로 비교된다.
- [ ] 기간·단위·정의가 동일하지 않은 항목을 경고했다.
- [ ] 최종 Pick의 장점뿐 아니라 valuation과 리스크를 다룬다.
- [ ] 가로형 16:9 deliverable이다.

## 3. Calculation Tests

| Test ID | 계산/검증 | 기대 결과 |
|---|---|---|
| CAL-001 | OPM = operating_income / revenue | 입력 facts와 소수점 오차 범위 내 일치 |
| CAL-002 | YoY = current / previous - 1 | periods가 연속이고 단위가 동일할 때만 산출 |
| CAL-003 | FCF = CFO - CAPEX | CAPEX 부호 규칙 명시 |
| CAL-004 | Net Debt = Debt - Cash | 재무/비재무기업 구분 적용 |
| CAL-005 | CFS/OFS contamination check | 같은 표 안에서 혼용 시 FAIL |
| CAL-006 | FY/Q/YTD contamination check | 누적/분기 혼용 시 FAIL |
| VAL-001 | valuation input provenance | 모든 input에 fact 또는 assumption id 존재 |
| VAL-002 | sensitivity consistency | scenario 변화 방향과 implied value 논리 일관 |

## 4. Narrative Tests

| Test ID | 검사 | 통과 기준 |
|---|---|---|
| NAR-001 | 수치 단순 반복 탐지 | 차트 해설에 mechanism과 financial impact가 존재 |
| NAR-002 | 추상 판단 탐지 | “긍정적/우호적” 뒤에 원인과 지표가 존재 |
| NAR-003 | 주장 추적 | conclusion 문장에 claim/evidence link 존재 |
| NAR-004 | 반증 조건 | 최상위 thesis와 각 투자포인트에 falsifier 존재 |
| NAR-005 | 산업/기업 분리 | 산업 보고서의 결론이 산업 구조에 기반 |

## 5. Visual and Rendering Tests

| Test ID | 검사 | 통과 기준 |
|---|---|---|
| VIS-001 | orientation | 기업/산업 portrait, Top Pick landscape |
| VIS-002 | brand tokens | 네이비/오렌지 디자인 시스템 사용 |
| VIS-003 | source labels | 주요 표/차트 하단에 출처 표기 |
| VIS-004 | typography smoke test | 한글·영문·숫자·%·통화·EV/EBITDA 모두 정상 렌더 |
| VIS-005 | overflow | 텍스트/표/차트가 영역 밖으로 넘치지 않음 |
| VIS-006 | editable PPTX claim | 객체 편집 가능한 경우에만 editable로 표기 |
| VIS-007 | PDF rendering | PDF와 PPTX의 핵심 레이아웃 불일치가 없음 |

## 6. 회귀 테스트 전략

### 기준 자료
- 기존 한화에어로스페이스 PPTX/HTML을 baseline으로 저장한다.

### 비교 지표

| 항목 | v11 baseline 관찰 | v12 기대 개선 |
|---|---|---|
| 수치 시각화 | 유지 | 유지 또는 개선 |
| 경제적 메커니즘 | 보완 필요 | 각 핵심 주장에 의무화 |
| 근거 추적 | 제한적 | evidence matrix 제공 |
| 산업 KPI | 범용적 위험 | 방산 lens 적용 |
| 전망/valuation | 설명 구조 보완 | 가정과 민감도 노출 |
| 출력 QA | 폰트/렌더 문제 가능 | smoke test와 release gate 적용 |

## 7. MVP 승인 기준

Codex/Claude 구현 MVP는 아래를 만족하면 1차 승인한다.

- [ ] 소스 manifest를 생성할 수 있다.
- [ ] 샘플 데이터에서 `normalized_facts.json`을 생성한다.
- [ ] sector lens 하나(`DEFENSE`)를 로드해 KPI checklist를 만든다.
- [ ] report plan JSON을 생성한다.
- [ ] 최소 HTML preview가 생성된다.
- [ ] QA report가 `PASS/FAIL/WARNING` 형식으로 출력된다.
- [ ] 계산 및 데이터 정합성 unit test가 최소 5개 실행된다.


---

<!-- SOURCE FILE: prompts/07_HANDOFF_PROMPT_CODEX_CLAUDE.md -->

# GIC v12 — Codex / Claude Code Implementation Handoff Prompt

아래 전체 블록은 구현을 시작할 때 Codex 또는 Claude Code에 그대로 붙여넣을 수 있는 착수 프롬프트다. 구현 에이전트는 반드시 저장소 안의 세부 spec과 schema를 먼저 읽고 작업해야 한다.

---

## Copy-Paste Start Prompt

```text
당신은 `GIC_v12_Financial_Research_System` 저장소의 구현 책임 엔지니어다.
이 프로젝트는 PPT를 빠르게 만드는 도구가 아니라, 공개 자료에 기반한 재무 데이터 모델링 결과를 GIC 리서치 보고서로 변환하는 시스템이다.

반드시 먼저 읽을 파일:
1. README.md
2. specs/00_GIC_v12_FINANCIAL_RESEARCH_MASTER_SPEC.md
3. specs/01_SOURCE_AND_EVIDENCE_POLICY.md
4. schemas/02_CANONICAL_DATA_SCHEMA.yaml
5. specs/03_REPORT_AND_DESIGN_CONTRACTS.md
6. schemas/04_SECTOR_FINANCIAL_LENSES.yaml
7. prompts/05_PROMPT_ORCHESTRATION_SPEC.md
8. qa/06_QA_ACCEPTANCE_TESTS.md
9. AGENTS.md 또는 CLAUDE.md

핵심 비즈니스 규칙:
- 세 가지 report mode를 분리한다: COMPANY_REPORT, INDUSTRY_REPORT, INDUSTRY_TOP_PICK.
- 공식 GIC 양식은 디자인 시스템 기준이며 내부 내용 항목을 강제하지 않는다.
- 기업/산업 리포트는 portrait; Top Pick은 16:9 landscape이다.
- deep-research-report.md는 방법론 소스이지 개별 투자 결론의 사실 근거가 아니다.
- 사실, 파생 계산, 가정, 전망, 판단, 반증 조건은 데이터 구조에서 분리한다.
- 핵심 주장마다 evidence link를 가져야 한다.
- 분석 품질을 낮추면서 구현 편의를 얻는 변경을 하지 않는다.

MVP 목표:
A. 소스 ingest/manifest
B. Markdown/JSON normalization scaffold
C. OpenDART 재무 fact loader 인터페이스와 mock test
D. sector lens loader 및 DEFENSE 예시 실행
E. facts → drivers → report_plan JSON pipeline
F. HTML preview renderer prototype
G. QA lint/acceptance test runner

권장 기술 방향:
- Python: ingestion, OpenDART loader, normalization, modeling, validation.
- YAML/JSON: schema, sector lenses, report plans, evidence links.
- MarkItDown: 일반 오피스/텍스트 자료 Markdown 전처리 후보. 고충실도 최종 문서 변환기로 오인하지 않는다.
- Docling: 복잡한 PDF/표/XBRL 후보; 채택 전 간단한 품질 benchmark를 만든다.
- PptxGenJS: 공식 양식에 가까운 편집 가능한 PPTX renderer 후보.
- Marp: Top Pick 빠른 prototype 또는 preview 후보; editable PPTX를 최종 품질 기준으로 사용하지 않는다.

첫 작업 순서:
1. 저장소 파일 구조를 확인하고 구현 계획을 `docs/IMPLEMENTATION_PLAN.md`로 작성한다. 아직 코드를 대량 변경하지 않는다.
2. `src/`, `tests/`, `outputs/`, `data/` 초기 폴더와 기본 config를 제안한다.
3. YAML schema를 검토해 타입 모델(Pydantic 또는 동등 검증 구조)을 설계한다.
4. `sources/reference/`와 `sources/baseline/` 파일을 건드리지 않고 테스트 fixture로 취급한다.
5. DEFENSE sector를 대상으로 dummy facts를 이용한 end-to-end skeleton을 만든다.
6. acceptance tests 중 MVP 대상 테스트를 실행하고 결과를 보고한다.

반드시 멈추고 사용자 확인을 받을 상황:
- 핵심 데이터 스키마 삭제/대폭 변경
- valuation 방법론 변경
- 공식 디자인 파일 자체를 덮어쓰기
- 외부 유료 API 또는 신규 production dependency 추가
- 근거 추적이나 QA gate를 생략하는 설계 선택

첫 응답 형식:
1. 내가 이해한 프로젝트 목적
2. 현재 파일에서 확인한 고정 규칙
3. 구현 architecture 제안
4. MVP milestone과 테스트 계획
5. 변경할 파일 목록
6. 사용자 확인이 필요한 의사결정
```

---

## Codex용 적용 방식

- 저장소 루트에 `AGENTS.md`를 둔다.
- Codex가 실행되기 전에 이 문서와 spec 파일을 읽도록 작업 지시를 준다.
- 하위 모듈에 특별한 규칙이 생기면 해당 폴더에 더 구체적인 `AGENTS.md` 또는 override를 추가한다.

## Claude Code용 적용 방식

- 저장소 루트에 `CLAUDE.md`를 둔다.
- 중복 관리를 줄이기 위해 `CLAUDE.md`에서 `@AGENTS.md`를 import하도록 구성한다.
- Claude 전용 지시가 있을 때만 `CLAUDE.md`에 추가한다.

## 에이전트 선택 권장

두 도구 중 하나로 시작한다. 같은 브랜치에서 두 도구를 동시에 무계획하게 사용하지 않는다.

- Codex로 시작하기 적합한 경우: ChatGPT와 같은 생태계에서 계획→코드→검수 흐름을 이어가고자 할 때.
- Claude Code로 시작하기 적합한 경우: `CLAUDE.md`, hooks, project memory 기반의 장기 로컬 개발 워크플로우를 이미 사용할 계획일 때.
- 어느 쪽을 선택하든 본 spec, schema, QA gate가 도구보다 우선한다.


---

<!-- SOURCE FILE: AGENTS.md -->

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


---

<!-- SOURCE FILE: CLAUDE.md -->

@AGENTS.md

# Claude Code Additional Notes

- Use plan mode before broad architecture changes.
- Keep working notes concise; write durable decisions into `docs/` rather than relying only on conversational memory.
- Do not overwrite any files in `sources/reference/` or `sources/baseline/`.
