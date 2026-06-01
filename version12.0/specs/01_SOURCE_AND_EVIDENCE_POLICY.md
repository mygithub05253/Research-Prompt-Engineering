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
