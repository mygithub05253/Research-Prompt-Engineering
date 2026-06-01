# v13 QA Lint Rules

## 1. Gate Summary

| Gate | Status Logic |
|---|---|
| G1 Evidence | 핵심 claim에 evidence link가 없으면 FAIL |
| G2 Calculation | 계산 오차 또는 입력 fact 누락이면 FAIL |
| G3 Scenario | actual/guidance/estimate/assumption 혼합이면 FAIL |
| G4 Research Quality | mechanism 또는 financial impact가 비어 있으면 WARNING/FAIL |
| G5 Mode & Design | orientation이 mode와 다르면 FAIL |
| G6 Render Integrity | HTML source label, title, unit, period 누락이면 FAIL |

## 2. Calculation Lints

- `OPM = operating_income / revenue`
- `YoY = current / previous - 1`
- `FCF = operating_cash_flow - capex`
- `Net Debt = total_debt - cash`
- CFS/OFS 혼용 금지.
- FY/Q/YTD 혼용 금지.
- 금액 단위가 다르면 계산 전 변환 로그 필요.

## 3. DEFENSE Lints

필수 KPI:

- 수주잔고
- 신규 수출계약 및 파이프라인
- 수출 비중/제품 믹스
- 생산능력과 납기
- 영업이익률 및 현금전환
- 환율/승인/현지화 조건

처리:

- `verified`: claim 근거 가능.
- `pending`: warning.
- `unavailable`: 핵심 thesis에 직접 사용 금지.
- `conflicted`: fail 또는 별도 설명 필요.

## 4. HTML Lints

- DRAFT 상태 표시 여부.
- source label 존재 여부.
- 빈 chart/table block 여부.
- 숫자 단위와 기간 표시 여부.
- 한글/영문/숫자/%, 통화, EV/EBITDA 표시 smoke check.

## 5. Release Approval

v13 MVP에서 release approval은 최종 제출 승인이 아니라 `HTML review draft is internally usable`을 의미한다.

```yaml
release_approved: false
human_reviewed: false
```

기본값은 항상 위와 같다. 사람이 QA를 검토하기 전에는 true로 변경하지 않는다.

