# Member Workflow

## 1. 부원 입장에서의 목표

부원은 OpenDART API Key와 기업명 또는 종목코드만 준비하면 된다. 시스템은 재무자료를 자동 수집하고, GIC v12/v13 기준의 HTML preview와 QA report를 만든다.

## 2. 가장 단순한 흐름

1. `examples/defense_company_request.yaml`을 복사한다.
2. 기업명 또는 종목코드를 입력한다.
3. 사업연도와 보고서 코드를 선택한다.
4. 실행한다.
5. `outputs/<run_id>/deliverables/preview.html`을 연다.
6. `outputs/<run_id>/audit/qa_report.md`를 확인한다.
7. FAIL 항목을 수정한다.

## 3. 부원이 이해해야 할 세 가지 상태

| 상태 | 뜻 | 행동 |
|---|---|---|
| `verified` | OpenDART 또는 검증된 공개자료로 확인 | 보고서 핵심 근거로 사용 가능 |
| `pending` | 자동 추출 후보이나 사람 확인 필요 | claim confidence를 낮추거나 검토 |
| `unavailable` | 공개자료에서 확인 불가 | 추정 금지, source gap으로 남김 |

## 4. 산출물 읽는 법

- `source_register.md`: 어떤 자료를 근거로 썼는지.
- `normalized_facts.json`: 실제 수치가 어떤 구조로 들어갔는지.
- `derived_metrics.json`: 계산된 지표가 어떤 fact에서 나왔는지.
- `driver_map.json`: 숫자가 매출/마진/현금흐름/가치평가로 어떻게 연결되는지.
- `report_plan.json`: HTML preview의 논리 구조.
- `qa_report.md`: 발표 또는 제출 전에 고쳐야 할 것.

## 5. HTML preview 사용법

HTML preview는 제출물이 아니라 검토 화면이다.

- 브라우저에서 열어 읽는다.
- 표와 차트 하단의 source label을 확인한다.
- `DRAFT - QA NOT APPROVED`가 보이면 제출하지 않는다.
- 브라우저 인쇄 기능으로 PDF draft를 만들 수 있지만, QA 통과 전에는 final로 부르지 않는다.

## 6. OpenDART-only report의 한계

OpenDART API만으로도 재무제표 기반 회사 분석은 가능하다. 하지만 방산 투자 thesis에 중요한 수주잔고, 수출 계약, 제품 믹스, 납기, 현지화 조건은 모든 회사에서 구조화 API로 나오지 않을 수 있다.

이 경우 v13은 빈칸을 메우지 않는다.

- thesis가 약해지면 warning.
- 핵심 claim에 근거가 없으면 fail.
- 사람이 IR 또는 사업보고서 표를 evidence inbox에 넣으면 다음 실행에서 보강.

