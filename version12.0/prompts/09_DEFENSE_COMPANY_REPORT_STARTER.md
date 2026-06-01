# GIC v12 DEFENSE Company Report Starter Prompt

이 프롬프트는 첫 no-code 실험용 통합 프롬프트다. ChatGPT, Claude Chat, Gemini에 `Master System Prompt`를 먼저 넣은 뒤, 아래 프롬프트를 붙여넣고 자료를 이어서 제공한다.

---

## Starter Prompt

```text
나는 GIC v12 방식으로 DEFENSE 섹터의 COMPANY_REPORT 초안을 만들고 싶다.
단, 바로 보고서 문장을 쓰지 말고 아래 순서로만 진행하라.

목표:
- 공개 자료 기반의 방산 기업 리서치 구조를 만든다.
- 사실, 파생 계산, 가정, 전망, 판단, 반증 조건을 분리한다.
- 모든 핵심 claim에 evidence link를 붙인다.
- 최종 산출물은 release-ready가 아니라 QA 전 draft로 둔다.

대상 설정:
- report_mode: COMPANY_REPORT
- sector_id: DEFENSE
- primary_entity: [여기에 기업명 입력]
- as_of_date: [YYYY-MM-DD]
- output_formats: report_plan, research_thesis, qa_report
- orientation: portrait
- language: ko-KR

제공할 자료:
1. DART/OpenDART 재무 수치:
[여기에 매출, 영업이익, CFO, CAPEX, 현금, 차입금 등 붙여넣기]

2. 회사 IR/사업보고서에서 확인한 방산 KPI:
[여기에 수주잔고, 신규 수출계약, 수출 비중, 제품 믹스, 생산능력, 납기, 현금전환 관련 수치 붙여넣기]

3. 산업/정책 자료:
[여기에 국방비, 방산 수출, 승인/현지화, 지정학/정책 자료 붙여넣기]

4. 자료 출처 목록:
[여기에 source_id, 자료명, 발행자, 발행일, 기준일, URL 또는 파일명을 붙여넣기]

반드시 출력할 산출물:
1. request.yaml
2. source_register.md
3. normalized_facts.json
4. sector_kpi_checklist.md
5. driver_map.yaml
6. assumptions.md
7. claim_evidence_matrix.md
8. report_plan.json
9. research_thesis.md
10. qa_report.md

실행 규칙:
- 자료가 부족하면 결론을 만들지 말고 `additional source required`로 표시한다.
- 방법론 문서와 GIC 디자인 양식은 사실 근거로 쓰지 않는다.
- 회사 발표 수치와 작성자 판단을 분리한다.
- 수치 단위, 기간, 연결/별도, actual/guidance/estimate 구분을 유지한다.
- 각 핵심 문단은 Fact -> Mechanism -> Financial Impact -> Judgment -> Falsifier 순서로 작성한다.
- QA gate 중 하나라도 FAIL이면 release_approved는 false다.

먼저 Step 1~3 산출물(request.yaml, source_register.md, normalized_facts.json)만 작성하고 멈춰라.
내가 확인 후 "계속"이라고 하면 Step 4부터 진행하라.
```

## Recommended Use

1. `prompts/08_NO_CODE_PROMPT_PACK.md`의 Master System Prompt를 먼저 붙여넣는다.
2. 이 starter prompt를 붙여넣는다.
3. 실제 자료를 붙여넣는다.
4. 모델이 Step 1~3만 출력하게 둔다.
5. 사람이 source와 fact를 검토한 뒤 "계속"을 입력한다.
6. Step 4~10까지 진행한다.

## First-Human-Review Check

Step 1~3 이후 사람은 아래를 확인한다.

- source_id가 중복되지 않는가?
- METHOD/DESIGN 자료가 사실 근거로 분류되지 않았는가?
- 핵심 수치마다 source_locator가 있는가?
- actual, guidance, estimate가 분리되는가?
- DEFENSE KPI에 필요한 자료가 충분한가?

