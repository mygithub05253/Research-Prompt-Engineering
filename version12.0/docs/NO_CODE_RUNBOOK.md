# GIC v12 No-Code Runbook

이 문서는 GIC v12를 코딩 없이 ChatGPT, Claude Chat, Gemini에서 운영하는 실무 절차다. 목표는 프롬프트 하나로 바로 보고서를 쓰는 것이 아니라, 근거 자료를 구조화한 뒤 리서치 문장과 보고서 계획으로 변환하는 것이다.

---

## 1. 운영 원칙

- 첫 MVP는 `DEFENSE` 섹터에 한정한다.
- OpenDART API key는 문서나 프롬프트에 저장하지 않는다. no-code 운영에서는 사람이 DART/OpenDART에서 확인한 표나 수치를 붙여넣는다.
- 모델에게 바로 "보고서 써줘"라고 하지 않는다. 항상 `source_register -> normalized_facts -> sector_kpi_checklist -> driver_map -> claim_evidence_matrix -> report_plan -> research_thesis -> qa_report` 순서로 진행한다.
- 중간 산출물은 복사해 별도 파일 또는 노트에 저장한다. 다음 단계 프롬프트에는 직전 산출물을 그대로 붙여넣는다.
- QA gate를 통과하지 못하면 산출물은 초안이다.

## 2. 추천 도구 배치

### ChatGPT

- 강점: 구조화 출력, 긴 분석 체인 관리, 표/JSON 초안 생성.
- 추천 역할: master prompt + 전체 체인 1차 실행.

### Claude Chat

- 강점: 긴 문서 독해, narrative 품질, 논리적 일관성 점검.
- 추천 역할: `research_thesis.md`와 `qa_report.md` 교차 검토.

### Gemini

- 강점: Google 생태계 자료와 긴 컨텍스트 검토.
- 추천 역할: 자료 누락, source coverage, 외부 자료 점검.

세 모델을 모두 쓸 때도 원칙은 동일하다. 같은 입력 템플릿과 같은 산출물명을 쓰고 결과를 비교한다.

## 3. 한 번의 리포트 실행 절차

### Step 1: 분석 요청 정리

사용 파일:

- `templates/no_code/request.yaml`
- `prompts/08_NO_CODE_PROMPT_PACK.md`의 `Master System Prompt`
- `prompts/08_NO_CODE_PROMPT_PACK.md`의 `Request Router Prompt`

작업:

1. 대상 기업, 섹터, 기준일, 리포트 모드, 사용 가능한 자료를 적는다.
2. 모델에게 `request.yaml`만 출력하게 한다.
3. 모드와 orientation이 맞는지 확인한다.

완료 기준:

- `report_mode`가 셋 중 하나로 확정됨.
- `sector_id`가 `DEFENSE`임.
- 기준일이 있음.
- 필요한 누락 자료가 표시됨.

### Step 2: 소스 등록

사용 파일:

- `templates/no_code/source_register.md`
- `Source Curator Prompt`

작업:

1. DART/OpenDART, 사업보고서, IR, 정부/기관 통계, 뉴스, 방법론 자료를 구분한다.
2. 각 자료의 발행자, 발행일, 기준일, coverage를 기록한다.
3. 결론의 직접 근거로 쓸 수 없는 자료를 명확히 표시한다.

완료 기준:

- 방법론/디자인 자료가 사실 근거로 분류되지 않음.
- 핵심 재무 수치의 1차 근거가 확인됨.
- 누락된 T1/T2 자료가 보임.

### Step 3: facts 정규화

사용 파일:

- `templates/no_code/normalized_facts.json`
- `Data Normalizer Prompt`

작업:

1. 원천 자료에서 수치와 기간, 단위, source locator를 추출한다.
2. actual, company_guidance, analyst_estimate, derived를 구분한다.
3. 연결/별도, FY/Q/YTD/LTM/spot을 구분한다.

완료 기준:

- 모든 숫자에 `source_id`와 `source_locator`가 있음.
- 출처 없는 숫자는 `unavailable`로 표시됨.
- 실제값과 전망/가정이 섞이지 않음.

### Step 4: DEFENSE KPI 체크

사용 파일:

- `templates/no_code/sector_kpi_checklist.md`
- `DEFENSE Sector Lens Prompt`

작업:

1. 여섯 개 필수 KPI를 모두 점검한다.
2. 공개 확인 불가 항목은 추정하지 않는다.
3. 재무 연결 경로를 revenue, margin, cash_flow, balance_sheet, valuation으로 표시한다.

완료 기준:

- 모든 필수 KPI가 `verified`, `pending`, `conflicted`, `unavailable` 중 하나로 표시됨.
- 누락된 KPI가 다음 단계에서 결론 강도를 낮추는 조건으로 반영됨.

