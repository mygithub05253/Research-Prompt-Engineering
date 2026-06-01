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
