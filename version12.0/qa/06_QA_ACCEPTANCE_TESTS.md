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