### Step 5: driver map 작성

사용 파일:

- `templates/no_code/driver_map.yaml`
- `templates/no_code/assumptions.md`
- `Driver Modeler Prompt`

작업:

1. 수주잔고, 수출 파이프라인, 수출 믹스, 납기/생산능력, 현금전환, 환율/승인/현지화 리스크를 driver로 만든다.
2. driver마다 fact, mechanism, financial transmission, timing, falsifier를 붙인다.
3. 가정은 사실과 별도 파일에 둔다.

완료 기준:

- driver마다 `input_fact_ids`가 있음.
- 판단이 아니라 재무 전달 경로가 적혀 있음.
- falsifier가 있음.

### Step 6: claim-evidence matrix 작성

사용 파일:

- `templates/no_code/claim_evidence_matrix.md`
- `Claim Evidence Matrix Prompt`

작업:

1. 보고서에서 쓸 핵심 주장을 claim 단위로 분해한다.
2. claim마다 fact, assumption, driver, falsifier link를 붙인다.
3. link가 없는 claim은 삭제하거나 `additional source required`로 낮춘다.

완료 기준:

- 핵심 판단 claim에 falsifier가 있음.
- 사실 claim과 판단 claim이 분리됨.
- citation text가 있음.

### Step 7: report plan 작성

사용 파일:

- `templates/no_code/report_plan.json`
- `Report Planner Prompt`

작업:

1. mode별 페이지/슬라이드 구조를 만든다.
2. 각 page/slide에 objective, title, key_claim_ids, charts, tables, narrative blocks를 배치한다.
3. source label과 overflow risk를 남긴다.

완료 기준:

- `COMPANY_REPORT`와 `INDUSTRY_REPORT`는 portrait.
- `INDUSTRY_TOP_PICK`은 landscape.
- 차트/표마다 source label이 있음.

### Step 8: narrative 작성

사용 파일:

- `templates/no_code/research_thesis.md`
- `Research Writer Prompt`

작업:

1. 구조화 산출물만 사용해 문단을 쓴다.
2. 핵심 문단은 Fact -> Mechanism -> Financial Impact -> Judgment -> Falsifier 순서를 지킨다.
3. 문단 끝에 claim_id와 source_id를 표시한다.

완료 기준:

- 근거 없는 미사여구가 없음.
- 회사 발표와 작성자 판단이 분리됨.
- 반증 조건이 문단에 포함됨.

### Step 9: QA audit

사용 파일:

- `templates/no_code/qa_report.md`
- `Auditor Prompt`

작업:

1. 모델에게 보고서를 고치지 말고 audit만 하게 한다.
2. G1-G6 gate를 PASS/FAIL/WARNING으로 표시한다.
3. FAIL이 있으면 release_approved를 false로 둔다.

완료 기준:

- fatal error가 명시됨.
- recommended fixes가 있음.
- QA 통과 전 최종본 표현을 쓰지 않음.

## 4. 첫 실험 권장 설정

```yaml
report_mode: COMPANY_REPORT
sector_id: DEFENSE
primary_entity: "분석자가 선택한 방산 기업"
candidate_entities: []
as_of_date: "2026-05-31"
output_formats: ["report_plan", "research_thesis", "qa_report"]
page_orientation: portrait
language: ko-KR
```

첫 실험에서는 PPTX/PDF를 만들지 않는다. 보고서 구조와 리서치 논리가 검증된 뒤에만 HTML preview나 PPT 작업으로 넘어간다.

## 5. 사람 검토 체크리스트

- 핵심 수치마다 출처, 기간, 단위가 있는가?
- DART/OpenDART 실제값과 회사 IR 가이던스가 분리되는가?
- 수주잔고와 수출 계약이 단순 성장 문구가 아니라 매출 인식·마진·현금흐름으로 연결되는가?
- 생산능력, 납기, 승인, 현지화 조건 같은 반증 변수가 보이는가?
- 산업 보고서가 기업 추천서처럼 변질되지 않았는가?
- Top Pick 비교에서 모든 후보가 동일 KPI 정의·기간·단위로 비교되는가?
- QA 통과 전 release-ready 표현이 없는가?

## 6. 자동화로 넘어가는 기준

아래 문제가 반복될 때만 코딩 자동화를 검토한다.

- OpenDART 숫자 수집을 매번 수동으로 하기 어렵다.
- source register와 normalized facts 작성에 시간이 과도하게 걸린다.
- JSON/YAML 형식 오류가 자주 발생한다.
- QA gate를 사람이 매번 확인하기 어렵다.
- 같은 섹터/회사군을 반복 생산해야 한다.

그 전까지는 no-code 프롬프트 체인이 더 빠르고 통제 가능하다.

