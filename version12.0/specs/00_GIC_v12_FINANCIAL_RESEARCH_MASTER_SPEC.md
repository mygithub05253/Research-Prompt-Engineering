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
